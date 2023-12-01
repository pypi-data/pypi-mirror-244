
from itertools import chain
import logging
import re
from dataclasses import dataclass, field
from typing import Optional, Union

from rnamoip.database.model.common import Pairing
from rnamoip.database.model.strand import Strand

DEFAULT_WILDCARD_THRESHOLD = 1.0 / 3.0


class IUPACConverter:
    POSSIBLE_VALUES = 'ACGURYSWKMBDHVXN.-'
    A = 'A'
    C = 'C'
    G = 'G'
    U = 'U'
    R = 'R'  # A or G
    Y = 'Y'  # C or U
    S = 'S'  # G or C
    W = 'W'  # A or U
    K = 'K'  # G or U
    M = 'M'  # A or C
    B = 'B'  # C or G or U
    D = 'D'  # A or G or U
    H = 'H'  # A or C or U
    V = 'V'  # A or C or G
    N = 'N'  # any base
    X = 'X'  # any base
    DOT = '.'  # any base
    GAP = '-'  # gap

    @classmethod
    def to_possible_out(cls, nuc: str) -> str:
        if nuc == cls.A:
            return '.A'
        if nuc == cls.C:
            return '.C'
        if nuc == cls.G:
            return '.G'
        if nuc == cls.U:
            return '.U'
        if nuc == cls.R:
            return '.AG'
        if nuc == cls.Y:
            return '.CU'
        if nuc == cls.S:
            return '.GC'
        if nuc == cls.W:
            return '.AU'
        if nuc == cls.K:
            return '.GU'
        if nuc == cls.M:
            return '.AC'
        if nuc == cls.B:
            return '.CGU'
        if nuc == cls.D:
            return '.AGU'
        if nuc == cls.H:
            return '.ACU'
        if nuc == cls.V:
            return '.ACG'
        if nuc == cls.N or nuc == cls.X:
            return '.ACGU'
        if nuc == cls.GAP or nuc == cls.DOT:
            return '-'  # Not possible to match
        raise Exception(f'Unknow nucleotide "{nuc}" parsed.')


@dataclass
class InsertionResult:
    starts: list[int] = field(default_factory=list)
    ends: list[int] = field(default_factory=list)
    pseudoknotables_list: list[list[bool]] = field(default_factory=list)
    weights: list[float] = field(default_factory=list)
    seqs: list[str] = field(default_factory=list)


