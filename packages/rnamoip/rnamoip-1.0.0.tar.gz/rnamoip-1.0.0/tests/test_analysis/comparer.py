
from rnamoip.analysis.comparer import Comparer, ComparerResult, InteractionResult
from rnamoip.analysis.model.interaction import Interaction

# Disabled those test since ViennaRNA is messign up the tests

def test_small_ss():
    real_ss = ".((((((....))))))"
    pred_ss = ".(.((.((..)).)).)"
    motifs = {}
    result = Comparer.get_compare_result(real_ss, pred_ss, motifs)
    assert ComparerResult(
        true_positives=4,
        false_positives=1,
        false_negatives=2,
    ) == result


def small_ss_with_motif_coverage():
    real_ss = ".((((((....))))))"
    pred_ss = ".(.((.((..)).)).)"
    motifs = {
        "1": {
            "name": "CAU-AUG",
            "related": [],
            "strands": [
                {
                    "name": "CAU-AUG",
                    "seq": "AUG",
                    "strand_seq": "AUG",
                    "strand_id": 1,
                    "start": 1,
                    "end": 3,
                },
                {
                    "name": "CAU-AUG",
                    "seq": "CAU",
                    "strand_seq": "CAU",
                    "strand_id": 0,
                    "start": 14,
                    "end": 16,
                },
            ],
        },
    }
    result = Comparer.get_compare_result(real_ss, pred_ss, motifs)
    assert ComparerResult(
        true_positives=5,
        false_positives=1,
        false_negatives=1,
    ) == result


def test_small_ss_with_motif_not_matching():
    real_ss = ".((((((....))))))"
    pred_ss = ".(.((.((..)).)).)"
    motifs = {
        "1": {
            "name": "CAU-AUG",
            "related": [],
            "strands": [
                {
                    "name": "CAU-AUG",
                    "seq": "AUG",
                    "strand_seq": "AUG",
                    "strand_id": 1,
                    "start": 1,
                    "end": 3,
                },
                {
                    "name": "CAU-AUG",
                    "seq": "CAU",
                    "strand_seq": "CAU",
                    "strand_id": 0,
                    "start": 8,
                    "end": 10,
                },
            ],
        },
    }
    result = Comparer.get_compare_result(real_ss, pred_ss, motifs)
    assert ComparerResult(
        true_positives=4,
        false_positives=1,
        false_negatives=2,
    ) == result


def test_small_ss_with_motif_coverage_with_motif_with_gap():
    real_ss = ".((((((....))))))"
    pred_ss = ".(..(.((..)).)..)"
    motifs = {
        "1": {
            "name": "CAU-UG",
            "related": [],
            "strands": [
                {
                    "name": "CAU-UG",
                    "seq": ".UG",
                    "strand_seq": ".UG",
                    "strand_id": 1,
                    "start": 14,
                    "end": 16,
                },
                {
                    "name": "CAU-UG",
                    "seq": "CAU",
                    "strand_seq": "CAU",
                    "strand_id": 0,
                    "start": 1,
                    "end": 3,
                },
            ],
        },
    }
    result = Comparer.get_compare_result(real_ss, pred_ss, motifs)
    assert ComparerResult(
        true_positives=5,
        false_positives=1,
        false_negatives=1,
    ) == result


def test_concrete_example_ss_no_motifs():
    real_ss = ".(((((((.....(((((.....[[)))))..........((((((]].....))))))..)))))))"
    pred_ss = ".((((.((..((.((.((...[[[[)).))..))......(((.((]]]]...)).)))..)).))))"
    motifs = {}
    result = Comparer.get_compare_result(real_ss, pred_ss, motifs)
    assert ComparerResult(17, 4, 3) == result


