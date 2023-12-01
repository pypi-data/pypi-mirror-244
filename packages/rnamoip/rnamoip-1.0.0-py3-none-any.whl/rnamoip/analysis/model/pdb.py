
from dataclasses import dataclass, field
from .chain import Chain


@dataclass
class PDB:
    name: str
    chains: list[Chain] = field(default_factory=list)
    nr = None

    @property
    def level(self) -> int:
        return len(self.chains)

    @property
    def length(self) -> int:
        return sum([c.length for c in self.chains])
