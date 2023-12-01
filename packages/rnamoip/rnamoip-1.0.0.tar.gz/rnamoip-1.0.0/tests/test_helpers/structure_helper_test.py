
import pytest
from rnamoip.helpers.structure import StructureHelper


def test_find_base_pairings():
    structure = '..(..((.))...).'
    pairings = StructureHelper._find_base_pairings(structure)
    assert (pairings == [(2, 13), (5, 9), (6, 8)])


def test_find_others_base_pairings():
    structure = '(.(()).)'
    pairings = StructureHelper._find_base_pairings(structure)
    assert (pairings == [(0, 7), (2, 5), (3, 4)])


def test_find_base_pairings_invalid_right_should_raise():
    structure_more_right = '(.).).'
    with pytest.raises(Exception):
        _ = StructureHelper._find_base_pairings(structure_more_right)


def test_find_base_pairings_invalid_left_should_raise():
    structure_more_left = '(.(.).'
    with pytest.raises(Exception):
        _ = StructureHelper._find_base_pairings(structure_more_left)


def test_find_base_pairings_valid_without_pairings():
    structure = '.......'
    pairings = StructureHelper.find_base_pairings_with_level(structure)
    assert pairings == ({
        0: [],
        1: [],
        2: [],
    }, {
        0: '.......',
        1: '.......',
        2: '.......',
    })


def test_find_base_pairings_valid_without_pseudoknot():
    structure = '(..((..))..)'
    pairings = StructureHelper.find_base_pairings_with_level(structure)
    assert pairings == ({
        0: [(0, 11), (3, 8), (4, 7)],
        1: [],
        2: [],
    }, {
        0: '(..((..))..)',
        1: 'x..xx..xx..x',
        2: 'x..xx..xx..x',
    })


def test_find_base_pairings_with_valid_lvl2_pseudoknot():
    structure = '(..[.((..).])..)'
    pairings = StructureHelper.find_base_pairings_with_level(structure)
    assert pairings == ({
        0: [(0, 15), (5, 12), (6, 9)],
        1: [(3, 11)],
        2: [],
    }, {
        0: '(..x.((..).x)..)',
        1: 'x..(.xx..x.)x..x',
        2: 'x..x.xx..x.xx..x',
    })


def test_find_base_pairings_with_valid_lvl3_pseudoknot():
    structure = '(..[.((.{.).])..})'
    pairings = StructureHelper.find_base_pairings_with_level(structure)
    assert pairings == ({
        0: [(0, 17), (5, 13), (6, 10)],
        1: [(3, 12)],
        2: [(8, 16)],
    }, {
        0: '(..x.((.x.).x)..x)',
        1: 'x..(.xx.x.x.)x..xx',
        2: 'x..x.xx.(.x.xx..)x',
    })


def test_find_base_pairings_with_valid_lvl4_pseudoknot():
    structure = '(..[.((.{.)..<])..})..>'
    pairings = StructureHelper.find_base_pairings_with_level(structure, maximum_pairing_level=4)
    assert pairings == ({
        0: [(0, 19), (5, 15), (6, 10)],
        1: [(3, 14)],
        2: [(8, 18)],
        3: [(13, 22)],
    }, {
        0: '(..x.((.x.)..xx)..x)..x',
        1: 'x..(.xx.x.x..x)x..xx..x',
        2: 'x..x.xx.(.x..xxx..)x..x',
        3: 'x..x.xx.x.x..(xx..xx..)',
    })


def test_find_base_pairings_with_invalid_pseudoknot_should_not_raise():
    # Doesn't raise anymore, since we have tools that behave like that.
    # However, a warning should be logged.
    structure = '(..[.((..)).]..)'
    pairings = StructureHelper.find_base_pairings_with_level(structure)
    assert pairings == ({
        0: [(0, 15), (5, 10), (6, 9)],
        1: [(3, 12)],
        2: [],
    }, {
        0: '(..x.((..)).x..)',
        1: 'x..(.xx..xx.)..x',
        2: 'x..x.xx..xx.x..x',
    })


def test_pairing_to_str():
    pairings = [(2, 13), (5, 9), (6, 8)]
    length = 15
    pairings_per_lvl, structure = StructureHelper.pairings_to_str(pairings, length)
    assert ('..(..((.))...).' == structure)
    assert ({
        0: [(2, 13), (5, 9), (6, 8)],
    } == pairings_per_lvl)


def test_pairing_to_str_with_pseudoknot():
    pairings = [(0, 9), (1, 8), (4, 11), (5, 10)]
    length = 12
    pairings_per_lvl, structure = StructureHelper.pairings_to_str(pairings, length)
    assert ('((..[[..))]]' == structure)
    assert ({
        0: [(0, 9), (1, 8)],
        1: [(4, 11), (5, 10)],
    } == pairings_per_lvl)


def test_pairing_to_str_with_lvl3_pseudoknot():
    pairings = [(0, 13), (1, 12), (4, 15), (5, 14), (8, 17), (9, 16)]
    length = 18
    pairings_per_lvl, structure = StructureHelper.pairings_to_str(pairings, length)
    assert ('((..[[..{{..))]]}}' == structure)
    assert ({
        0: [(0, 13), (1, 12)],
        1: [(4, 15), (5, 14)],
        2: [(8, 17), (9, 16)],
    } == pairings_per_lvl)