def test_concrete_example_ss_with_motifs():
    real_ss = ".(((((((.....(((((.....[[)))))..........((((((]].....))))))..)))))))"
    pred_ss = ".((((.((..((.((.((...[[[[)).))..))......(((.((]]]]...)).)))..)).))))"
    #         "....111555566644477777....444666......555222333.8888333222.555111..."
    # Motif can be represented as above:
    motifs = {
        "332": {
            "name": "CAU-AUG",
            "related": [],
            "strands": [
                {
                    "name": "CAU-AUG",
                    "seq": "AUG",
                    "strand_seq": "AUG",
                    "strand_id": 1,
                    "start": 62,
                    "end": 64,
                },
                {
                    "name": "CAU-AUG",
                    "seq": "CAU",
                    "strand_seq": "CAU",
                    "strand_id": 0,
                    "start": 4,
                    "end": 6,
                },
            ],
        },
        "319": {
            "name": "CGU-ACG",
            "related": [],
            "strands": [
                {
                    "name": "CGU-ACG",
                    "seq": "CGU",
                    "strand_seq": "CGU",
                    "strand_id": 0,
                    "start": 14,
                    "end": 16,
                },
                {
                    "name": "CGU-ACG",
                    "seq": "ACG",
                    "strand_seq": "ACG",
                    "strand_id": 1,
                    "start": 26,
                    "end": 28,
                },
            ],
        },
        "306": {
            "name": "GGC-GUC",
            "related": [],
            "strands": [
                {
                    "name": "GGC-GUC",
                    "seq": "GUC",
                    "strand_seq": "GUC",
                    "strand_id": 1,
                    "start": 54,
                    "end": 56,
                },
                {
                    "name": "GGC-GUC",
                    "seq": "GGC",
                    "strand_seq": "GGC",
                    "strand_id": 0,
                    "start": 42,
                    "end": 44,
                },
            ],
        },
        "38": {
            "name": "GGAU",
            "related": [],
            "strands": [
                {
                    "name": "GGAU",
                    "seq": "GGAU",
                    "strand_seq": "GGAU",
                    "strand_id": 0,
                    "start": 17,
                    "end": 20,
                },
            ],
        },
        "584": {
            "name": "UCG-CAA",
            "related": [],
            "strands": [
                {
                    "name": "UCG-CAA",
                    "seq": "CAA",
                    "strand_seq": "CAA",
                    "strand_id": 1,
                    "start": 29,
                    "end": 31,
                },
                {
                    "name": "UCG-CAA",
                    "seq": "UCG",
                    "strand_seq": "UCG",
                    "strand_id": 0,
                    "start": 11,
                    "end": 13,
                },
            ],
        },
        "78": {
            "name": "AUAA-CC-AC",
            "related": [],
            "strands": [
                {
                    "name": "AUAA-CC-AC",
                    "seq": "ACC",
                    "strand_seq": ".CC",
                    "strand_id": 1,
                    "start": 38,
                    "end": 40,
                },
                {
                    "name": "AUAA-CC-AC",
                    "seq": "GAC",
                    "strand_seq": ".AC",
                    "strand_id": 2,
                    "start": 58,
                    "end": 60,
                },
                {
                    "name": "AUAA-CC-AC",
                    "seq": "AUAA",
                    "strand_seq": "AUAA",
                    "strand_id": 0,
                    "start": 7,
                    "end": 10,
                },
            ],
        },
        "583": {
            "name": "AAAU",
            "related": [],
            "strands": [{
                "name": "AAAU",
                "seq": "AAAU",
                "strand_seq": "AAAU",
                "strand_id": 0,
                "start": 50,
                "end": 53,
            }],
        },
    }
    result = Comparer.get_compare_result(real_ss, pred_ss, motifs)
    assert ComparerResult(20, 4, 0) == result


