import logging
from typing import Optional

try:
    import gurobipy as gp
except ImportError:
    logging.warning('Gurobi not found in env.')

from .base_model import BaseModel, Optimisation, IPMode


class GurobiModel(BaseModel):
    model: gp.Model
    model_name: str
    optimization: Optimisation
    var_list: list

    def initialize(
        self,
        model_name: str,
        mode: IPMode,
        optimization: Optimisation,
        gurobi_env: Optional[gp.Env],
        time_limit: float,
        max_solutions_count: int,
    ):
        if not gurobi_env:
            self.model = gp.Model(
                name=model_name,
            )
        else:
            self.model = gp.Model(
                name=model_name,
                env=gurobi_env,
            )
        self.model_name = model_name
        self.optimization = optimization if gp.GRB.MAXIMIZE == Optimisation.MAX_OPTIMISATION else gp.GRB.MINIMIZE
        self.model.params.IntFeasTol = 1e-6
        self.model.params.TimeLimit = time_limit
        self.model.params.PoolSolutions = max_solutions_count
        # do a systematic search for the k-best solutions
        self.model.setParam(gp.GRB.Param.PoolSearchMode, 2)
        self.var_list = []

    def add_constr(self, constr):
        self.model.addConstr(constr)

    def add_var(self, name, var_type='B'):
        var = self.model.addVar(name=name, vtype=var_type)
        self.var_list.append(var)
        return var

    def add_objective(self, expr):
        self.model.setObjective(expr, self.optimization)

    def optimize(self):
        self.model.optimize()

    def save(self):
        self.model.write(self.model_name)

    def sum(self, iterable):
        return sum(iterable)

    def clear(self):
        self.model.reset(1)

    def dispose(self):
        self.model.dispose()

    def get_variables_name(self, vars):
        return [var.VarName for var in vars]

    def get_variable_name(self, var) -> str:
        return var.VarName

    def is_feasible(self) -> bool:
        return self.model.Status == gp.GRB.OPTIMAL

    def get_solution_count(self) -> int:
        return self.model.SolCount

    def get_solution_score(self) -> float:
        return self.model.getObjective().getValue()

    def get_solution_code(self) -> str:
        return self.model.Status

    def get_var_val(self, var) -> int:
        return var.x

    def get_solutions_list(self) -> list[dict]:
        variables_solution_list = []
        for i in range(self.get_solution_count()):
            self.model.params.SolutionNumber = i
            variables_solution_list.append({
                **{self.get_variable_name(var): var.Xn for var in self.var_list},
                'solution_score': self.model.ObjBound,
                'solution_code': self.get_solution_code(),
                'solution_id': i,
            })
        return variables_solution_list