def test_get_pairings_between_two_ordered_position():
    pairings = [(2, 13), (5, 9), (6, 8)]
    pairings_in = StructureHelper.get_pairings_crossing_two_positions(pairings, 4, 7)
    assert ([(5, 9), (6, 8)] == pairings_in)


def test_get_no_pairings_between_two_unordered_position():
    pairings = [(2, 13), (5, 9), (6, 8)]
    pairings_in = StructureHelper.get_pairings_crossing_two_positions(pairings, 5, 4)
    assert ([] == pairings_in)


def test_get_pairings_inside_two_position():
    pairings = [(2, 13), (5, 9), (6, 8)]
    pairings_in = StructureHelper.get_pairings_inside_two_positions(pairings, 4, 10)
    assert ([(5, 9), (6, 8)] == pairings_in)


def test_get_no_pairings_inside_two_position():
    pairings = [(2, 13), (5, 9), (6, 8)]
    pairings_in = StructureHelper.get_pairings_inside_two_positions(pairings, 4, 6)
    assert ([] == pairings_in)


def test_get_no_pairings_inside_two_unordered_position():
    pairings = [(2, 13), (5, 9), (6, 8)]
    pairings_in = StructureHelper.get_pairings_crossing_two_positions(pairings, 10, 4)
    assert ([] == pairings_in)


def test_remove_lonely_pairings():
    pairings = [(2, 13), (5, 9), (6, 8)]
    filtered_pairings = StructureHelper.remove_lonely_pairings(pairings)
    assert([(5, 9), (6, 8)] == filtered_pairings)


def test_remove_lonely_pairings_recursive():
    pairings = [(2, 13), (5, 9), (6, 11)]
    filtered_pairings = StructureHelper.remove_lonely_pairings(pairings)
    assert([] == filtered_pairings)


def test_remove_lonely_pairings_extensive():
    ss = '(((((.(..((((........)))).(((((.......))))).....(((((.......)))))).)))))....'
    pairings = StructureHelper._find_base_pairings(ss)
    filtered_pairings = StructureHelper.remove_lonely_pairings(pairings)
    assert([
        (0, 71), (1, 70), (2, 69), (3, 68), (4, 67), (9, 24), (10, 23), (11, 22), (12, 21), (26, 42),
        (27, 41), (28, 40), (29, 39), (30, 38), (48, 64), (49, 63), (50, 62), (51, 61), (52, 60),
    ] == filtered_pairings)


def test_get_lvl_from_pairings():
    pairings = [(2, 13), (5, 9), (6, 8)]
    length = 15
    lvl_per_nuc = StructureHelper.get_lvl_from_pairings(pairings, length)
    expected = [-1, -1, 0, -1, -1, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1]
    print(lvl_per_nuc)
    assert expected == lvl_per_nuc


def test_get_lvl_from_pairings_with_lvl1():
    pairings = [(0, 9), (1, 8), (4, 11), (5, 10)]
    length = 12
    lvl_per_nuc = StructureHelper.get_lvl_from_pairings(pairings, length)
    expected = [0, 0, -1, -1, 1, 1, -1, -1, -1, -1, -1, -1]
    print(lvl_per_nuc)
    assert expected == lvl_per_nuc


def test_get_lvl_from_pairings_with_lvl2():
    pairings = [(0, 13), (1, 12), (4, 15), (5, 14), (8, 17), (9, 16)]
    length = 18
    lvl_per_nuc = StructureHelper.get_lvl_from_pairings(pairings, length)
    expected = [0, 0, -1, -1, 1, 1, -1, -1, 2, 2, -1, -1, -1, -1, -1, -1, -1, -1]
    assert expected == lvl_per_nuc


def test_use_case():
    pairing_list = [
        (1, 48), (2, 47), (3, 46), (4, 45), (5, 24), (6, 23), (7, 22), (8, 21), (9, 20),
        (10, 19), (11, 18), (15, 35), (16, 34), (29, 44), (30, 43), (31, 42), (32, 41),
    ]
    length = 48
    lvl_per_nuc = StructureHelper.get_lvl_from_pairings(pairing_list, length)
    expected = [
        -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
        -1, -1, -1, 0, 0, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,
    ]
    assert expected == lvl_per_nuc

    pairings_per_lvl, ss = StructureHelper.pairings_to_str(pairing_list, length)
    expected_ss = ".(((((((((((...[[.)))))))....((((.]].....)))))))"
    assert expected_ss == ss

    assert ({
        0: [
            (1, 48), (2, 47), (3, 46), (4, 45), (5, 24), (6, 23), (7, 22),
            (8, 21), (9, 20), (10, 19), (11, 18), (29, 44), (30, 43),
            (31, 42), (32, 41),
        ],
        1: [(15, 35), (16, 34)],
    } == pairings_per_lvl)


if __name__ == '__main__':
    test_pairing_to_str_with_pseudoknot()