# flake8: noqa: E501
def test_interactions_base():
    interactions_per_pdb_model = {
        '1': [
            Interaction(start_pos=0, end_pos=8, start_nuc='C', end_nuc='G', type='CWW', type2='cWW', motif_from=None, start_strand=0, end_strand=0, model='1', pdb='1L2X', chain='A'),
            Interaction(start_pos=1, end_pos=7, start_nuc='G', end_nuc='A', type='TSS', type2='tSS', motif_from=None, start_strand=0, end_strand=0, model='1', pdb='1L2X', chain='A'),
            Interaction(start_pos=2, end_pos=6, start_nuc='G', end_nuc='C', type='CWW', type2='cWW', motif_from=None, start_strand=0, end_strand=0, model='1', pdb='1L2X', chain='A'),
            Interaction(start_pos=11, end_pos=54, start_nuc='G', end_nuc='C', type='CWW', type2='cWW', motif_from=None, start_strand=0, end_strand=0, model='1', pdb='1L2X', chain='A'),
            Interaction(start_pos=12, end_pos=53, start_nuc='G', end_nuc='C', type='CWW', type2='cWW', motif_from=None, start_strand=0, end_strand=0, model='1', pdb='1L2X', chain='A'),
        ],
    }
    motifs_interactions = {
        (39, 0): {
            73: [
                Interaction(start_pos=0, end_pos=8, start_nuc='C', end_nuc='G', type='CWW', type2='CWW', motif_from=None, start_strand=0, end_strand=0, model=None, pdb='4V5S', chain='DA'),
                Interaction(start_pos=1, end_pos=7, start_nuc='G', end_nuc='A', type='TSS', type2='TSS', motif_from=None, start_strand=0, end_strand=0, model=None, pdb='4V5S', chain='DA'),
                Interaction(start_pos=2, end_pos=6, start_nuc='G', end_nuc='C', type='CWW', type2='CWW', motif_from=None, start_strand=0, end_strand=0, model=None, pdb='4V5S', chain='DA'),
                Interaction(start_pos=2, end_pos=8, start_nuc='G', end_nuc='C', type='CWW', type2='CWW', motif_from=None, start_strand=0, end_strand=0, model=None, pdb='4V5S', chain='DA'),
            ],
        },
    }
    motifs_occurences = {
        (39, 0): {
            'name': 'GG-UCC',
            'related': [73],
            'strands': [
                {'name': 'GG-UCC', 'seq': 'CGG', 'strand_seq': '.GG', 'strand_id': 0, 'start': 0, 'end': 2},
                {'name': 'GG-UCC', 'seq': 'UCC', 'strand_seq': 'UCC', 'strand_id': 1, 'start': 6, 'end': 8},
            ],
        },
    }

    result = Comparer.compare_interactions(
        interactions_per_pdb_model,
        motifs_occurences,
        motifs_interactions,
    )

    expected_result = InteractionResult(
        interactions_ratio=1,
        interactions_ratio_can=1,
        interactions_ratio_non_can=1,
        generous_interactions_ratio=1,
        generous_interactions_ratio_can=1,
        generous_interactions_ratio_non_can=1,
        interactions_count_of_pdb_in_motifs=3,
        best_pdb_model='1',
        best_generous_pdb_model='1',
        best_occurence_list=[((39, 0), 73)],
        total_pdb_interactions=5,
    )
    assert expected_result == result

# flake8: noqa: E501
def test_interactions_motif_outside():
    interactions_per_pdb_model = {
        '1': [
            Interaction(start_pos=0, end_pos=8, start_nuc='C', end_nuc='G', type='CWW', type2='cWW', motif_from=None, start_strand=0, end_strand=0, model='1', pdb='1L2X', chain='A'),
            Interaction(start_pos=1, end_pos=7, start_nuc='G', end_nuc='A', type='TSS', type2='tSS', motif_from=None, start_strand=0, end_strand=0, model='1', pdb='1L2X', chain='A'),
            Interaction(start_pos=2, end_pos=6, start_nuc='G', end_nuc='C', type='CWW', type2='cWW', motif_from=None, start_strand=0, end_strand=0, model='1', pdb='1L2X', chain='A'),
        ],
    }
    motifs_interactions = {
        (39, 0): {
            73: [
                Interaction(start_pos=0, end_pos=3, start_nuc='C', end_nuc='G', type='CWW', type2='CWW', motif_from=None, start_strand=0, end_strand=0, model=None, pdb='4V5S', chain='DA'),
                Interaction(start_pos=1, end_pos=4, start_nuc='G', end_nuc='A', type='TSS', type2='TSS', motif_from=None, start_strand=0, end_strand=0, model=None, pdb='4V5S', chain='DA'),
                Interaction(start_pos=2, end_pos=5, start_nuc='G', end_nuc='C', type='CWW', type2='CWW', motif_from=None, start_strand=0, end_strand=0, model=None, pdb='4V5S', chain='DA'),
            ],
        },
    }
    motifs_occurences = {
        (39, 0): {
            'name': 'GG-UCC',
            'related': [73],
            'strands': [
                {'name': 'GG-UCC', 'seq': 'CGG', 'strand_seq': '.GG', 'strand_id': 0, 'start': 0, 'end': 2},
                {'name': 'GG-UCC', 'seq': 'UCC', 'strand_seq': 'UCC', 'strand_id': 1, 'start': 3, 'end': 5},
            ],
        },
    }

    result = Comparer.compare_interactions(
        interactions_per_pdb_model,
        motifs_occurences,
        motifs_interactions,
    )

    expected_result = InteractionResult(
        interactions_ratio=0,
        interactions_ratio_can=0,
        interactions_ratio_non_can=0,
        generous_interactions_ratio=0,
        generous_interactions_ratio_can=0,
        generous_interactions_ratio_non_can=0,
        interactions_count_of_pdb_in_motifs=0,
        total_pdb_interactions=3,
        best_pdb_model=None,
        best_generous_pdb_model=None,
        best_occurence_list=[],
    )
    assert expected_result == result

