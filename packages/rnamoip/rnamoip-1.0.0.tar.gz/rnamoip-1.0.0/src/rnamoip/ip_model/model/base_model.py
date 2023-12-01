
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

    @abstractmethod
    def add_constr(self, constr):
        pass

    @abstractmethod
    def add_var(self, var, var_type):
        pass

    @abstractmethod
    def add_objective(self, var):
        pass

    @abstractmethod
    def optimize(self):
        pass

    @abstractmethod
    def save(self):
        pass

    @abstractmethod
    def sum(self, iterable):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def dispose(self):
        pass

    @abstractmethod
    def get_variables_name(self, vars) -> list[str]:
        pass

    def get_variable_name(self, var) -> str:
        pass

    @abstractmethod
    def is_feasible(self) -> bool:
        pass

    @abstractmethod
    def get_solution_count(self) -> int:
        pass

    @abstractmethod
    def get_solution_score(self) -> float:
        pass

    @abstractmethod
    def get_solution_code(self) -> str:
        pass

    @abstractmethod
    def get_var_val(self, var) -> int:
        pass

    def get_solutions_list(self) -> list[dict]:
        pass
