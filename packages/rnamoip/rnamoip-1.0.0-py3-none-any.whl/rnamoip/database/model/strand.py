
from dataclasses import dataclass, field
from .common import Pairing


@dataclass
class Strand:
    sequence: str
    pseudokotable_list: list[bool] = field(default_factory=list)
    insertions_start: list[int] = field(default_factory=list)
    insertions_end: list[int] = field(default_factory=list)
    insertions_pseudoknotables: list[list[bool]] = field(default_factory=list)
    insertions_weights: list[float] = field(default_factory=list)
    insertions_seq: list[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.pseudokotable_list:
            self.pseudokotable_list = [False] * len(self.sequence)
        if not self.insertions_weights:
            self.insertions_weights = [1] * len(self.insertions_start)

    @property
    def length(self):
        return len(self.sequence)

    @property
    def possible_pairings(self) -> list[Pairing]:
        return list(zip(self.insertions_start, self.insertions_end))

    @property
    def possible_pairings_with_seq(self) -> list[tuple[int, int, str]]:
        return list(zip(self.insertions_start, self.insertions_end, self.insertions_seq))