# flake8: noqa: E501
def test_interactions_2_models_2_motifs_with_perfect_generous():
    interactions_per_pdb_model = {
        '1': [
            Interaction(start_pos=0, end_pos=8, start_nuc='C', end_nuc='G', type='CWW', type2='cWW', motif_from=None, start_strand=0, end_strand=0, model='1', pdb='1L2X', chain='A'),
            Interaction(start_pos=1, end_pos=8, start_nuc='U', end_nuc='U', type='TSS', type2='tSS', motif_from=None, start_strand=0, end_strand=0, model='1', pdb='1L2X', chain='A'),
            Interaction(start_pos=2, end_pos=8, start_nuc='U', end_nuc='U', type='CWW', type2='cWW', motif_from=None, start_strand=0, end_strand=0, model='1', pdb='1L2X', chain='A'),
        ],
        '2': [
            Interaction(start_pos=0, end_pos=8, start_nuc='C', end_nuc='G', type='CWW', type2='cWW', motif_from=None, start_strand=0, end_strand=0, model='1', pdb='1L2X', chain='A'),
            Interaction(start_pos=1, end_pos=7, start_nuc='G', end_nuc='A', type='TSS', type2='tSS', motif_from=None, start_strand=0, end_strand=0, model='1', pdb='1L2X', chain='A'),
            Interaction(start_pos=2, end_pos=6, start_nuc='G', end_nuc='C', type='CWW', type2='cWW', motif_from=None, start_strand=0, end_strand=0, model='1', pdb='1L2X', chain='A'),
        ],
    }
    motifs_interactions = {
        (39, 0): {
            73: [
                Interaction(start_pos=0, end_pos=12, start_nuc='A', end_nuc='A', type='CWW', type2='CWW', motif_from=None, start_strand=0, end_strand=0, model=None, pdb='4V5S', chain='DA'),
                Interaction(start_pos=1, end_pos=15, start_nuc='A', end_nuc='A', type='TSS', type2='TSS', motif_from=None, start_strand=0, end_strand=0, model=None, pdb='4V5S', chain='DA'),
                Interaction(start_pos=2, end_pos=6, start_nuc='G', end_nuc='C', type='CWW', type2='CWW', motif_from=None, start_strand=0, end_strand=0, model=None, pdb='4V5S', chain='DA'),
            ],
            74: [
                Interaction(start_pos=0, end_pos=8, start_nuc='C', end_nuc='G', type='CWW', type2='CWW', motif_from=None, start_strand=0, end_strand=0, model=None, pdb='4V5S', chain='DA'),
                Interaction(start_pos=1, end_pos=7, start_nuc='G', end_nuc='A', type='TSS', type2='TSS', motif_from=None, start_strand=0, end_strand=0, model=None, pdb='4V5S', chain='DA'),
                Interaction(start_pos=2, end_pos=18, start_nuc='A', end_nuc='A', type='CWW', type2='CWW', motif_from=None, start_strand=0, end_strand=0, model=None, pdb='4V5S', chain='DA'),
            ],
        },
    }
    motifs_occurences = {
        (39, 0): {
            'name': 'GG-UCC',
            'related': [73, 74],
            'strands': [
                {'name': 'GG-UCC', 'seq': 'CGG', 'strand_seq': '.GG', 'strand_id': 0, 'start': 0, 'end': 2},
                {'name': 'GG-UCC', 'seq': 'UCC', 'strand_seq': 'UCC', 'strand_id': 1, 'start': 6, 'end': 8},
            ],
        },
    }

    result = Comparer.compare_interactions(
        interactions_per_pdb_model,
        motifs_occurences,
        motifs_interactions,
    )

    expected_result = InteractionResult(
        interactions_ratio=2/3,
        interactions_ratio_can=0.5,
        interactions_ratio_non_can=1,
        generous_interactions_ratio=1,
        generous_interactions_ratio_can=1,
        generous_interactions_ratio_non_can=1,
        interactions_count_of_pdb_in_motifs=3,
        total_pdb_interactions=3,
        best_pdb_model='2',
        best_generous_pdb_model='2',
        best_occurence_list=[((39, 0), 74)],
    )
    assert expected_result == result

