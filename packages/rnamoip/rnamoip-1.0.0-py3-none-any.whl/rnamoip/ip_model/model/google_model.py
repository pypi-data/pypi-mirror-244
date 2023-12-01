
import logging
from typing import Any, Optional

from ortools.sat.python import cp_model
from ortools.sat.cp_model_pb2 import CpSolverStatus

from .base_model import BaseModel, IPMode, Optimisation


class SolutionCollecter(cp_model.CpSolverSolutionCallback):
    solution_count: int = 0

    def __init__(self, variables):
        super().__init__()
        self.variables = variables
        self.variables_solution_list = []

    def on_solution_callback(self):
        status = CpSolverStatus.Name(self.Response().status)
        self.variables_solution_list.append({
            **{str(var): self.Value(var) for var in self.variables},
            'solution_score': self.ObjectiveValue(),
            'solution_code': status,
            'solution_id': self.solution_count,
        })
        self.solution_count += 1


class GoogleModel(BaseModel):
    model: cp_model.CpModel
    model_name: str
    optimization: Optimisation
    solver: cp_model.CpSolver = None
    collector: SolutionCollecter = None
    status: int = None
    time_limit: int
    max_solutions_count: int
    var_list: list

    def initialize(
        self,
        model_name: str,
        mode: IPMode,
        optimization: Optimisation,
        gurobi_env: Optional[Any],
        time_limit: float,
        max_solutions_count: int,
    ):
        self.model = cp_model.CpModel()
        self.model_name = model_name
        self.optimization = optimization
        self.time_limit = time_limit
        self.max_solutions_count = max_solutions_count
        self.var_list = []

    def add_constr(self, constr):
        self.model.Add(constr)

    def add_var(self, name, var_type='B'):
        var = self.model.NewBoolVar(name=name)
        self.var_list.append(var)
        return var

    def add_objective(self, expr):
        if self.optimization == Optimisation.MAX_OPTIMISATION:
            self.model.Maximize(expr)
        elif self.optimization == Optimisation.MIN_OPTIMISATION:
            self.model.Minimize(expr)

    def optimize(self):
        self.solver = cp_model.CpSolver()
        self.solver.parameters.max_time_in_seconds = self.time_limit
        self.solver.parameters.keep_all_feasible_solutions_in_presolve = True
        self.collector = SolutionCollecter(self.var_list)
        self.status = self.solver.Solve(self.model, self.collector)

    def save(self):
        pass

    def sum(self, iterable):
        return sum(iterable)

    def clear(self):
        self.model = cp_model.CpModel()

    def dispose(self):
        pass

    def get_variables_name(self, vars: list):
        return [str(var) for var in vars]

    def get_variable_name(self, var) -> str:
        return str(var)

    def is_feasible(self) -> bool:
        status = self.solver.StatusName()
        if status == CpSolverStatus.Name(CpSolverStatus.FEASIBLE):
            logging.warn('No Optimal solution found, only Feasible')
        return self.solver.StatusName() in [
            CpSolverStatus.Name(CpSolverStatus.OPTIMAL), CpSolverStatus.Name(CpSolverStatus.FEASIBLE),
        ]

    def get_solution_count(self) -> int:
        return self.collector.solution_count

    def get_solution_score(self) -> float:
        return self.solver.ObjectiveValue()

    def get_solution_code(self) -> str:
        return self.solver.StatusName()

    def get_var_val(self, var) -> int:
        return self.solver.Value(var)

    def get_solutions_list(self) -> list[dict]:
        sorted_solution = sorted(
            self.collector.variables_solution_list,
            key=lambda sol: sol['solution_score'],
        )
        return sorted_solution[0:self.max_solutions_count]