class SequenceHelper:
    ANY_NUCLEOTIDE = '.'
    STRAND_SEPARATOR = '-'
    MINIMAL_STRAND_LENGTH = 3
    CANONICAL_PAIRS = [
        ('A', 'U'),
        ('U', 'A'),
        ('G', 'C'),
        ('C', 'G'),
        ('G', 'U'),
        ('U', 'G'),
    ]

    @classmethod
    def get_strands_of_desc_line(cls, desc_str: str) -> list[list[str]]:
        """
            Should take as argument the second line of a .desc file.
        """
        nuc_desc = [i.split('_') for i in desc_str.split()]
        if len(nuc_desc) == 0:
            return []

        nuc_by_pos = [(int(pos), nuc) for pos, nuc in nuc_desc]
        pos, nucs = map(list, zip(*nuc_by_pos))
        strands = cls.get_strands_from_list(pos, ''.join(nucs))
        return strands

    @classmethod
    def get_strands_from_list(cls, nuc_pos: list[int], seq: list[str]) -> list[Strand]:
        sequence = cls.get_sequence_from_list(nuc_pos, seq)
        if not sequence:
            return []
        return [Strand(strand) for strand in sequence.split(cls.STRAND_SEPARATOR)]

    @classmethod
    def get_strands_decomposition(cls, nuc_pos: list[int], insert_pos: bool = False) -> list[int]:
        '''
        Create a list of positions, inserting wildcard if the gap is too short
        @param nuc_pos: list of positions to analyse.
        @param insert_pos: Indicate if we insert the missing position, or a wildcard if false.
        @return list of nucleotides positions without small gap.
        '''
        if not nuc_pos:
            return []

        pos_list: list[Union[int, str]] = [nuc_pos[0]]
        for index, pos in enumerate(nuc_pos[1:], 1):
            if pos > nuc_pos[index - 1] + 1 or pos < nuc_pos[index - 1]:
                # Gap Found
                distance = abs(pos - nuc_pos[index - 1])
                if distance < 5:
                    any_insert = distance - 1
                    if insert_pos:
                        pos_list.extend(range(nuc_pos[index - 1] + 1, nuc_pos[index]))
                    else:
                        pos_list.extend([cls.ANY_NUCLEOTIDE] * any_insert)
            pos_list.append(pos)
        return pos_list

    @classmethod
    def get_sequence_from_list(
        cls, nuc_pos: list[int], seq: str, wildcard_threshold=DEFAULT_WILDCARD_THRESHOLD,
    ) -> Optional[str]:
        """
            From a list of nucleotides positions, and a sequence of nucleotides,
            Return a list of nucs, separated by any gap found.
            Will return an empty list if the strands are not valid (too many wildcard)
        """
        # First, create a list of positions, inserting wildcard if the gap is too short
        pos_list: list[Union[int, str]] = cls.get_strands_decomposition(nuc_pos)

        # Second, create a list of strands from the pos list
        strands = []
        strand = [seq[0]]
        seq_index = 1
        for index, pos in enumerate(pos_list[1:], 1):
            if pos == cls.ANY_NUCLEOTIDE:
                strand.append(pos)
                continue
            elif (
                pos_list[index - 1] != cls.ANY_NUCLEOTIDE
                and (pos > pos_list[index - 1] + 1 or pos < pos_list[index - 1])
            ):
                strands.append(strand)
                strand = []
            strand.append(seq[seq_index])
            seq_index += 1
        strands.append(strand)

        # check for wild card
        wildcard = 0
        total = 0
        for strand in strands:
            wildcard += sum([1 for n in strand if n == cls.ANY_NUCLEOTIDE])
            if len(strand) < cls.MINIMAL_STRAND_LENGTH:
                wildcard += cls.MINIMAL_STRAND_LENGTH - len(strand)
            total += len(strand)

        if wildcard / total >= wildcard_threshold:
            logging.warn('Too many wildcards in the sequence.')
            return None
        # Finally, convert to strand list
        strands = [''.join(s) for s in strands]
        return cls.STRAND_SEPARATOR.join(strands)

    @staticmethod
    def is_equivalent_IUPAC_seq(seq1: str, seq2: str) -> bool:
        ''' Look if seq1 is equivaent to an IUPAC coded seq2.'''
        if seq1 == seq2:
            return True
        is_equivalent = True
        for s, t in zip(seq1, seq2):
            if s not in IUPACConverter.to_possible_out(t):
                is_equivalent = False
                break
        return is_equivalent

    @classmethod
    def get_possible_insertions_of_alignement(
        cls,
        strand: Strand,
        sequence: str,
        alignments: list[str],
        minimum_pairing_distance: int = MINIMAL_STRAND_LENGTH,
        minimum_alignment_match_threshold: float = 0.5,
        maximum_alignment_distance: int = 1,
    ) -> InsertionResult:
        result = InsertionResult()
        nb_nucs = len(alignments[0])
        strand_len = len(strand.sequence)
        for n in range(nb_nucs - strand_len):
            inserting = False
            end_pos = n + strand_len
            subseq = sequence[n:end_pos]

            # If the strand fit the sequence, we insert it anyway with the ali weight
            if re.match(rf'{subseq}', strand.sequence):
                inserting = True

            if inserting or len(strand.sequence) > 2:
                matchs = 0
                total_seen = 0
                for alignment in alignments:
                    sub_ali_seq = alignment[n:end_pos]
                    # If the subsequence is only gap, skip it
                    if re.match(r'[\.\-]{%s}' % len(sub_ali_seq), sub_ali_seq):
                        continue
                    total_seen += 1
                    # Check if the subsequence is not too far from the original sequence
                    hamming_dist = cls.hamming_distance(subseq, sub_ali_seq)
                    if (
                        hamming_dist <= maximum_alignment_distance
                        and cls.is_equivalent_IUPAC_seq(
                            strand.sequence, alignment[n:end_pos],
                        )
                    ):
                        matchs += 1

                ratio = matchs / total_seen
                if not inserting and ratio >= minimum_alignment_match_threshold:
                    inserting = True

            if inserting:
                cls._evaluate_insertion_match(
                    strand,
                    result,
                    nb_nucs,
                    n,
                    end_pos - 1,
                    minimum_pairing_distance,
                )
                result.weights.extend([ratio for _ in result.starts])
        return result

    @classmethod
    def get_possible_insertions_of_sequence(
        cls,
        strand: Strand,
        compared_sequence: str,
        minimum_pairing_distance: int = MINIMAL_STRAND_LENGTH,
    ) -> InsertionResult:
        result = InsertionResult()
        # Find a match for a specific sequence
        for match in re.finditer(rf'{strand.sequence}', compared_sequence):
            match_start = match.start()
            match_end = match.end() - 1
            cls._evaluate_insertion_match(
                strand,
                result,
                len(compared_sequence),
                match_start,
                match_end,
                minimum_pairing_distance,
            )
        result.weights.extend([1 for _ in result.starts])
        return result

    @classmethod
    def _evaluate_insertion_match(
        cls,
        strand: Strand,
        result: InsertionResult,
        max_length: int,
        match_start: int,
        match_end: int,
        minimum_pairing_distance: int,
    ):
        # If our strand is shorter than the min, we need enforce the min
        if (difference := minimum_pairing_distance - len(strand.sequence)) > 0:
            for x in range(0, difference + 1):
                insert_start = match_start - difference + x
                insert_end = match_end + x
                if (
                    insert_start >= 0 and insert_end < max_length
                    and insert_start not in result.starts
                ):
                    result.starts.append(insert_start)
                    result.ends.append(insert_end)
                    ps_status = (
                        [False for _ in range(insert_start, match_start)]
                        + strand.pseudokotable_list
                        + [False for _ in range(match_end, insert_end)]
                    )
                    result.pseudoknotables_list.append(ps_status)
                    result.seqs.append(''.join(chain(
                        [cls.ANY_NUCLEOTIDE for _ in range(insert_start, match_start)],
                        strand.sequence,
                        [cls.ANY_NUCLEOTIDE for _ in range(match_end, insert_end)],
                    )))
        else:
            result.starts.append(match_start)
            result.ends.append(match_end)
            result.seqs.append(strand.sequence)
            result.pseudoknotables_list.append(strand.pseudokotable_list)

    @classmethod
    def filter_canonical_pair(cls, sequence: str, pairings: list[Pairing]) -> list[Pairing]:
        out = []
        for pair in pairings:
            nuc_pairing = (sequence[pair[0]], sequence[pair[1]])
            if cls.is_canonical(nuc_pairing):
                out.append(pair)
        return out

    @classmethod
    def is_canonical(cls, pair: tuple[str, str]) -> bool:
        return pair in cls.CANONICAL_PAIRS

    @staticmethod
    def get_motif_name(position: int, strands_list: list[dict]) -> Optional[str]:
        motif = None
        for s in strands_list:
            if s['start'] <= position <= s['end']:
                motif = s['name']
                break
        return motif

    @staticmethod
    def hamming_distance(seq1: str, seq2: str) -> int:
        return sum([
            1 if a not in IUPACConverter.to_possible_out(b) else 0
            for a, b in zip(seq1, seq2)
        ])