# flake8: noqa: E501
def test_interactions_2_motifs_occurences():
    interactions_per_pdb_model = {
        '1': [
            Interaction(start_pos=0, end_pos=11, start_nuc='C', end_nuc='G', type='CWW', type2='cWW', motif_from=None, start_strand=0, end_strand=0, model='1', pdb='1L2X', chain='A'),
            Interaction(start_pos=1, end_pos=11, start_nuc='U', end_nuc='U', type='TSS', type2='tSS', motif_from=None, start_strand=0, end_strand=0, model='1', pdb='1L2X', chain='A'),
            Interaction(start_pos=2, end_pos=11, start_nuc='U', end_nuc='U', type='CWW', type2='cWW', motif_from=None, start_strand=0, end_strand=0, model='1', pdb='1L2X', chain='A'),
            Interaction(start_pos=3, end_pos=8, start_nuc='C', end_nuc='G', type='CWW', type2='cWW', motif_from=None, start_strand=0, end_strand=0, model='1', pdb='1L2X', chain='A'),
            Interaction(start_pos=4, end_pos=8, start_nuc='U', end_nuc='U', type='TSS', type2='tSS', motif_from=None, start_strand=0, end_strand=0, model='1', pdb='1L2X', chain='A'),
            Interaction(start_pos=5, end_pos=6, start_nuc='U', end_nuc='U', type='TSS', type2='TSS', motif_from=None, start_strand=0, end_strand=0, model='1', pdb='1L2X', chain='A'),
        ],
    }
    motifs_interactions = {
        (39, 0): {
            73: [
                Interaction(start_pos=0, end_pos=11, start_nuc='C', end_nuc='G', type='CWW', type2='CWW', motif_from=None, start_strand=0, end_strand=0, model=None, pdb='4V5S', chain='DA'),
                Interaction(start_pos=1, end_pos=10, start_nuc='A', end_nuc='A', type='TSS', type2='TSS', motif_from=None, start_strand=0, end_strand=0, model=None, pdb='4V5S', chain='DA'),
                Interaction(start_pos=2, end_pos=9, start_nuc='G', end_nuc='C', type='CWW', type2='CWW', motif_from=None, start_strand=0, end_strand=0, model=None, pdb='4V5S', chain='DA'),
            ],
        },
        (39, 1): {
            73: [
                Interaction(start_pos=3, end_pos=8, start_nuc='C', end_nuc='G', type='CWW', type2='CWW', motif_from=None, start_strand=0, end_strand=0, model=None, pdb='4V5S', chain='DA'),
                Interaction(start_pos=4, end_pos=7, start_nuc='A', end_nuc='A', type='TSS', type2='TSS', motif_from=None, start_strand=0, end_strand=0, model=None, pdb='4V5S', chain='DA'),
                Interaction(start_pos=5, end_pos=7, start_nuc='U', end_nuc='U', type='TSS', type2='TSS', motif_from=None, start_strand=0, end_strand=0, model=None, pdb='4V5S', chain='DA'),
            ],
        },
    }
    motifs_occurences = {
        (39, 0):
        {
            'name': 'GG-UCC',
            'related': [73],
            'strands': [
                {'name': 'GG-UCC', 'seq': 'CGG', 'strand_seq': '.GG', 'strand_id': 0, 'start': 0, 'end': 2},
                {'name': 'GG-UCC', 'seq': 'UCC', 'strand_seq': 'UCC', 'strand_id': 1, 'start': 9, 'end': 11},
            ],
        },
        (39, 1):
        {
            'name': 'GG-UCC',
            'related': [73],
            'strands': [
                {'name': 'GG-UCC', 'seq': 'CGG', 'strand_seq': '.GG', 'strand_id': 0, 'start': 3, 'end': 5},
                {'name': 'GG-UCC', 'seq': 'UCC', 'strand_seq': 'UCC', 'strand_id': 1, 'start': 6, 'end': 8},
            ],
        },
    }

    result = Comparer.compare_interactions(
        interactions_per_pdb_model,
        motifs_occurences,
        motifs_interactions,
    )

    expected_result = InteractionResult(
        interactions_ratio=1/3,
        interactions_ratio_can=1,
        interactions_ratio_non_can=0,
        generous_interactions_ratio=1/3,
        generous_interactions_ratio_can=1,
        generous_interactions_ratio_non_can=0,
        interactions_count_of_pdb_in_motifs=6,
        total_pdb_interactions=6,
        best_pdb_model='1',
        best_generous_pdb_model='1',
        best_occurence_list=[((39, 0), 73), ((39, 1), 73)],
    )
    assert expected_result == result
