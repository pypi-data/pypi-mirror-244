from typing import Any, Optional
from mip import Model, xsum, OptimizationStatus
from mip.constants import BINARY
from mip.entities import Var
from mip import MAXIMIZE, MINIMIZE, constants as mip_constants

from .base_model import BaseModel, Optimisation, IPMode


class MipModel(BaseModel):
    model: Model
    model_name: str
    status: str
    time_limit: int
    optimization: Optimisation

    def initialize(
        self,
        model_name: str,
        mode: IPMode,
        optimization: Optimisation,
        gurobi_env: Optional[Any],
        time_limit: float,
    ):
        optimization = MAXIMIZE if self == optimization.MAX_OPTIMISATION else MINIMIZE
        if mode == IPMode.GUROBI:
            mode = mip_constants.GRB
        elif mode == IPMode.CBC:
            mode = mip_constants.CBC
        else:
            mode = IPMode.DEFAULT

        self.model = Model(sense=optimization, name=model_name, solver_name=mode)
        self.model_name = model_name
        self.time_limit = time_limit

    def add_constr(self, constr):
        self.model += constr

    def add_var(self, name, var_type=BINARY) -> Var:
        return self.model.add_var(name=name, var_type=var_type)

    def add_objective(self, expr):
        self.model += expr

    def optimize(self):
        self.status = self.model.optimize(max_seconds=self.time_limit)

    def save(self):
        self.model.write(self.model_name)

    def sum(self, iterable):
        return xsum(iterable)

    def clear(self):
        self.model.clear()

    def get_variables_name(self, vars):
        return [var.name for var in vars]

    def get_variable_name(self, var) -> str:
        return var.name

    def is_feasible(self) -> bool:
        return self.get_solution_count() > 0

    def dispose(self):
        pass

    def get_solution_count(self) -> int:
        return self.model.num_solutions

    def get_solution_score(self) -> int:
        return self.model.objective_value

    def get_solution_code(self) -> str:
        return OptimizationStatus(self.status).name

    def get_var_val(self, var: Var) -> int:
        return var.x
