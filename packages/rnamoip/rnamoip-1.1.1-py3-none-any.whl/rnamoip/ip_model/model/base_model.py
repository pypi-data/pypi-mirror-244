
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Optional


class Optimisation(Enum):
    MAX_OPTIMISATION = 'maximize'
    MIN_OPTIMISATION = 'minimize'


class IPMode(Enum):
    GUROBI = 'GRB'
    CBC = 'CBC'
    DEFAULT = ''


class BaseModel(ABC):
    @abstractmethod
    def initialize(
        self,
        model_name: str,
        mode: IPMode,
        optimization: Optimisation,
        gurobi_env: Optional[Any],
        time_limit: float,
        max_solutions_count: int,
    ):
        pass

    def add_constr(self, constr):
        pass

    def add_var(self, var, var_type):
        pass

    def add_objective(self, var):
        pass

    def optimize(self):
        pass

    def save(self):
        pass

    def sum(self, iterable):
        pass

    def clear(self):
        pass

    def dispose(self):
        pass

    def get_variables_name(self, vars) -> list[str]:
        pass

    def get_variable_name(self, var) -> str:
        pass

    def is_feasible(self) -> bool:
        pass

    def get_solution_count(self) -> int:
        pass

    def get_solution_score(self) -> float:
        pass

    def get_solution_code(self) -> str:
        pass

    def get_var_val(self, var) -> int:
        pass

    def get_solutions_list(self) -> list[dict]:
        pass
