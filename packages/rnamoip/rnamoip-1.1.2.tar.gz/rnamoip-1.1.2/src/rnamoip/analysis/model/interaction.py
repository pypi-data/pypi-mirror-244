
from dataclasses import dataclass
from rnamoip.helpers.sequence import SequenceHelper


@dataclass
class Interaction:
    start_pos: int
    end_pos: int
    start_nuc: str
    end_nuc: str
    type: str
    type2: str
    motif_from: str = None
    start_strand: int = 0
    end_strand: int = 0
    model: str = None
    pdb: str = None
    chain: str = None

    @property
    def is_canonical(self) -> bool:
        # TODO: Verify Canonical definition
        return SequenceHelper.is_canonical((self.start_nuc, self.end_nuc))

    @property
    def reverse_type(self) -> str:
        return ''.join([self.type[0], self.type[2], self.type[1]])

    def __eq__(self, __o: object) -> bool:
        return (
            self.start_pos == __o.start_pos
            and self.end_pos == __o.end_pos
            and self.type == __o.type
        ) or (
            self.end_pos == __o.start_pos
            and self.start_pos == __o.end_pos
            and self.reverse_type == __o.type
        )
