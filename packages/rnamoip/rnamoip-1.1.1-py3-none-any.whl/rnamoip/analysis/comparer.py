
from dataclasses import dataclass, field
from enum import Enum
from itertools import chain

import RNA
from rnamoip.helpers.sequence import SequenceHelper
from rnamoip.helpers.structure import StructureHelper

from .comparer_result import ComparerResult
from .model.interaction import Interaction


class InteractionType(str, Enum):
    CANONICAL = 'Canonical'
    NON_CANONICAL = 'Non Canonical'

    def abbrev(self):
        if self == self.CANONICAL:
            return 'can'
        elif self == self.NON_CANONICAL:
            return 'non_can'


@dataclass
class InteractionResult:
    interactions_ratio: float = 0
    interactions_ratio_can: float = 0
    interactions_ratio_non_can: float = 0
    generous_interactions_ratio: float = 0
    generous_interactions_ratio_can: float = 0
    generous_interactions_ratio_non_can: float = 0
    interactions_count_of_pdb_in_motifs: int = None
    non_can_count_of_pdb_in_motifs: int = None
    correct_non_can_count_of_motifs: int = None
    can_count_of_pdb_in_motifs: int = None
    correct_can_count_of_motifs: int = None
    motifs_count_without_canonique: int = 0
    motifs_count_without_non_canonique: int = 0
    best_pdb_model: str = None
    best_generous_pdb_model: str = None
    best_occurence_list: list[str] = field(default_factory=list)
    total_pdb_interactions: int = None
    total_motifs_interactions: int = None
    total_motifs_interactions_can: int = None
    total_motifs_interactions_non_can: int = None

    def get_metric(self, metric: str, interaction_type: InteractionType):
        inter_abbrev = interaction_type.abbrev()
        tp = (
            getattr(self, f'{inter_abbrev}_count_of_pdb_in_motifs')
            * getattr(self, f'interactions_ratio_{inter_abbrev}')
        )
        tp = round(tp, 1)
        fp = getattr(self, f'{inter_abbrev}_count_of_pdb_in_motifs') - tp
        fn = getattr(self, f'total_motifs_interactions_{inter_abbrev}') - tp

        comparer_results = ComparerResult(tp, fp, fn)
        if metric == 'PPV':
            return comparer_results.PPV
        elif metric == 'Sensitivity':
            return comparer_results.sensitivity
        elif metric == 'F1 Score':
            return comparer_results.f1_score
        else:
            raise Exception('Unknown metric')


@dataclass
class MotifResult:
    correct_count: int = 0
    gen_correct_count: int = 0
    total_pdb_count: int = 0
    total_motifs_count: int = 0
    current_motifs_total: int = 0
    current_best: int = 0
    current_total: int = 0

    @staticmethod
    def divide_or_zero(a, b):
        return a / b if b else 0

    def reinitialize_current(self):
        self.current_best = 0
        self.current_motifs_total = 0

    def interaction_ratio(self):
        return self.divide_or_zero(self.correct_count, self.total_pdb_count)

    def generous_interaction_ratio(self):
        return self.divide_or_zero(self.gen_correct_count, self.total_pdb_count)

    def update_total(self):
        self.total_pdb_count += self.current_total
        self.correct_count += self.current_best
        self.total_motifs_count += self.current_motifs_total


@dataclass
class MotifResults:
    all: MotifResult = field(default_factory=MotifResult)
    can: MotifResult = field(default_factory=MotifResult)
    non_can: MotifResult = field(default_factory=MotifResult)
    current_best_occ: str = None
    best_occurence_list: list[str] = field(default_factory=list)
    motifs_count_without_canonique: int = 0
    motifs_count_without_non_canonique: int = 0

    def reinitialise_current_best(self):
        self.current_best_occ = None
        self.all.reinitialize_current()
        self.can.reinitialize_current()
        self.non_can.reinitialize_current()

    def update_total(self):
        self.all.update_total()
        self.can.update_total()
        self.non_can.update_total()
        self.best_occurence_list.append(self.current_best_occ)
        if self.can.current_total == 0:
            self.motifs_count_without_canonique += 1
        if self.non_can.current_total == 0:
            self.motifs_count_without_non_canonique += 1


