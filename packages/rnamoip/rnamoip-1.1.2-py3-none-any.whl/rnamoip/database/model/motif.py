
from dataclasses import dataclass, field
from functools import cached_property

from .strand import Strand


@dataclass
class Motif:
    strands: list[Strand]
    name: str
    related_ids: list[str] = field(default_factory=list)

    @property
    def level(self) -> int:
        return len(self.strands)

    @property
    def length(self) -> int:
        return sum([s.length for s in self.strands])

    @cached_property
    def pdb_name(self) -> str:
        split_list = self.name.split('.')
        if len(split_list) <= 1:
            return self.name
        return split_list[0]

    @cached_property
    def chain_name(self) -> str:
        split_list = self.name.split('.')
        if len(split_list) <= 1:
            return self.name
        return split_list[1]

    @cached_property
    def full_name(self) -> str:
        return f'{self.pdb_name}-{self.chain_name}'
