import logging
from pathlib import Path
from typing import Optional

from .model.common import Pairing
from .model.motif import Motif
from ..helpers.base_pairing import BasePairingProbaHelper
from ..helpers.parser.desc import DescParser
from ..helpers.parser.rin import RinParser
from ..helpers.sequence import SequenceHelper
from ..helpers.structure import StructureHelper


class Catalog:
    _folder_path: Path
    _rna_sequence: str
    _secondary_structure: str
    _alignment: list[str]
    _minimum_probability: float
    _minimum_pairing_distance: int
    _maximum_pairing_level: int
    _minimum_alignment_match_threshold: float
    _maximum_alignment_distance: int

    _motifs: list[Motif]
    _motifs_present: list[Motif]
    _base_pairings: list[Pairing]
    _base_pairings_per_level: dict[int, list[Pairing]]
    _structure_per_level: dict[int, str]
    _base_pairings_proba: dict[Pairing, float]
    _pdb_name: Optional[str]
    _pdbs_to_ignore: list[str]
    _parser: str
    _motifs: dict

    def __init__(
        self,
        folder_path: Path,
        rna_sequence: str,
        alignment: list[str],
        secondary_structure: str,
        minimum_probability: float,
        minimum_pairing_distance: int,
        maximum_pairing_level: int,
        minimum_alignment_match_threshold: float,
        maximum_alignment_distance: int,
        pdb_name: Optional[str],
        pdbs_to_ignore: list[str],
        parser: str,
        motifs_present: Optional[list[Motif]],
        motifs: dict = None,
    ) -> None:
        self._folder_path = folder_path
        self._rna_sequence = rna_sequence
        self._alignment = alignment
        self._secondary_structure = secondary_structure
        self._minimum_probability = minimum_probability
        self._minimum_pairing_distance = minimum_pairing_distance
        self._maximum_pairing_level = maximum_pairing_level
        self._minimum_alignment_match_threshold = minimum_alignment_match_threshold
        self._maximum_alignment_distance = maximum_alignment_distance
        self._pdb_name = pdb_name
        self._pdbs_to_ignore = pdbs_to_ignore
        self._parser = parser
        self._motifs = motifs

        self.init_catalog(motifs_present)

    @property
    def rna_sequence(self):
        return self._rna_sequence

    @property
    def alignment(self):
        return self._alignment

    @property
    def secondary_structure(self):
        return self._secondary_structure

    @property
    def motifs_present(self):
        return self._motifs_present

    @property
    def base_pairings(self):
        return self._base_pairings

    @property
    def base_pairings_per_level(self):
        return self._base_pairings_per_level

    @property
    def base_pairings_proba(self):
        return self._base_pairings_proba

    def init_catalog(self, motifs_present: Optional[list[Motif]]):
        """
        Parse all the motifs files in the folder, and store them into the class list.
        """
        if motifs_present is None:
            if self._motifs is None:
                if self._parser == 'desc':
                    self._motifs = DescParser.parse_folder(self._folder_path)

                    # Remove motifs that correspond to the pdb we are analysing, if any was passed.
                    if self._pdbs_to_ignore:
                        self.filter_pdb_motifs()
                elif self._parser == 'rin':
                    self._motifs = RinParser.parse_folder(self._folder_path)
                else:
                    raise Exception(f"Invalid Parser defined '{self._parser}'.")

            # Create a list of matching motifs in sequence.
            self._motifs_present = self.match_by_nucleotide()
        else:
            self._motifs_present = motifs_present
        self._base_pairings_per_level, self._structure_per_level = \
            StructureHelper.find_base_pairings_with_level(self._secondary_structure, self._maximum_pairing_level)
        self._base_pairings = self._base_pairings_per_level[0]

        sequence = self.alignment if self.alignment else self.rna_sequence
        self._base_pairings_proba = BasePairingProbaHelper.get_base_pairings_proba_with_lvl(
            sequence,
            self._structure_per_level,
            self._minimum_probability,
            self._minimum_pairing_distance,
        )

        logging.debug(f"Motifs that can be inserted: {len(self._motifs_present)}")

    def filter_pdb_motifs(self):
        self._motifs = [
            motif for motif in self._motifs
            if motif.full_name not in self._pdbs_to_ignore
            and motif.pdb_name not in self._pdbs_to_ignore
        ]

    def motif_present_per_level(self, level: int) -> list[tuple[int, Motif]]:
        return [(index, motif) for index, motif in enumerate(self._motifs_present) if motif.level == level]

    def match_by_nucleotide(self) -> list[Motif]:
        motifs_present = []
        for motif in self._motifs:
            for strand in motif.strands:
                if self.alignment:
                    alignments_without_gap = [
                        alignment.replace('-', '').upper() for alignment in self.alignment
                    ]
                    result = SequenceHelper.get_possible_insertions_of_alignement(
                        strand,
                        self.rna_sequence,
                        alignments_without_gap,
                        self._minimum_pairing_distance,
                        self._minimum_alignment_match_threshold,
                        self._maximum_alignment_distance,
                    )
                else:
                    result = SequenceHelper.get_possible_insertions_of_sequence(
                        strand, self.rna_sequence, self._minimum_pairing_distance,
                    )
                if len(result.starts) == 0 or len(result.ends) == 0:
                    break
                strand.insertions_start = result.starts
                strand.insertions_end = result.ends
                strand.insertions_pseudoknotables = result.pseudoknotables_list
                strand.insertions_weights = result.weights
                strand.insertions_seq = result.seqs
            else:
                motifs_present.append(motif)
        return motifs_present
