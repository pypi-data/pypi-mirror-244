
from glpk import glpk, GLPK
from glpk import mpsread

from .mip_model import MipModel


class GLPKModel(MipModel):
    def optimize(self):
        # Save the model, then send it to glpk
        self.save()
        readfile = f'{self.model_name}.mps.gz'
        c, A_ub, b_ub, A_eq, b_eq, bounds = mpsread(readfile, fmt=GLPK.GLP_MPS_FILE, ret_glp_prob=False)
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