class Comparer:
    @staticmethod
    def compare_ss(original: str, ss_list: list[str]) -> list[int]:
        return [
            RNA.bp_distance(original, ss)
            for ss in ss_list
        ]

    @staticmethod
    def get_compare_result(
        real_ss: str,
        secondary_structure: str,
        motifs_inserted: list[dict] = None,
    ) -> ComparerResult:
        real_pairings_per_lvl, _ = StructureHelper.find_base_pairings_with_level(real_ss)
        output_pairings_per_lvl, _ = StructureHelper.find_base_pairings_with_level(secondary_structure, 6)

        real_pairings = set(bp for bp_list in real_pairings_per_lvl.values() for bp in bp_list)
        output_pairings = set(bp for bp_list in output_pairings_per_lvl.values() for bp in bp_list)

        # If we have missing pairings, it might be because we inserted them into a motif
        # In that case, we can count them as well predicted
        if motifs_inserted:
            strands_list = list(chain(*[mi['strands'] for mi in motifs_inserted.values()]))
            missing_pairings = real_pairings - output_pairings
            pairings_save = set()
            for a, b in missing_pairings:
                motif_a = SequenceHelper.get_motif_name(a, strands_list)
                motif_b = SequenceHelper.get_motif_name(b, strands_list)

                if motif_a and motif_b and motif_a == motif_b:
                    pairings_save.add((a, b))

            output_pairings = output_pairings | pairings_save
        true_positives = output_pairings & real_pairings
        false_positives = output_pairings - real_pairings
        false_negatives = real_pairings - output_pairings

        return ComparerResult(
            true_positives=len(true_positives),
            false_positives=len(false_positives),
            false_negatives=len(false_negatives),
        )

    @staticmethod
    def compare_generous_motifs_interactions(
        pdb_interactions: list[Interaction],
        motif_interactions_list: list[list[Interaction]],
        motif_results: MotifResults,
    ):
        # Generous case
        matches = 0
        matches_can = 0
        matches_non_can = 0
        motif_interactions = list(chain(*motif_interactions_list))
        for pdb_interaction in pdb_interactions:
            for interaction in motif_interactions:
                if interaction == pdb_interaction:
                    matches += 1
                    if pdb_interaction.is_canonical:
                        matches_can += 1
                    else:
                        matches_non_can += 1
                    break
        motif_results.all.gen_correct_count += matches
        motif_results.can.gen_correct_count += matches_can
        motif_results.non_can.gen_correct_count += matches_non_can

    @staticmethod
    def compare_motif_interactions(
        pdb_interactions: list[Interaction],
        motif_interactions_per_occ: dict[str, list[Interaction]],
        motif_results: MotifResults,
        motif_occurence: tuple[str, str],
    ):
        motif_results.all.current_total = len(pdb_interactions)
        motif_results.can.current_total = len([
            inter for inter in pdb_interactions if inter.is_canonical
        ])
        motif_results.non_can.current_total = len([
            inter for inter in pdb_interactions if not inter.is_canonical
        ])
        for occ, interactions in motif_interactions_per_occ.items():
            matches = 0
            matches_can = 0
            matches_non_can = 0
            for interaction in interactions:
                for pdb_interaction in pdb_interactions:
                    if interaction == pdb_interaction:
                        matches += 1
                        if pdb_interaction.is_canonical:
                            matches_can += 1
                        else:
                            matches_non_can += 1
            if matches >= motif_results.all.current_best:
                motif_results.all.current_best = matches
                motif_results.can.current_best = matches_can
                motif_results.non_can.current_best = matches_non_can
                motif_results.current_best_occ = motif_occurence, occ
                motif_results.all.current_motifs_total = len(interactions)
                motif_results.can.current_motifs_total = len([
                    inter for inter in interactions if inter.is_canonical
                ])
                motif_results.non_can.current_motifs_total = len([
                    inter for inter in interactions if not inter.is_canonical
                ])

        motif_results.update_total()

    @classmethod
    def compare_interactions(
        cls,
        interactions_per_pdb_model: dict[str, list[Interaction]],
        motifs_occurences: dict[str, list],
        motifs_interactions: dict[str, list[Interaction]],
    ):
        result: InteractionResult = InteractionResult()
        for model_index, pdb_interactions in interactions_per_pdb_model.items():
            interactions_ratio = 0
            interactions_ratio_can = 0
            interactions_ratio_non_can = 0
            generous_interactions_ratio = 0
            generous_interactions_ratio_can = 0
            generous_interactions_ratio_non_can = 0
            motif_results = MotifResults()
            for motif_occurence, motif in motifs_occurences.items():
                # Find motif range
                sorted_strands = sorted(motif['strands'], key=lambda a: a['start'])
                pos_list = [list(range(strand['start'], strand['end'] + 1)) for strand in sorted_strands]
                motif_pos_list_in_pdb = list(chain(*pos_list))
                # Look for the best ratio
                motif_results.reinitialise_current_best()

                ranged_interactions_in_pdb = [
                    inter for inter in pdb_interactions
                    if inter.start_pos in motif_pos_list_in_pdb and inter.end_pos in motif_pos_list_in_pdb
                ]

                # Retrieve occurences list
                motifs_interactions_per_occ = motifs_interactions[motif_occurence]
                cls.compare_motif_interactions(
                    ranged_interactions_in_pdb,
                    motifs_interactions_per_occ,
                    motif_results,
                    motif_occurence,
                )
                cls.compare_generous_motifs_interactions(
                    ranged_interactions_in_pdb,
                    motifs_interactions_per_occ.values(),
                    motif_results,
                )

            interactions_ratio = motif_results.all.interaction_ratio()
            interactions_ratio_can = motif_results.can.interaction_ratio()
            interactions_ratio_non_can = motif_results.non_can.interaction_ratio()
            generous_interactions_ratio = motif_results.all.generous_interaction_ratio()
            generous_interactions_ratio_can = motif_results.can.generous_interaction_ratio()
            generous_interactions_ratio_non_can = motif_results.non_can.generous_interaction_ratio()

            # Failsafe if there are not initialize
            if result.interactions_count_of_pdb_in_motifs is None:
                result.interactions_count_of_pdb_in_motifs = motif_results.all.total_pdb_count
                result.non_can_count_of_pdb_in_motifs = motif_results.non_can.total_pdb_count
                result.correct_non_can_count_of_motifs = motif_results.non_can.correct_count
                result.can_count_of_pdb_in_motifs = motif_results.can.total_pdb_count
                result.correct_can_count_of_motifs = motif_results.can.correct_count
                result.motifs_count_without_canonique = motif_results.motifs_count_without_canonique
                result.motifs_count_without_non_canonique = motif_results.motifs_count_without_non_canonique
                result.total_motifs_interactions = motif_results.all.total_motifs_count
                result.total_motifs_interactions_can = motif_results.can.total_motifs_count
                result.total_motifs_interactions_non_can = motif_results.non_can.total_motifs_count
            if result.total_pdb_interactions is None:
                result.total_pdb_interactions = len(pdb_interactions)

            # Overwrite if it's a better ratio
            if interactions_ratio > result.interactions_ratio:
                result.interactions_ratio = interactions_ratio
                result.interactions_ratio_can = interactions_ratio_can
                result.interactions_ratio_non_can = interactions_ratio_non_can
                result.best_pdb_model = model_index
                result.best_occurence_list = motif_results.best_occurence_list
                result.total_pdb_interactions = len(pdb_interactions)
                result.interactions_count_of_pdb_in_motifs = motif_results.all.total_pdb_count
                result.non_can_count_of_pdb_in_motifs = motif_results.non_can.total_pdb_count
                result.correct_non_can_count_of_motifs = motif_results.non_can.correct_count
                result.can_count_of_pdb_in_motifs = motif_results.can.total_pdb_count
                result.correct_can_count_of_motifs = motif_results.can.correct_count
                result.motifs_count_without_canonique = motif_results.motifs_count_without_canonique
                result.motifs_count_without_non_canonique = motif_results.motifs_count_without_non_canonique
                result.total_motifs_interactions = motif_results.all.total_motifs_count
                result.total_motifs_interactions_can = motif_results.can.total_motifs_count
                result.total_motifs_interactions_non_can = motif_results.non_can.total_motifs_count

            if generous_interactions_ratio > result.generous_interactions_ratio:
                result.generous_interactions_ratio = generous_interactions_ratio
                result.generous_interactions_ratio_can = generous_interactions_ratio_can
                result.generous_interactions_ratio_non_can = generous_interactions_ratio_non_can
                result.best_generous_pdb_model = model_index

        return result
