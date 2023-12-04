
from copy import deepcopy
from dataclasses import asdict, dataclass
from itertools import chain
from typing import Any, Optional

from rnamoip.analysis.comparer import Comparer, InteractionResult
from rnamoip.analysis.comparer_result import ComparerResult
from rnamoip.analysis.pdb_interaction import get_pdb_interaction
from rnamoip.analysis.rin_interaction import get_rins_interactions
from rnamoip.analysis.model.interaction import Interaction


@dataclass
class AnalysisResult:
    pdb_name: str
    chain_name: str
    sequence_original: str
    pdb_ori_structure: str
    initial_structure: str
    rnafold_structure: str
    rnamoip_structure: str
    motifs_structuree: str

    highest_junctions: int
    highest_pseudoknot_lvl: int
    alignments: Optional[list[str]]
    original_motifs: dict
    motifs_inserted: dict[str: list[dict]]
    iteration_count: int
    execution_time_in_sec: int
    solutions_count: int
    solution_score: float
    solution_code: str
    solution_list: list[dict]
    alpha: float
    motif_type: str

    rnamoip_result: ComparerResult = None
    rnafold_result: ComparerResult = None
    rnafold_distance_score: int = None
    rnamoip_distance_score: int = None
    interactions_result: InteractionResult = InteractionResult()

    def __post_init__(self):
        ss_to_compare = [self.rnamoip_structure, self.rnafold_structure]
        scores = Comparer.compare_ss(self.pdb_ori_structure, ss_to_compare)
        self.rnamoip_distance_score, self.rnafold_distance_score = scores
        self.rnamoip_result = Comparer.get_compare_result(
            self.pdb_ori_structure, self.rnamoip_structure, self.motifs_inserted,
        ) if self.rnamoip_result is None else self.rnamoip_result
        self.rnafold_result = Comparer.get_compare_result(
            self.pdb_ori_structure, self.rnafold_structure,
        ) if self.rnafold_result is None else self.rnafold_result

    @staticmethod
    def get_motif_occurences(motifs: dict[list[dict]]) -> dict[list[dict]]:
        # Since motifs can be inserted multiple times, group by complete occurences
        occs = {}
        for motif_id, motif in motifs.items():
            max_strands = max(motif['strands'], key=lambda s: s['strand_id'])['strand_id']
            if len(motif) != max_strands:
                strand_by_strand_id = {}
                for i in range(max_strands + 1):
                    strand_by_strand_id[i] = [s for s in motif['strands'] if s['strand_id'] == i]
                for i in range(len(strand_by_strand_id[0])):
                    occs[(motif_id, i)] = {
                        'name': motif['name'],
                        'related_rins': motif['related_rins'],
                        'strands': [strand_by_strand_id[j][i] for j in range(max_strands + 1)],
                    }
            else:
                occs[(motif_id, 0)] = motif
        return occs

    @staticmethod
    def update_rins_interactions_positions(
        rin_interactions: dict[str, list[list[Interaction]]],
        motif: dict,
    ) -> list[Interaction]:
        '''
            Here is the realisation that we only need one occurence per rin,
            since the rin itself represent all the interactions.
        '''
        motif_interactions_per_rin = {}
        for rin, interactions_list in rin_interactions.items():
            motif_mapping = {}
            seq = motif['name'].replace('-', '').replace('.', '')
            sorted_strands = sorted(motif['strands'], key=lambda a: a['start'])
            pos_list = [list(range(strand['start'], strand['end'] + 1)) for strand in sorted_strands]
            motif_pos_list_in_pdb = list(chain(*pos_list))
            for index, nuc in enumerate(seq):
                if nuc == '.' or nuc == '-':
                    continue
                # Careful, Rin position are 1-based index
                motif_mapping[index + 1] = motif_pos_list_in_pdb[index]

            motif_interactions = interactions_list[0]
            for interaction in motif_interactions:
                interaction.start_pos = motif_mapping[interaction.start_pos]
                interaction.end_pos = motif_mapping[interaction.end_pos]
            motif_interactions_per_rin[rin] = motif_interactions
        return motif_interactions_per_rin

    @classmethod
    def analyse_motifs_interactions(
        cls,
        pdb_name,
        chain_name,
        motifs_inserted,
        rins_data: dict[str, Any],
        pdb_interactions: dict[str, list[Interaction]],
        motifs_count: dict[str, int],
    ) -> InteractionResult:
        interactions_in_motifs = {}
        motifs_occurences = cls.get_motif_occurences(motifs_inserted)
        for occ, motif in motifs_occurences.items():
            # Get RIN interactions in range of motif
            rins_related = [int(mr) for mr in motif['related_rins']]
            rins_interactions = get_rins_interactions(
                rins_related, rins_data,
            )

            rins_interactions = cls.update_rins_interactions_positions(
                deepcopy(rins_interactions),
                motif,
            )

            interactions_in_motifs[occ] = rins_interactions

        if not pdb_interactions:
            pdb_interactions = get_pdb_interaction(pdb_name, chain_name)
        motifs_count['motifs_count_in_pdb'] += len(motifs_occurences.keys())
        interactions_result = Comparer.compare_interactions(
            pdb_interactions,
            motifs_occurences,
            interactions_in_motifs,
        )
        motifs_count['motifs_count_in_pdb_no_canonique'] += interactions_result.motifs_count_without_canonique
        motifs_count['motifs_count_in_pdb_no_non_canonique'] += \
            interactions_result.motifs_count_without_non_canonique
        return interactions_result

    def asdict(self):
        # asdict doesn't seem to like defaultdict...
        self.motifs_inserted = dict(self.motifs_inserted)
        return asdict(self)
