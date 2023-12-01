
import logging
from datetime import date, datetime
from functools import reduce
from pathlib import Path
from typing import Any, Optional, Union

from rnamoip.config import CommonConfig, Config
from rnamoip.database.catalog import Catalog
from rnamoip.helpers.sequence import SequenceHelper
from rnamoip.helpers.structure import StructureHelper
from rnamoip.helpers.validation import Validator
from rnamoip.ip_model.ip_manager import IPManager, Solver
from rnamoip.renderer import Result, StdRenderer


class Predicter:
    model: IPManager
    config: Config
    catalog: Catalog
    iteration_count: int = 0
    start_time: date

    initial_secondary_structure: str
    minimum_probability: float
    minimum_pairing_distance: int
    maximum_pairing_level: int
    minimum_alignment_match_threshold: float
    last_initialisation_time: date
    pdb_name: Optional[str]
    pdbs_to_ignore: list[str]
    motifs_present = None
    alpha: float
    motifs: dict = None

    MAX_ITERATION_COUNT: int = 3

    def __init__(
        self,
        configuration_file: Union[str, dict] = None,
        rna_sequence: str = None,
        secondary_structure: str = None,
        alignment: list[str] = None,
        motifs_path: Path = None,
        gurobi_env: Any = None,
        pdb_name: Optional[str] = None,
        pdbs_to_ignore: list[str] = [],
        alpha: Optional[float] = None,
        parser: str = '',
        solver: str = '',
        motifs: dict = None,
    ) -> None:
        self.config = Config(configuration_file)
        self.pdb_name = pdb_name if pdb_name is not None else self.config.get_property(CommonConfig.PDB_NAME)
        if self.pdb_name:
            logging.info(f"Doing PDB {self.pdb_name}...")
        else:
            logging.info("No PDB specified.")
        self.motifs_path = motifs_path if motifs_path else self.config.get_property(CommonConfig.MOTIFS_PATH)
        self.minimum_pairing_distance = self.config.get_property(CommonConfig.MINIMUM_PAIRING_DISTANCE)

        if rna_sequence is not None:
            self.rna_sequence = Validator.validate_rna_seq(rna_sequence)
            self.initial_secondary_structure = Validator.validate_secondary_struct(
                secondary_structure, self.minimum_pairing_distance,
            ) if secondary_structure else len(self.rna_sequence) * SequenceHelper.ANY_NUCLEOTIDE
            self.alignment = Validator.validate_alignment(alignment) if alignment is not None else []
        else:
            self.rna_sequence = self.config.get_property(CommonConfig.SEQUENCE)
            if not self.rna_sequence:
                raise Exception('No RNA sequence specified.')
            self.initial_secondary_structure = self.config.get_property(CommonConfig.SECONDARY_STRUCTURE)
            self.alignment = self.config.get_property(CommonConfig.ALIGNMENT)

        self.minimum_probability = self.config.get_property(CommonConfig.MINIMUM_PAIRING_PROBABILITY)
        self.maximum_pairing_level = self.config.get_property(CommonConfig.MAXIMUM_PAIRING_LEVEL)
        self.minimum_alignment_match_threshold = self.config.get_property(
            CommonConfig.MINIMUM_ALIGNMENT_MATCH_THRESHOLD,
        )
        self.maximum_alignment_distance = self.config.get_property(
            CommonConfig.MAXIMUM_ALIGNMENT_DISTANCE,
        )

        solver = solver if solver else Solver(self.config.get_property(CommonConfig.SOLVER_NAME).upper())
        self.alpha = alpha if alpha is not None else self.config.get_property(CommonConfig.ALPHA_WEIGHT)
        self.model = IPManager(self.config, solver, gurobi_env=gurobi_env, alpha=self.alpha)
        self.last_initialisation_time = datetime.now()
        self.start_time = datetime.now()
        if pdbs_to_ignore:
            self.pdbs_to_ignore = pdbs_to_ignore
        else:
            self.pdbs_to_ignore = [self.pdb_name] if self.pdb_name else []
        self.parser = parser if parser else self.config.get_property(CommonConfig.PARSER)
        self.motifs = motifs

    def iterate(self) -> Result:
        result = None
        secondary_structure = self.initial_secondary_structure
        ss_results = [secondary_structure]

        while True:
            result_dict = self.predict(secondary_structure)
            predicted_ss: str = result_dict['predicted_ss']
            ss_results.append(predicted_ss)
            self.iteration_count += 1
            logging.info(f"Iteraction #{self.iteration_count} Finished")
            logging.info(f"Current Prediction : {predicted_ss}")

            if (
                self.config.get_property(CommonConfig.ITERATIVE) is False
                or secondary_structure == predicted_ss
                or predicted_ss is None
                or self.iteration_count > self.MAX_ITERATION_COUNT + 1
            ):
                result: Result = self._prepare_result_output(result_dict)
                break

            self.model.clear()
            secondary_structure = predicted_ss
            self.last_initialisation_time = datetime.now()

        logging.info(f"Number of iterations : {self.iteration_count}")
        logging.info(f"Solution Score : {result.solution_score}")
        logging.info(f"Solution Code : {result.solution_code}")
        logging.info(f"Solutions Count : {len(result.solutions_list)}")
        StdRenderer.render(result)
        result.structures = ss_results

        total_time = datetime.now() - self.start_time
        logging.debug(f"Total Process time: {total_time.total_seconds()}s")

        return result

    def predict(self, secondary_structure: Optional[str]) -> dict:
        ss = secondary_structure if secondary_structure else self.initial_secondary_structure
        self.catalog = Catalog(
            self.motifs_path,
            self.rna_sequence,
            self.alignment,
            ss,
            self.minimum_probability,
            self.minimum_pairing_distance,
            self.maximum_pairing_level,
            self.minimum_alignment_match_threshold,
            self.maximum_alignment_distance,
            self.pdb_name,
            self.pdbs_to_ignore,
            self.parser,
            self.motifs_present,
            self.motifs,
        )
        # Cache insertion points
        self.motifs_present = self.catalog.motifs_present
        self.model.initialize(self.catalog, f'ip_step_{self.iteration_count}.lp')
        init_time = datetime.now() - self.last_initialisation_time
        logging.debug(f"Initialization time: {init_time.total_seconds()}s")
        try:
            self.model.maximise_motif()
            logging.debug(f"Getting result for sequence: {self.catalog.rna_sequence}")
            result_dict = self.model.optimize()
        except Exception:
            logging.exception(f'Error on objective function for pdb {self.pdb_name}')
            result_dict = {}

        opti_time = datetime.now() - self.last_initialisation_time
        logging.info(f"Optimization time: {opti_time.total_seconds()}s")
        logging.debug(f"Original Secondary Structure: {self.catalog.secondary_structure}")

        pairing_result = result_dict.get('pairing_result', {})
        new_structure = StructureHelper.pairings_per_lvl_to_str(pairing_result, len(self.catalog.rna_sequence))
        logging.debug(f"Modified Secondary Structure: {new_structure}")
        result_dict['predicted_ss'] = new_structure
        return result_dict

    def _prepare_result_output(self, result_dict: dict):
        pairing_result = result_dict.get('pairing_result', {})
        motifs_result = result_dict.get('motifs_result', {})
        solutions_count = result_dict.get('solutions_count', 0)
        solution_score = result_dict.get('solution_score', 0)
        solution_code = result_dict.get('solution_code', 'No code return')
        solutions_list = result_dict.get('solutions_list', [])
        predicted_ss: str = result_dict['predicted_ss']

        pairings_count = reduce(lambda sum, pairings_per_lvl: len(pairings_per_lvl) + sum, pairing_result.values(), 0)
        nuc_count = pairings_count * 2

        logging.debug(f"Nucleotide Count: {nuc_count}")
        logging.debug(f"Nucleotide Ratio: {nuc_count / len(self.catalog.rna_sequence)}")

        sequence_by_motifs = {}
        for motif in motifs_result.values():
            for strand in motif['strands']:
                for i in range(len(strand['seq'])):
                    sequence_by_motifs[strand['start'] + i] = motif['name']

        execution_time_in_sec = (datetime.now() - self.start_time).total_seconds()
        result = Result(
            sequence=self.rna_sequence,
            initial_structure=self.initial_secondary_structure,
            new_structure=predicted_ss,
            motifs=motifs_result,
            sequence_by_motifs=sequence_by_motifs,
            iterations_count=self.iteration_count,
            execution_time_in_sec=execution_time_in_sec,
            solutions_count=solutions_count,
            solution_score=solution_score,
            solution_code=solution_code,
            motif_type=self.parser,
            alpha=self.alpha,
            solutions_list=solutions_list,
        )
        return result

    def dispose(self):
        self.motifs_present = None
        self.model.dispose()
