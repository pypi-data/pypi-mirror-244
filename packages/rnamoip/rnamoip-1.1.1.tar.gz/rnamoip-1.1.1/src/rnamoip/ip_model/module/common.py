
from dataclasses import dataclass
from itertools import chain
from math import ceil
from typing import Any

from ...database.catalog import Catalog
from ...database.model.common import Pairing
from ..model.base_model import BaseModel


@dataclass
class CommonConstraint:
    model: BaseModel
    pairing_vars: dict[Pairing, Any]
    base_pairings_per_lvl: dict[int, dict[Pairing, Any]]
    catalog: Catalog

    minimum_pairing_coverage: float
    maximum_pairing_level: int

    def eq_no_lonely_pairings(self):
        length = len(self.catalog.rna_sequence)
        for lvl in range(self.maximum_pairing_level):
            for n in range(length):
                left_neirbourghs = []
                right_neirbourghs = []
                pairings = self.base_pairings_per_lvl[lvl].items()
                left_middle_pos = [var for pair, var in pairings if n == pair[0]]
                left_middle_pairing = len(left_middle_pos) - self.model.sum(left_middle_pos)
                right_middle_pos = [var for pair, var in pairings if n == pair[1]]
                right_middle_pairing = len(right_middle_pos) - self.model.sum(right_middle_pos)
                if n > 0:
                    left_pos_1 = [var for pair, var in pairings if n - 1 == pair[0]]
                    left_neirbourghs.append(len(left_pos_1) - self.model.sum(left_pos_1))
                if n < length:
                    right_pos_2 = [var for pair, var in pairings if n + 1 == pair[1]]
                    right_neirbourghs.append(len(right_pos_2) - self.model.sum(right_pos_2))

                left_pos_2 = [var for pair, var in pairings if n + 1 == pair[0]]
                left_neirbourghs.append(len(left_pos_2) - self.model.sum(left_pos_2))
                right_pos_1 = [var for pair, var in pairings if n - 1 == pair[1]]
                right_neirbourghs.append(len(right_pos_1) - self.model.sum(right_pos_1))
                self.model.add_constr(self.model.sum(left_neirbourghs) >= left_middle_pairing)
                self.model.add_constr(self.model.sum(right_neirbourghs) >= right_middle_pairing)

    def eq_minimum_pairing_coverage(self):
        sum_pairings = self.model.sum(
            1 - var
            for var in chain(*[val.values() for val in self.base_pairings_per_lvl.values()])
        )
        pairing_count = len(self.catalog.rna_sequence) * self.minimum_pairing_coverage
        self.model.add_constr(sum_pairings * 2 >= ceil(pairing_count))
