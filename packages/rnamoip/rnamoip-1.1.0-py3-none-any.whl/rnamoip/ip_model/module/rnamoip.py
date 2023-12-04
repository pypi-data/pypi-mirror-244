from dataclasses import dataclass, field
from itertools import chain
from math import ceil
from typing import Any

from ...database.catalog import Catalog
from ...database.model.common import Pairing
from ...database.model.motif import Motif
from ...helpers.structure import StructureHelper
from ..model.base_model import BaseModel


@dataclass
class RNAMoIP:
    model: BaseModel
    motifs_vars: dict
    pairing_vars: dict[Pairing, Any]
    base_pairings_per_lvl: dict[int, dict[Pairing, Any]]
    catalog: Catalog

    # Configurations variables
    enable_delete_pairings: bool
    delete_pairings_penalty: int
    maximum_number_of_complex_motif: int
    maximum_percentage_of_deleted_pairs: float
    minimum_pairings_distance: int
    enable_pseudonotable_motif: bool

    # Catalog variables
    rna_sequence: str = field(init=False)
    motifs_present: list[Motif] = field(init=False)
    base_pairings: dict[Pairing, Any] = field(init=False)
    canonical_base_pairings: dict[Pairing, Any] = field(default_factory=dict)

    def __post_init__(self):
        self.rna_sequence = self.catalog.rna_sequence
        self.motifs_present = self.catalog.motifs_present
        self.base_pairings = self.catalog.base_pairings

    def define_motifs_variables(self):
        for m, motif in enumerate(self.motifs_present):
            for s, strand in enumerate(motif.strands):
                for (start, end, seq) in strand.possible_pairings_with_seq:
                    var = self.model.add_var(name=f'm{m}_j{s}_k{start}_l{end}_{seq}')
                    motif = self.motifs_vars[start, end].setdefault(m, {})
                    motif[s] = var

    def define_base_pairings_variables(self):
        for (start, end) in self.base_pairings:
            var = self.model.add_var(name=f'bp_{start}_{end}')
            self.pairing_vars[(start, end)] = var
            self.canonical_base_pairings[(start, end)] = var

    def eq4_hairpins_insertion(self):
        level_two_motifs = self.catalog.motif_present_per_level(2)
        possible_hairpins = self.catalog.motif_present_per_level(1)
        for h, hairpin in possible_hairpins:
            for (start, end) in hairpin.strands[0].possible_pairings:
                left_extremity = []
                right_extremity = []
                for m, motif in level_two_motifs:
                    for kp, lp in motif.strands[0].possible_pairings:
                        if lp == start - 1:
                            left_extremity.append(self.motifs_vars[kp, lp][m][0])
                    for kp, lp in motif.strands[1].possible_pairings:
                        if kp == end + 1:
                            right_extremity.append(self.motifs_vars[kp, lp][m][1])
                left_sum = self.model.sum(left_extremity)
                right_sum = self.model.sum(right_extremity)
                pairings = StructureHelper.get_pairings_stack_on_two_positions(self.pairing_vars,
                                                                               start,
                                                                               end)
                pairings_sum = self.model.sum(1 - self.pairing_vars[pair] for pair in pairings)
                self.model.add_constr(left_sum + right_sum + pairings_sum >= self.motifs_vars[start, end][h][0])

    def eq5_loops_and_bulges_insertion(self):
        level_two_motifs = self.catalog.motif_present_per_level(2)
        for m, motif in level_two_motifs:
            for (u, v), pair_var in self.pairing_vars.items():
                first_sum = self.model.sum(
                    self.motifs_vars[k, l][m][0]
                    for (k, l) in motif.strands[0].possible_pairings
                    if l < u or v < k
                )

                rest_sum = self.model.sum(
                    self.motifs_vars[k, l][m][1]
                    for (k, l) in motif.strands[1].possible_pairings
                    if l < u or v < k
                )
                self.model.add_constr(first_sum - rest_sum <= len(self.rna_sequence) * pair_var)
                self.model.add_constr(first_sum - rest_sum >= -len(self.rna_sequence) * pair_var)

    def eq6_filled_at_least_2_unpaired(self):
        level_two_motifs = self.catalog.motif_present_per_level(2)
        for m, motif in level_two_motifs:
            for (k, l) in motif.strands[0].possible_pairings:
                for (k2, l2) in motif.strands[1].possible_pairings:
                    # Found in the code, but not the equation..
                    if l + self.minimum_pairings_distance > k2:
                        coverage = list(range(k, l + 1)) + list(range(k2, l2 + 1))
                        bases_inside = [(u, v) for (u, v) in self.pairing_vars
                                        if u in coverage and v in coverage]
                        bases = [(u, v) for (u, v) in self.pairing_vars
                                 if u in coverage or v in coverage
                                 and (u, v) not in bases_inside]
                        if len(coverage) - 1 <= 2 * len(bases_inside) + len(bases):
                            self.model.add_constr(self.motifs_vars[k, l][m][0] + self.motifs_vars[k2, l2][m][1] <= 1)

    def eq7_maximum_number_of_k_junction(self):
        complex_motifs_vars = []
        for m, motif in enumerate(self.motifs_present):
            if motif.level >= 3:
                vars = [self.motifs_vars[k, l][m][0] for (k, l) in motif.strands[0].possible_pairings]
                complex_motifs_vars.extend(vars)
        self.model.add_constr(self.model.sum(complex_motifs_vars) <= self.maximum_number_of_complex_motif)

    def eq8_k_junctions_insertion(self):
        for m, motif in enumerate(self.motifs_present):
            if motif.level > 2:
                for (u, v), pair_var in self.pairing_vars.items():
                    first_sum = self.model.sum(
                        self.motifs_vars[k, l][m][0]
                        for (k, l) in motif.strands[0].possible_pairings
                        if u <= k <= l <= v
                    )

                    rest_sum = self.model.sum(
                        self.motifs_vars[k, l][m][s]
                        for s, strand in enumerate(motif.strands[1:], 1)
                        for (k, l) in strand.possible_pairings
                        if u <= k <= l <= v
                    )
                    self.model.add_constr(
                        (motif.level - 1) * first_sum - rest_sum <= len(self.rna_sequence) * pair_var,
                    )
                    self.model.add_constr(
                        (motif.level - 1) * first_sum - rest_sum >= -len(self.rna_sequence) * pair_var,
                    )

    def eq9_10_motifs_completness(self):
        for m, motif in enumerate(self.motifs_present):
            if motif.level > 1:
                for s, strand in enumerate(motif.strands):
                    for (k0, l0) in strand.possible_pairings:
                        var = self.motifs_vars[k0, l0][m][s]
                        # Look Right
                        if s < motif.level - 1:
                            right_vars = [self.motifs_vars[k, l][m][s + 1] for (k, l)
                                          in motif.strands[s + 1].possible_pairings
                                          if l0 + 5 < k]
                            self.model.add_constr(var <= self.model.sum(right_vars))
                        # Look Left
                        if s > 0:
                            right_vars = [self.motifs_vars[k, l][m][s - 1] for (k, l)
                                          in motif.strands[s - 1].possible_pairings
                                          if l < k0 - 5]
                            self.model.add_constr(var <= self.model.sum(right_vars))

    def eq11_strands_completeness(self):
        for m, motif in enumerate(self.motifs_present):
            if motif.level > 1:
                sum_first_strand = self.model.sum(
                    self.motifs_vars[k, l][m][0] for (k, l) in motif.strands[0].possible_pairings
                )
                for s, strand in enumerate(motif.strands[1:], 1):
                    sum_s_strand = self.model.sum(self.motifs_vars[k, l][m][s] for (k, l) in strand.possible_pairings)
                    self.model.add_constr(sum_first_strand - sum_s_strand == 0)

    def eq12_insertion_overlap_pairings(self):
        for m, motif in enumerate(self.motifs_present):
            if motif.level > 1:
                for s, strand in enumerate(motif.strands):
                    for k, l in strand.possible_pairings:
                        pairing_sum = self.model.sum(
                            1 - var for (u, v), var in self.pairing_vars.items()
                            if (k - 1 <= u <= k)
                            or (l <= u <= l + 1)
                            or (k - 1 <= v <= k)
                            or (l <= v <= l + 1)
                        )
                        self.model.add_constr(self.motifs_vars[k, l][m][s] <= pairing_sum)

    def eq13_prevent_strands_overlapping(self):
        for u in range(len(self.rna_sequence)):
            pairing_vars = [1 - var for pair, var in self.pairing_vars.items()
                            if u in pair]

            strand_at_vars = []
            for (k, l) in self.motifs_vars:
                if u in (k, l):
                    pair_vars = [var.values() for var in self.motifs_vars[k, l].values()]
                    strand_at_vars.extend(list(chain(*pair_vars)))
            if pairing_vars or strand_at_vars:
                strand_vars = []
                for (k, l) in self.motifs_vars:
                    if k < u < l:
                        pair_vars = [var.values() for var in self.motifs_vars[k, l].values()]
                        strand_vars.extend(list(chain(*pair_vars)))

                self.model.add_constr(
                    (4 * self.model.sum(strand_vars)
                     + 1 * (self.model.sum(pairing_vars) if pairing_vars else 0)
                     + 3 * (self.model.sum(strand_at_vars) if strand_at_vars else 0)) <= 4,
                )

    def eq14_prevent_lonely_base_pairs(self):
        for n in range(len(self.rna_sequence)):
            neirbourghs = []
            middle_pos = [var for pair, var in self.pairing_vars.items()
                          if n in pair]
            middle_pairing = len(middle_pos) - self.model.sum(middle_pos)
            if n > 0:
                left_pos = [var for pair, var in self.pairing_vars.items()
                            if n - 1 in pair]
                neirbourghs.append(len(left_pos) - self.model.sum(left_pos))
            if n < len(self.rna_sequence):
                right_pos = [var for pair, var in self.pairing_vars.items()
                             if n + 1 in pair]
                neirbourghs.append(len(right_pos) - self.model.sum(right_pos))

            self.model.add_constr(self.model.sum(neirbourghs) >= middle_pairing)

    def eq15_maximum_deleted_pair(self):
        sum_bps = self.model.sum(self.canonical_base_pairings.values())
        self.model.add_constr(
            sum_bps <= ceil(self.maximum_percentage_of_deleted_pairs * len(self.canonical_base_pairings)),
        )

    def _calculate_motif_weight_for_alignments(
        self,
        motif_sequence: str,
        i: int,
        j: int,
        alignments: list[str],
    ) -> float:
        # Calculate a weight for a motif depending on how many time it fits into the alignment
        if not alignments:
            return 1
        nb_fits = 0
        for align in alignments:
            if motif_sequence in align[i:j + 1]:
                nb_fits += 1
        return nb_fits / len(alignments)

    def _can_pseudoknot(self, pos: int, pseudoknotable_list: list[bool], i: int, j: int) -> bool:
        # This is true if the position can:
        #   - tag as pseudoknotted, or
        #   - Outside of the strand
        can_pseudoknot = True
        if pos in range(i, j + 1):
            if pseudoknotable_list[pos - i] is False:
                can_pseudoknot = False
        return can_pseudoknot

    def eq_prevent_insertion_on_pseudknot(self):
        for m, motif in enumerate(self.motifs_present):
            for s, strand in enumerate(motif.strands):
                for (i, j), pseudoknotables_list in zip(
                    strand.possible_pairings,
                    strand.insertions_pseudoknotables,
                ):
                    pseudoknot_pairing_vars = []
                    for lvl, var_per_pairings in self.base_pairings_per_lvl.items():
                        if lvl > 0:
                            pairings = StructureHelper.get_pairings_touching_two_positions(
                                var_per_pairings.keys(), i, j,
                            )
                            # Remove pairings at positions that can be pseudoknot in the strand (if available)
                            if self.enable_pseudonotable_motif is True and pseudoknotables_list:
                                filtered_pairing = []
                                for k, l in pairings:
                                    if not all(map(
                                        lambda x: self._can_pseudoknot(x, pseudoknotables_list, i, j), [k, l]),
                                    ):
                                        filtered_pairing.append((k, l))
                            else:
                                filtered_pairing = pairings

                            pseudoknot_pairing_vars.extend(
                                1 - var for pair, var in var_per_pairings.items() if pair in filtered_pairing
                            )
                    if pseudoknot_pairing_vars:
                        self.model.add_constr(
                            sum(pseudoknot_pairing_vars)
                            <= (1 - self.motifs_vars[i, j][m][s]) * len(pseudoknot_pairing_vars),
                        )

    def objective(self):
        motif_score_sum = []
        for m, motif in enumerate(self.motifs_present):
            sum_motif = self.model.sum(
                self.motifs_vars[k, l][m][s] * weight
                for s, strand in enumerate(motif.strands)
                for (k, l), weight in zip(strand.possible_pairings, strand.insertions_weights)
            )
            weight = motif.length ** 2
            motif_score_sum.append(sum_motif * weight)

        sum_motifs_inserted = self.model.sum(motif_score_sum)
        score = 0
        if self.enable_delete_pairings:
            score += self.model.sum(self.canonical_base_pairings.values()) * self.delete_pairings_penalty
        return score - sum_motifs_inserted
