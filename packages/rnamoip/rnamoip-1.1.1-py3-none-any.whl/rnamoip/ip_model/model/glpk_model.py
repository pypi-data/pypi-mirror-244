import logging
from typing import Optional, Any

from .mip_model import MipModel
from .base_model import Optimisation, IPMode

try:
    from glpk import glpk, GLPK
    from glpk import mpsread
except ImportError:
    logging.info('GLPK not found in env, skipping import.')


class GLPKModel(MipModel):
    def initialize(
        self,
        model_name: str,
        mode: IPMode,
        optimization: Optimisation,
        gurobi_env: Optional[Any],
        time_limit: float,
        max_solutions_count: int,
    ) -> None:
        logging.warning('Warning, GLPK solver is deprecated for RNAMoIP.')
        super().initialize(model_name, mode, optimization, gurobi_env, time_limit, max_solutions_count)

    def optimize(self):
        # Save the model, then send it to glpk
        self.save()
        readfile = f'{self.model_name}.mps.gz'
        c, A_ub, b_ub, A_eq, b_eq, bounds, integrality = mpsread(readfile, fmt=GLPK.GLP_MPS_FILE, ret_glp_prob=False)
        res = glpk(c, A_ub, b_ub, A_eq, b_eq, bounds)
        self.status = res

    def get_solution_count(self) -> int:
        return 1

    def get_solution_score(self) -> int:
        return 0

    def get_solution_code(self) -> str:
        return 0

    def get_var_val(self, var) -> int:
        return var.x
