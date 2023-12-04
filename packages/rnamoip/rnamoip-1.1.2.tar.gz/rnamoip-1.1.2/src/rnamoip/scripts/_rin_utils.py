
import os
from collections import defaultdict, namedtuple
from dataclasses import asdict, dataclass, field
from typing import Optional

import cloudpickle

Position = namedtuple('Position', ['chain_name', 'pos'])


class RinPickler:
    data_path = 'data/rin'
    local_rins_filename = f'{data_path}/2022-07-02_RINLocal_000398_00012676.nxpickled'
    carnaval2_filename = f'{data_path}/carnaval2_preprocessed_data_2022-07-02.pickle'

    @staticmethod
    def unpickle(filename):
        with open(filename, 'rb') as pickle_file:
            data = cloudpickle.load(pickle_file)
        return data

    @staticmethod
    def pickle_to_file(filename, data):
        with open(os.path.join(RinPickler.data_path, filename), 'wb') as pickle_file:
            cloudpickle.dump(data, pickle_file)


@dataclass
class Occurence:
    pdb: str
    chain_name: Optional[str]
    rin_id: int
    sequence: str
    occ_positions: list[Position] = field(default_factory=list)
    occ_mapping: dict[int, Position] = field(default_factory=dict)


@dataclass
class PDB:
    pdb: str
    chain_name: str
    sequence: str

    def to_dict(self):
        return asdict(self)


@dataclass
class RINHolder:
    rin_id: int
    repr: tuple[str, list[int]]
    occ_by_sequence: dict[str, list[Occurence]] = field(default_factory=dict)
    pseudoknotable_pos_list: list[bool] = field(init=False)

    def __post_init__(self):
        self.occ_by_sequence = defaultdict(list)


@dataclass
class SeqsHolder:
    pseudoknotable_pos_list: list[bool] = field(default_factory=list)
    occurences: list[Occurence] = field(default_factory=list)

    def to_dict(self):
        return asdict(self)
