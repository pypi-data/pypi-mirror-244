import logging
from collections import defaultdict
from enum import Enum
from itertools import chain
from typing import Any

from rnamoip.config import (
    CommonConfig, CommonEquation, Config, IPKnotConfig, Module, RNAMoIPConfig,
)
from rnamoip.database.catalog import Catalog
from rnamoip.database.model.common import Pairing
from rnamoip.helpers.structure import StructureHelper

from .model.base_model import BaseModel, IPMode, Optimisation
from .model.cplex_model import CPLEXModel
from .model.glpk_model import GLPKModel
from .model.google_model import GoogleModel
from .model.gurobi_model import GurobiModel
from .model.mip_model import MipModel
from .module.common import CommonConstraint
from .module.ipknot import IPKnot
from .module.rnamoip import RNAMoIP

INSERTED_PAIR_VALUE = 0
INSERTED_MOTIF_VALUE = 1


class Solver(Enum):
    MIP = 'MIP'
    GRB = 'GRB'
    CP_SAT = 'CP-SAT'
    GLPK = 'GLPK'
    CPLEX = 'CPLEX'


class IPManager:
    model: BaseModel
    model_name: str = 'rnamoip.mps'
    motifs_vars: dict
    pairing_vars: dict[Pairing, Any]
    base_pairings_per_lvl: dict[int, dict[Pairing, Any]]
    config: Config
    alpha: float

    def __init__(self, config: Config, solver: str, gurobi_env: Any, alpha: float):
        self.config = config
        if solver == solver.MIP:
            self.model = MipModel()
        elif solver == solver.GRB:
            self.model = GurobiModel()
        elif solver == solver.CP_SAT:
            self.model = GoogleModel()
        elif solver == solver.GLPK:
            self.model = GLPKModel()
        elif solver == solver.CPLEX:
            self.model = CPLEXModel()
        else:
            raise Exception(f"Invalid Solver '{solver}' passed in config. Did you mean 'MIP' or 'GRB' ?")

        self.alpha = alpha
        self.motifs_vars = defaultdict(dict)
        self.pairing_vars = defaultdict(dict)
        self.base_pairings_per_lvl = defaultdict(dict)
        mode = IPMode(self.config.get_property(CommonConfig.SOLVER_MODE))
        time_limit = config.get_property(CommonConfig.TIME_LIMIT)
        max_solutions_count = config.get_property(CommonConfig.MAXIMUM_SOLUTION_COUNT)
        self.model.initialize(
            optimization=Optimisation.MIN_OPTIMISATION,
            model_name=self.model_name,
            mode=mode,
            gurobi_env=gurobi_env,
            time_limit=time_limit,
            max_solutions_count=max_solutions_count,
        )

    def initialize(
        self,
        catalog: Catalog,
        model_name: str,
    ):
        self.catalog = catalog
        self.model_name = model_name
        maximum_pairing_level = self.config.get_property(CommonConfig.MAXIMUM_PAIRING_LEVEL)

        for lvl in range(maximum_pairing_level):
            self.base_pairings_per_lvl[lvl] = dict()

        self.rnamoip = RNAMoIP(
            self.model,
            self.motifs_vars,
            self.pairing_vars,
            self.base_pairings_per_lvl,
            self.catalog,
            self.config.get_property(CommonConfig.ENABLE_DELETE_PAIR_IN_RNAMOIP),
            self.config.get_property(CommonConfig.DELETION_PENALTY),
            self.config.get_property(CommonConfig.MAXIMUM_COMPLEX_MOTIFS),
            self.config.get_property(CommonConfig.MAXIMUM_PERCENTAGE_OF_DELETED_PAIRS),
            self.config.get_property(CommonConfig.MINIMUM_PAIRING_DISTANCE),
            self.config.get_property(CommonConfig.ENABLE_PSEUDONOTABLE_MOTIF),
        )

        self.ipknot = IPKnot(
            self.model,
            self.pairing_vars,
            self.base_pairings_per_lvl,
            self.catalog,
            maximum_pairing_level,
        )

        self.common_constraint = CommonConstraint(
            self.model,
            self.pairing_vars,
            self.base_pairings_per_lvl,
            self.catalog,
            minimum_pairing_coverage=self.config.get_property(CommonConfig.MINIMUM_PAIRING_COVERAGE),
            maximum_pairing_level=maximum_pairing_level,
        )

    @staticmethod
    def execute_equation(module, equation_name: str):
        logging.debug(f"Adding equation: '{equation_name}'")
        try:
            equation = getattr(module, equation_name)
        except AttributeError:
            logging.warn(f"Unknown equation named '{equation_name}' will be skip.")
            return
        equation()

    def maximise_motif(self):
        self.rnamoip.define_motifs_variables()
        self.rnamoip.define_base_pairings_variables()
        self.ipknot.define_base_pairings_proba_variables()

        for eq in RNAMoIPConfig:
            if self.config.get_property(eq, Module.RNAMOIP) is True:
                self.execute_equation(self.rnamoip, eq.value)

        for eq in IPKnotConfig:
            if self.config.get_property(eq, Module.IPKNOT) is True:
                self.execute_equation(self.ipknot, eq.value)

        common_equations = self.config.get_property(CommonConfig.EQUATIONS, Module.COMMON)
        for eq in CommonEquation:
            if common_equations.get(eq.value, False) is True:
                self.execute_equation(self.common_constraint, eq.value)

        rnamoip_objective = self.alpha * self.rnamoip.objective()
        ipknot_objective = (1 - self.alpha) * self.ipknot.objective()

        self.model.add_objective(rnamoip_objective - ipknot_objective)

    def optimize(self) -> dict:
        logging.debug('Optimizing Model...')
        self.model.optimize()
        self.model.save()

        if not self.model.is_feasible():
            logging.warn('The model is not feasible...')
            return {}

        motifs_vars_list = [
            motifs_vars.values()
            for pair in self.motifs_vars
            for motifs_vars in self.motifs_vars[pair].values()
        ]
        all_motif_vars = list(chain(*motifs_vars_list))
        motifs_vars = [
            var for var in all_motif_vars
            if self.model.get_var_val(var) == INSERTED_MOTIF_VALUE
        ]
        motifs_vars = self.model.get_variables_name(motifs_vars)

        # Group by motifs
        motifs_results = [
            self._motif_var_to_result(name) for name in motifs_vars
        ]

        # Extract Pairings Results
        pairing_results = {}
        pairings_name_per_lvl_per_pair = {}
        for lvl, pairings in self.base_pairings_per_lvl.items():
            pairing_results[lvl] = [
                pair for (pair, var) in pairings.items()
                if self.model.get_var_val(var) == INSERTED_PAIR_VALUE
            ]
            pairings_name_per_lvl_per_pair[lvl] = {
                pair: self.model.get_variable_name(var) for (pair, var) in pairings.items()
            }

        solutions_count = self.model.get_solution_count()
        solution_score = self.model.get_solution_score()
        solution_code = self.model.get_solution_code()
        solutions_infos_list = self.get_sub_solutions_results(
            motif_vars=all_motif_vars,
            pairing_vars_per_lvl_per_pair=self.base_pairings_per_lvl,
        )

        return {
            'motifs_result': self.prepare_motif_results(motifs_results),
            'pairing_result': pairing_results,
            'solutions_count': solutions_count,
            'solution_score': solution_score,
            'solution_code': solution_code,
            'solutions_list': solutions_infos_list,
        }

    def get_sub_solutions_results(
        self, motif_vars: list[str], pairing_vars_per_lvl_per_pair: dict[str, Pairing],
    ) -> list[dict]:
        solutions_list = self.model.get_solutions_list()
        solutions_results = []
        for solution in solutions_list:
            pairing_results = {}
            for lvl, pairing_name_per_pair in pairing_vars_per_lvl_per_pair.items():
                pairing_results[lvl] = [
                    pair for pair, var in pairing_name_per_pair.items()
                    if solution[self.model.get_variable_name(var)] == INSERTED_PAIR_VALUE
                ]
            motifs_results = [
                self._motif_var_to_result(self.model.get_variable_name(var)) for var in motif_vars
                if solution[self.model.get_variable_name(var)] == INSERTED_MOTIF_VALUE
            ]
            new_structure = StructureHelper.pairings_per_lvl_to_str(
                pairing_results,
                len(self.catalog.rna_sequence),
            )
            solutions_results.append({
                'motifs_result': self.prepare_motif_results(motifs_results),
                'secondary_structure': new_structure,
                'solution_score': solution['solution_score'],
                'solution_code': solution['solution_code'],
            })
        solutions_results = sorted(solutions_results, key=lambda sol: sol['solution_score'])
        return solutions_results

    def prepare_motif_results(self, motifs_result) -> dict[str, dict]:
        seq_for_motif: dict[str, dict] = {}
        length_motif = 0
        for (seq_id_start, seq_id_end, motif_id, strand_id_str, seq) in motifs_result:
            start = int(seq_id_start)
            end = int(seq_id_end)
            motif = self.catalog.motifs_present[int(motif_id)]
            strand_id = int(strand_id_str)
            sm = seq_for_motif.setdefault(motif_id, {
                'name': motif.name,
                'related_rins': motif.related_ids,
                'strands': [],
            })
            sm['strands'].append({
                'name': motif.name,
                'seq': self.catalog.rna_sequence[start:end + 1],
                'strand_seq': seq,
                'strand_id': strand_id,
                'start': start,
                'end': end,
            })
            length_motif += end - start + 1

        return seq_for_motif

    @staticmethod
    def _motif_var_to_result(motif_var_name: str) -> tuple[str, str, str, str, str]:
        (raw_motif, brin, raw_seq_start, raw_seq_end, raw_seq) = motif_var_name.split('_')
        return (raw_seq_start[1:], raw_seq_end[1:], raw_motif[1:], brin[1], raw_seq)

    def clear(self):
        self.model.clear()
        self.pairing_vars = defaultdict(dict)
        self.motifs_vars = defaultdict(dict)
        self.base_pairings_per_lvl = defaultdict(dict)

    def dispose(self):
        self.clear()
        self.model.dispose()
