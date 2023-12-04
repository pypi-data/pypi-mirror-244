
import logging
import re
from collections import defaultdict
from itertools import count
from operator import xor

from ..database.model.common import Pairing

from .sequence import SequenceHelper


class StructureHelper:
    PAIRING_LEFT_CHAR = '([{<ABC'
    PAIRING_RIGHT_CHAR = ')]}>abc'

    @staticmethod
    def get_pairing_level_of(structure: str) -> int:
        pairings = ''.join(['.', StructureHelper.PAIRING_LEFT_CHAR])
        for i, p in zip(count(len(pairings) - 1, -1), reversed(pairings)):
            if p in structure:
                return i
        return 0

    @staticmethod
    def pairings_to_str(pairings: list[Pairing], length: int) -> tuple[dict[int, list], str]:
        structure = []
        pairings_per_lvl = defaultdict(list)
        nuc_by_lvl = StructureHelper.get_lvl_from_pairings(pairings, length)
        righties = {}
        for i in range(length):
            if i in righties.keys():
                pair_lvl = righties[i]
                structure.append(StructureHelper.PAIRING_RIGHT_CHAR[pair_lvl])
                righties.pop(i)
                continue
            pairs = [pair for pair in pairings if i in pair]
            if len(pairs) == 0:
                structure.append(SequenceHelper.ANY_NUCLEOTIDE)
                continue
            pair = pairs[0]
            pair_lvl = nuc_by_lvl[pair[0]]
            righties[pair[1]] = pair_lvl
            pairings_per_lvl[pair_lvl].append(pair)
            structure.append(StructureHelper.PAIRING_LEFT_CHAR[pair_lvl])
        return pairings_per_lvl, ''.join(structure)

    @staticmethod
    def pairings_per_lvl_to_str(pairings_per_lvl: dict[int, list[Pairing]], length: int) -> str:
        structure = []
        for i in range(length):
            for lvl, pairings in pairings_per_lvl.items():
                has_append = False
                for (k, l) in pairings:
                    if i == k:
                        structure.append(StructureHelper.PAIRING_LEFT_CHAR[lvl])
                        has_append = True
                        break
                    if i == l:
                        structure.append(StructureHelper.PAIRING_RIGHT_CHAR[lvl])
                        has_append = True
                        break
                if has_append:
                    break
            else:
                structure.append('.')
        return ''.join(structure)

    @staticmethod
    def _find_base_pairings(secondary_structure: str) -> list[Pairing]:
        pairings = []
        left_pair = []
        for i, c in enumerate(secondary_structure):
            if c == '(':
                left_pair.append(i)
            elif c == ')':
                if len(left_pair) == 0:
                    raise Exception(f"""
                        The secondary structure is invalid, its missing an opening parenthesis
                        to match with position {i}.
                    """)
                index = left_pair.pop()
                pairings.append((index, i))
        if len(left_pair) != 0:
            raise Exception(f"""
                The secondary structure is invalid, its missing a closing parenthesis
                to match with position {left_pair[0]}.
            """)
        pairings.sort(key=lambda x: x[0])
        return pairings

    @staticmethod
    def find_base_pairings_with_level(
        secondary_structure: str,
        maximum_pairing_level: int = 3,
    ) -> tuple[dict[int, list[Pairing]], dict[int, str]]:
        pairings_per_level = {lvl: [] for lvl in range(maximum_pairing_level)}
        struct_per_level = {0: '.' * len(secondary_structure)}

        for level in range(maximum_pairing_level):
            left_limit = StructureHelper.PAIRING_LEFT_CHAR[level]
            right_limit = StructureHelper.PAIRING_RIGHT_CHAR[level]

            # Escape if lvl < 4
            left_limit = fr'\{left_limit}' if level < 4 else fr'{left_limit}'
            right_limit = fr'\{right_limit}' if level < 4 else fr'{right_limit}'

            # Replace all pairings from other level for unpairable position.
            reg_list = '|'.join([r'\.', left_limit, right_limit])
            reg = fr'[^{reg_list}]'
            level_struct = re.sub(reg, 'x', secondary_structure)
            if level != 0:
                level_struct = re.sub(left_limit, '(', level_struct)
                level_struct = re.sub(right_limit, ')', level_struct)
            pairings_per_level[level] = StructureHelper._find_base_pairings(level_struct)
            struct_per_level[level] = level_struct

        # Validate that the level two pairings crossed at least one pair in the sub level
        for lvl, pairings in pairings_per_level.items():
            if lvl != 0 and pairings_per_level.get(lvl - 1) is not None and not all(map(
                lambda pair: StructureHelper.get_pairings_crossing_two_positions(
                    pairings_per_level[lvl - 1], pair[0], pair[1]),
                pairings,
            )):
                logging.warning(f"""
                    Warning with secondary structure '{secondary_structure}'.
                    Some pairings in pseudoknot are invalid, since the level '{lvl}' has pairs not
                    crossing anything in sub-level '{lvl - 1}'.
                """)
                continue
            if lvl > maximum_pairing_level:
                raise Exception(f"""
                    Error with secondary structure '{secondary_structure}'.
                    Configuration error: The crossing level of the pairing found in the secondary structure is
                    higher than the maximum pairing level '{lvl}' specified.
                """)

        return pairings_per_level, struct_per_level

    @staticmethod
    def get_pairings_crossing_two_positions(
        pairings: list[Pairing],
        start: int,
        end: int,
    ) -> list[Pairing]:
        """ Return the pairings that are only partialy inside the two speficy position."""
        return list(filter(lambda p: xor((start < p[0] < end),
                                         (start < p[1] < end)), pairings))

    @staticmethod
    def get_pairings_touching_two_positions(
        pairings: list[Pairing],
        start: int,
        end: int,
    ) -> list[Pairing]:
        """ Return the pairings that are only partialy inside the two speficy position."""
        return list(filter(lambda p: (start <= p[0] <= end) or (start <= p[1] <= end), pairings))

    @staticmethod
    def get_pairings_inside_two_positions(pairings: list[Pairing],
                                          start: int,
                                          end: int) -> list[Pairing]:
        """ Return the pairings that are completly inside the two speficy position. """
        return list(filter(
            lambda p: (start <= p[0] <= end) and (start <= p[1] <= end),
            pairings,
        ))

    @staticmethod
    def get_pairings_stack_on_two_positions(pairings: list[Pairing],
                                            start: int,
                                            end: int) -> list[Pairing]:
        """ Return the pairings that are stack on two positions. """
        return list(filter(
            lambda p: (start - 1 <= p[0] <= start) and (end <= p[1] <= end + 1),
            pairings,
        ))

    @staticmethod
    def remove_lonely_pairings(pairings: list[Pairing]) -> list[Pairing]:
        # Remove lonely pairings
        lefties = [i for (i, _) in pairings]
        righties = [j for (_, j) in pairings]
        bps_to_remove = []
        for (i, j) in pairings:
            alone_left = i - 1 not in lefties and i + 1 not in lefties
            alone_right = j - 1 not in righties and j + 1 not in righties
            if alone_left or alone_right:
                bps_to_remove.append((i, j))

        if bps_to_remove:
            filtered_pairings = [pair for pair in pairings if pair not in bps_to_remove]
            return StructureHelper.remove_lonely_pairings(filtered_pairings)
        return pairings

    @staticmethod
    def remove_lonely_pairings_with_lvl(
        pairings_per_lvl: dict[int, list[Pairing]],
    ) -> dict[int, list[Pairing]]:
        new_pairings = {}
        for lvl, pairings in pairings_per_lvl.items():
            new_pairings[lvl] = StructureHelper.remove_lonely_pairings(pairings)
        return new_pairings

    @staticmethod
    def get_pair_table_from_pairings(pairings: list[Pairing], length: int) -> list[int]:
        pair_table = [-1] * length
        for i in range(length):
            for pair in pairings:
                if pair[0] == i:
                    pair_table[i] = pair[1]
                    break
                elif pair[1] == i:
                    pair_table[i] = pair[0]
                    break
        return pair_table

    @staticmethod
    def get_lvl_from_pairings(pairings: list[Pairing], length: int) -> list[int]:
        pair_table = StructureHelper.get_pair_table_from_pairings(pairings, length)
        crossing_list: list[list[int]] = [[] for _ in range(length)]
        # make an adjacent graph, in which pseudoknotted base-pairs are connected.
        for i, j in enumerate(pair_table):
            if j < 0 or j <= i:
                continue
            for k, l in enumerate(pair_table[i + 1:], i + 1):
                if l < 0 or l <= k:
                    continue
                if k < j and j < l:
                    crossing_list[i].append(k)
                    crossing_list[k].append(i)

        # vertices are indexed by the position of the left base
        vertices: list = []
        for i, j in enumerate(pair_table):
            if j >= 0 and i < j:
                vertices.append(i)

        # sort vertices by degree
        vertices = sorted(vertices, key=lambda x: len(crossing_list[x]))

        # determine colors
        color_list = [-1] * length
        max_color = 0

        for i, vertice in enumerate(vertices):
            # find the smallest color that is unused. Set will ensure the lsit is unique
            used: set = set()
            for j, crossed in enumerate(crossing_list[vertice]):
                if color_list[crossed] >= 0:
                    used.add(color_list[crossed])
            used = sorted(used)
            index = 0
            for c in used:
                if index != c:
                    break
                index += 1
            color_list[vertice] = index
            max_color = max(max_color, index)

        # renumber colors in decentant order by the number of base-pairs for each color
        count_color: list = [0] * (max_color + 1)
        for c in color_list:
            if c >= 0:
                count_color[c] += 1

        # Create an index list to assigne base on the sorted count
        index_colors = range(len(count_color))
        sorted_colors_index = sorted(index_colors, key=lambda x: count_color[x], reverse=True)

        nuc_by_level: list = [-1] * length
        for i, color in enumerate(color_list):
            nuc_by_level[i] = sorted_colors_index[color] if color >= 0 else -1
        return nuc_by_level
