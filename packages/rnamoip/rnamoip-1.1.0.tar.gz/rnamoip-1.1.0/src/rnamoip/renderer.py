
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from colorama import init, Back, Fore, Style


@dataclass
class Result:
    sequence: str
    initial_structure: str
    new_structure: str
    motifs: dict[str: list[dict]]
    sequence_by_motifs: dict[int: Any]
    iterations_count: int
    execution_time_in_sec: int
    solutions_count: int
    solution_score: float
    solution_code: str
    motif_type: str
    alpha: float
    structures: list[str] = field(init=False)
    solutions_list: list = field(default_factory=list)

    @property
    def motif_sequence(self) -> str:
        index_by_motif = {}
        for index, motif in enumerate(self.motifs.values()):
            index_by_motif[motif['name']] = chr(ord('a') + index)
        sequence = []
        for i in range(len(self.initial_structure)):
            if i in self.sequence_by_motifs.keys():
                sequence.append(index_by_motif[self.sequence_by_motifs[i]])
            else:
                sequence.append('.')
        return ''.join(sequence)


class MotifColor(Enum):
    GREEN = 0
    BLUE = 1
    YELLOW = 2
    MAGENTA = 3
    CYAN = 4
    RED = 5
    WHITE = 6

    def to_color(self):
        if self.value == self.GREEN.value:
            return Back.GREEN
        elif self.value == self.YELLOW.value:
            return Back.YELLOW
        elif self.value == self.BLUE.value:
            return Back.BLUE
        elif self.value == self.MAGENTA.value:
            return Back.MAGENTA
        elif self.value == self.CYAN.value:
            return Back.CYAN
        elif self.value == self.RED.value:
            return Back.RED
        elif self.value == self.WHITE.value:
            return Back.WHITE


class StdRenderer:
    @staticmethod
    def render(result: Result):
        init()
        structure = []
        for i, (a, b) in enumerate(zip(result.initial_structure, result.new_structure)):
            s = ''
            if a != b:
                s += f'{Back.RED}'
            else:
                s += f'{Back.BLACK}'
            structure.append(s + b)
        structure.append(f'{Style.RESET_ALL}')
        print(''.join(structure))

        # Print motifs
        structure = []
        motif_color = MotifColor.GREEN
        current_motif = ''
        motifs_by_color = {}
        for i, (a, b) in enumerate(zip(result.initial_structure, result.new_structure)):
            s = ''
            if i in result.sequence_by_motifs:
                current_motif = result.sequence_by_motifs[i]
                if not result.sequence_by_motifs[i] in motifs_by_color:
                    motifs_by_color[current_motif] = motif_color.to_color()
                    motif_color = MotifColor((motif_color.value + 1) % (MotifColor.WHITE.value + 1))
                s += f'{motifs_by_color[current_motif]}'
                structure.append(f'{s}{Fore.BLACK}{b}')
            else:
                s += f'{Back.BLACK}'
                structure.append(f'{s}{Fore.WHITE}{b}')
        structure.append(f'{Style.RESET_ALL}')

        for motif_id, motif in dict(sorted(result.motifs.items(), key=lambda x: x[0])).items():
            name = motif['name']
            for strand in motif['strands']:
                seq = strand['seq']
                strand_id = strand['strand_id']
                start = strand['start']
                end = strand['end']
                color = motifs_by_color.get(name, MotifColor.RED.value)
                strand_info = ', '.join([name, seq, f'{start}-{end}', f'Strand#{strand_id}'])
                print(f'{color}{Fore.BLACK}{motif_id}: {strand_info} {Style.RESET_ALL} ')
        print(''.join(structure))
