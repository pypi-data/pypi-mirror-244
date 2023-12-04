from rnamoip.database.model.strand import Strand
from rnamoip.helpers.sequence import InsertionResult, SequenceHelper


def test_no_insertions_sequence():
    seq1 = Strand('A')
    seq2 = 'G'
    result = SequenceHelper.get_possible_insertions_of_sequence(seq1, seq2)
    assert InsertionResult([], [], [], []) == result


def test_no_insertions_complex_sequence():
    seq1 = Strand('AGC')
    seq2 = 'AACUGUCAGUCGAU'
    result = SequenceHelper.get_possible_insertions_of_sequence(seq1, seq2)
    expected = InsertionResult([], [], [], [])
    assert expected == result


def test_1_match_in_sequence():
    seq1 = Strand('AGC')
    seq2 = 'AACUGUCAGCUCGAU'
    result = SequenceHelper.get_possible_insertions_of_sequence(seq1, seq2)
    expected = InsertionResult([7], [9], [[False, False, False]], [1], ['AGC'])
    assert expected == result


def test_3_match_in_sequence():
    seq1 = Strand('AGC')
    seq2 = 'AACUGUCAGCUCGAGCUUAAGAGC'
    result = SequenceHelper.get_possible_insertions_of_sequence(seq1, seq2)
    expected = InsertionResult(
        [7, 13, 21],
        [9, 15, 23],
        [[False, False, False], [False, False, False], [False, False, False]],
        [1, 1, 1],
        ['AGC', 'AGC', 'AGC'],
    )
    assert expected == result


def test_2_match_below_minimal_length_in_sequence():
    seq1 = Strand('AG')
    seq2 = 'AAGCUGUCAGCUC'
    result = SequenceHelper.get_possible_insertions_of_sequence(seq1, seq2)
    expected = InsertionResult(
        [0, 1, 7, 8],
        [2, 3, 9, 10],
        [[False, False, False], [False, False, False], [False, False, False], [False, False, False]],
        [1, 1, 1, 1],
        ['.AG', 'AG.', '.AG', 'AG.'],
    )
    assert expected == result


def test_2_match_more_below_minimal_length_in_sequence():
    seq1 = Strand('G')
    seq2 = 'AACUGUCAGCUC'
    result = SequenceHelper.get_possible_insertions_of_sequence(seq1, seq2)
    expected = InsertionResult(
        [2, 3, 4, 6, 7, 8],
        [4, 5, 6, 8, 9, 10],
        [
            [False, False, False], [False, False, False], [False, False, False],
            [False, False, False], [False, False, False], [False, False, False],
        ],
        [1, 1, 1, 1, 1, 1],
        ['..G', '.G.', 'G..', '..G', '.G.', 'G..'],
    )
    assert expected == result


def test_match_below_minimal_length_on_edge():
    seq1 = Strand('UA')
    seq2 = 'UAGGAUGCUA'
    result = SequenceHelper.get_possible_insertions_of_sequence(seq1, seq2)
    expected = InsertionResult(
        [0, 7],
        [2, 9],
        [[False, False, False], [False, False, False]],
        [1, 1],
        ['UA.', '.UA'],
    )
    assert expected == result


def test_is_equivalent_IUPAC_seq():
    seq1 = 'AUG'
    seq_IUPAC = 'AWN'
    assert SequenceHelper.is_equivalent_IUPAC_seq(seq1, seq_IUPAC)


def test_is_equivalent_IUPAC_seq_with_dot():
    seq1 = '.UG'
    seq_IUPAC = 'AYG'
    assert SequenceHelper.is_equivalent_IUPAC_seq(seq1, seq_IUPAC)


def test_is_not_equivalent_IUPAC_seq():
    seq1 = 'AUG'
    seq_IUPAC = 'ASN'
    assert not SequenceHelper.is_equivalent_IUPAC_seq(seq1, seq_IUPAC)


def test_insertion_alignment_1_match_in_sequence():
    seq1 = Strand('AGC')
    seq2 = 'AAAAGCACGA'
    alignments = [
        'AAAAGCACGA',
        'AAAGGCACGA',
    ]
    result = SequenceHelper.get_possible_insertions_of_alignement(seq1, seq2, alignments)
    expected = InsertionResult([3], [5], [[False, False, False]], [0.5], ['AGC'])
    assert expected == result


def test_insertion_alignment_match_below_threshold():
    seq1 = Strand('AGC')
    seq2 = 'AAAGGCACGA'
    alignments = [
        'AAAAGCACGA',
        'AAAGGCACGA',
        'AAAGGCACGA',
    ]
    result = SequenceHelper.get_possible_insertions_of_alignement(seq1, seq2, alignments)
    expected = InsertionResult([], [], [], [])
    assert expected == result


def test_insertion_alignment_match_above_threshold():
    seq1 = Strand('AGC')
    seq2 = 'AAAGGCACGA'
    alignments = [
        'AAAAGCACGA',
        'AAAAGCACGA',
        'AAAGGCACGA',
        'AAAGGCACGA',
    ]
    result = SequenceHelper.get_possible_insertions_of_alignement(seq1, seq2, alignments)
    expected = InsertionResult([3], [5], [[False, False, False]], [0.5], ['AGC'])
    assert expected == result


def test_no_insertion_alignment_small_strand_only_main_seq():
    seq1 = Strand('U')
    seq2 = 'AAAGGCACGA'
    alignments = [
        'AAAAGUACGA',
        'AAAAGUACGA',
        'AAAGGUACGA',
        'AAAGGCACGA',
    ]
    result = SequenceHelper.get_possible_insertions_of_alignement(seq1, seq2, alignments)
    expected = InsertionResult([], [], [], [])
    assert expected == result


def test_no_insertion_alignment_with_high_hamming():
    seq1 = Strand('GGG')
    seq2 = 'AAG'
    alignments = [
        'GGG',
        'GGG',
        'GGG',
        'AAA',
    ]
    result = SequenceHelper.get_possible_insertions_of_alignement(seq1, seq2, alignments)
    expected = InsertionResult([], [], [], [])
    assert expected == result


def test_hamming_distance():
    seq1 = 'GGG'
    seq2 = 'AAG'
    assert 2 == SequenceHelper.hamming_distance(seq1, seq2)


def test_hamming_distance_with_IUPAC():
    seq1 = 'GGG'
    seq2 = 'ANG'
    assert 1 == SequenceHelper.hamming_distance(seq1, seq2)


def test_get_sequence_from_list_without_split():
    seq = 'CUAGCGCGAGGUCGCG'
    nucs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    result = SequenceHelper.get_sequence_from_list(nucs, seq)
    assert 'CUAGCGCGAGGUCGCG' == result


def test_get_sequence_from_list_with_split():
    seq = 'CUAGCGCGAGGUCGCG'
    nucs = [2, 3, 4, 5, 14, 15, 16, 42, 43, 44, 45, 46, 47, 48, 64, 65]
    result = SequenceHelper.get_sequence_from_list(nucs, seq)
    assert 'CUAG-CGC-GAGGUCG-CG' == result
