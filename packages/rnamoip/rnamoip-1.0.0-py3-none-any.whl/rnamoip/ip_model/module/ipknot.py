from dataclasses import dataclass, field
from typing import Any

from ...database.catalog import Catalog
from ...database.model.common import Pairing
from ..model.base_model import BaseModel


@dataclass
class IPKnot:
    model: BaseModel
    pairing_vars: dict[Pairing, Any]
    base_pairings_per_lvl: dict[int, dict[Pairing, Any]]
    catalog: Catalog

    maximum_pairing_level: int

    # Catalog variables
    base_pairings_proba: dict[Pairing, float] = field(init=False)

    weight_per_lvl = {
        0: 0.5,
        1: 0.25,
        2: 0.125,
        3: 0.0625,
    }

    def __post_init__(self):
        self.base_pairings_proba = self.catalog.base_pairings_proba

    def define_base_pairings_proba_variables(self):
        for (start, end) in self.base_pairings_proba:
            if (start, end) not in self.pairing_vars:
                var = self.model.add_var(name=f'b_prob_p0_{start}_{end}')
                self.pairing_vars[(start, end)] = var
                self.base_pairings_per_lvl[0][(start, end)] = var
            else:
                self.base_pairings_per_lvl[0][(start, end)] = self.pairing_vars[(start, end)]

        for lvl in range(1, self.maximum_pairing_level):
            for (start, end) in self.base_pairings_proba:
                var = self.model.add_var(name=f'b_prob_p{lvl}_{start}_{end}')
                self.base_pairings_per_lvl[lvl][(start, end)] = var

    def eq5_one_pairing_per_base(self):
        for n in range(len(self.catalog.rna_sequence)):
            base_vars = []
            for lvl in range(self.maximum_pairing_level):
                base_vars.extend([1 - var for pair, var in self.base_pairings_per_lvl[lvl].items()
                                  if n in pair])

            self.model.add_constr(self.model.sum(base_vars) <= 1)

    def eq6_pairings_possibilities_constraints(self):
        for lvl in range(self.maximum_pairing_level):
            for (i, j) in self.base_pairings_proba:
                for (k, l) in self.base_pairings_proba:
                    i2, j2, k2, l2 = i, j, k, l
                    if not (i < j and k < l) or (i, j) == (k, l):
                        continue
                    # Make sure the pairing are sequential
                    if i > k:
                        i2, j2, k2, l2 = k, l, i, j
                    # If the pairings crossed each other, ignored
                    if i2 < j2 < k2 < l2 or i2 < k2 < l2 < j2:
                        continue

                    self.model.add_constr(self.base_pairings_per_lvl[lvl][(i2, j2)]
                                          + self.base_pairings_per_lvl[lvl][(k2, l2)] >= 1)

    def eq7_ensure_crossing_in_sublvl(self):
        for lvl in range(1, self.maximum_pairing_level):
            sublvl_pairings = self.base_pairings_per_lvl[lvl - 1]
            for (k, l), pairing_var in self.base_pairings_per_lvl[lvl].items():
                left_pairings = list(filter(lambda i_j: i_j[0] < k < i_j[1] < l, sublvl_pairings))
                right_pairings = list(filter(lambda i_j: k < i_j[0] < l < i_j[1], sublvl_pairings))
                left_pairing_sum = self.model.sum(1 - var for p, var in sublvl_pairings.items() if p in left_pairings)
                right_pairing_sum = self.model.sum(1 - var for p, var in sublvl_pairings.items() if p in right_pairings)
                self.model.add_constr(
                    left_pairing_sum + right_pairing_sum >= 1 - pairing_var,
                )

    def eq8_9_prevent_lonely_base_pairs(self):
        for lvl in range(self.maximum_pairing_level):
            for n in range(len(self.catalog.rna_sequence)):
                neirbourghs = []
                middle_pos = [var for pair, var in self.base_pairings_per_lvl[lvl].items()
                              if n in pair]
                middle_pairing = len(middle_pos) - self.model.sum(middle_pos)
                if n > 0:
                    left_pos = [var for pair, var in self.base_pairings_per_lvl[lvl].items()
                                if n - 1 in pair]
                    neirbourghs.append(len(left_pos) - self.model.sum(left_pos))
                if n < len(self.catalog.rna_sequence):
                    right_pos = [var for pair, var in self.base_pairings_per_lvl[lvl].items()
                                 if n + 1 in pair]
                    neirbourghs.append(len(right_pos) - self.model.sum(right_pos))

                self.model.add_constr(self.model.sum(neirbourghs) >= middle_pairing)

    def eq_enforce_lvl2_pseudoknot(self):
        lvl2_pairings = self.base_pairings_per_lvl[1]
        lvl2_sum = self.model.sum(1 - var for var in lvl2_pairings.values())
        self.model.add_constr(lvl2_sum >= 1)

    def objective(self):
        sum_list = []
        for lvl, pairing_list in self.base_pairings_per_lvl.items():
            sum_list.append(self.weight_per_lvl[lvl] * self.model.sum(
                (1 - var) * self.base_pairings_proba[(i, j)] for (i, j), var in
                pairing_list.items()
            ))
        return self.model.sum(sum_list)
