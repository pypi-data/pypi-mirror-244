
import logging
from typing import Any, Optional

try:
    from docplex.mp.model import Model, ObjectiveSense
except ImportError:
    logging.debug('CPlex not found in env.')

from .base_model import BaseModel, Optimisation, IPMode


class CPLEXModel(BaseModel):
    '''
    Warning: Not fully tested Implementation
    '''
    model: Any
    model_name: str
    status: str
    time_limit: int
    sens: str
    solution: Any

    def initialize(
        self,
        model_name: str,
        mode: IPMode,
        optimization: Optimisation,
        gurobi_env: Optional[Any],
        time_limit: float,
    ):
        self.model = Model(model_name)
        self.sense = ObjectiveSense.Maximize if optimization == Optimisation.MAX_OPTIMISATION \
            else ObjectiveSense.Minimize
        self.time_limit = time_limit

    def add_constr(self, constr):
        self.model.add_constraint(constr)

    def add_var(self, name) -> Any:
        return self.model.binary_var(name)

    def add_objective(self, expr):
        self.model.set_objective(self.sense, expr)

    def optimize(self):
        self.solution = self.model.solve(TimeLimit=self.time_limit)

    def save(self):
        self.model.export_as_mps()

    def sum(self, iterable):
        return self.model.sum(iterable)

    def clear(self):
        self.model.clear()

    def get_variables_name(self, vars: list[Any]):
        return [var.short_name for var in vars]

    def get_variable_name(self, var) -> str:
        return var.short_name

    def is_feasible(self) -> bool:
        return self.solution.is_feasible_solution()

    def dispose(self):
        pass

    def get_solution_count(self) -> int:
        return len(self.solution)

    def get_solution_score(self) -> int:
        return self.solution.get_objective_value()

    def get_solution_code(self) -> str:
        return self.solution.solve_status

    def get_var_val(self, var: Any) -> int:
        return self.solution.get_var_value(var)
