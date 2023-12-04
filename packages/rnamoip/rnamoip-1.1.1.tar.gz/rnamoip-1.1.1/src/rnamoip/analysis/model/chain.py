
import logging
from dataclasses import dataclass, field
from enum import Enum
from functools import cached_property
from typing import Union

import forgi.graph.bulge_graph as fgb
import RNA

from rnamoip import logger
from rnamoip.database.model.common import Pairing
from rnamoip.helpers.structure import StructureHelper


class MotifType(Enum):
    STEM = 's'
    INTERIOR_LOOP = 'i'
    MULTI_LOOP = 'm'
    HAIRPIN = 'h'


@dataclass
class Chain:
    name: str
    pdb_name: str
    sequence: str
    bps: list[Pairing] = field(default_factory=list)
    inital_ss: str = None

    def __post_init__(self):
        pairings_per_lvl, secondary_structure = StructureHelper.pairings_to_str(self.bps, len(self.sequence))
        new_pairings = StructureHelper.remove_lonely_pairings_with_lvl(pairings_per_lvl)
        self._pairings_per_lvl = new_pairings
        self._secondary_structure = StructureHelper.pairings_per_lvl_to_str(new_pairings, self.length)

    @property
    def length(self) -> int:
        return len(self.sequence)

    @property
    def secondary_structure(self) -> str:
        return self._secondary_structure

    @property
    def full_name(self) -> str:
        return f'{self.pdb_name}-{self.name}'

    @property
    def pairings_per_lvl(self) -> dict[int, list[Pairing]]:
        return self._pairings_per_lvl

    @cached_property
    def motifs_list(self) -> dict[str, list[str]]:
        motifs = {mt.value: [] for mt in MotifType}
        if not self.pairings_per_lvl or not self.pairings_per_lvl[0]:
            return motifs
        _, lvl0_ss = StructureHelper.pairings_to_str(self.pairings_per_lvl[0], len(self.sequence))

        log = logger.get_logger()
        log.setLevel(logging.ERROR)
        bg = fgb.BulgeGraph.from_dotbracket(lvl0_ss, seq=self.sequence)
        log.setLevel(logging.INFO)

        multiloops = []
        for junction in bg.junctions:
            for m in junction:
                if m[0] != MotifType.MULTI_LOOP.value:
                    break
            else:
                multiloops.append([bg.defines[m] for m in junction])

        motifs[MotifType.MULTI_LOOP.value] = multiloops
        for motif, pairing in bg.defines.items():
            for mt in [mt for mt in MotifType if mt != MotifType.MULTI_LOOP]:
                if motif[0] == mt.value:
                    motifs[mt.value].append(pairing)
                    break
        return motifs

    @cached_property
    def hairpins_count(self) -> int:
        return len(self.motifs_list[MotifType.HAIRPIN.value])

    @cached_property
    def biggest_multiloop(self) -> int:
        return max((len(loop) for loop in self.motifs_list[MotifType.MULTI_LOOP.value]), default=0)

    @cached_property
    def highest_pseudoknot_lvl(self) -> bool:
        return max(self.pairings_per_lvl.keys(), default=0)

    def rnafold_ss(self, sequence: Union[list[str], str]) -> str:
        fc = RNA.fold_compound(sequence)
        (ss, mfe) = fc.mfe()
        return ss
