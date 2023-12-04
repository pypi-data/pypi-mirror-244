
from rnamoip.ip_model.ip_manager import Solver
from rnamoip.predicter import Predicter


def test_without_possible_insertion():
    ss = '....'
    sequence = 'AAAA'
    desc_folder = 'tests/desc_mocks/single'

    result = Predicter(None, sequence, ss, motifs_path=desc_folder, parser='desc', solver=Solver.CP_SAT).iterate()

    assert(len(result.motifs) == 0)


# Not a test since we need CBC installation
def single_insertion_with_pairing_MIP():
    ss = '((...))'
    sequence = 'AAAAAAA'
    desc_folder = 'tests/desc_mocks/single'

    predicter = Predicter(None, sequence, ss, motifs_path=desc_folder, parser='desc', solver=Solver.MIP)
    result = predicter.iterate()

    assert(len(result.motifs) == 1)
    inserted_motif = result.motifs['0']
    assert(inserted_motif['name'] == 'single.desc')
    assert(len(inserted_motif['strands']) == 1)
    assert(inserted_motif['strands'][0]['seq'] == 'AAAA')
    assert(inserted_motif['strands'][0]['strand_id'] == 0)
    assert(inserted_motif['strands'][0]['start'] == 1)
    assert(inserted_motif['strands'][0]['end'] == 4)


def test_single_insertion_with_pairing_CP_SAT():
    ss = '((...))'
    sequence = 'AAAAAAA'
    desc_folder = 'tests/desc_mocks/single'

    predicter = Predicter(None, sequence, ss, motifs_path=desc_folder, parser='desc', solver=Solver.CP_SAT)
    result = predicter.iterate()

    assert(len(result.motifs) == 1)
    inserted_motif = result.motifs['0']
    assert(inserted_motif['name'] == 'single.desc')
    assert(len(inserted_motif['strands']) == 1)
    assert(inserted_motif['strands'][0]['seq'] == 'AAAAA')
    assert(inserted_motif['strands'][0]['strand_id'] == 0)
    assert(inserted_motif['strands'][0]['start'] == 1)
    assert(inserted_motif['strands'][0]['end'] == 5)


def test_double_insertion():
    ss = '((...)).((...))..((...))'
    sequence = 'AAAAAAAAAAAAAAAAAAAAAAAA'
    desc_folder = 'tests/desc_mocks/single'

    predicter = Predicter(None, sequence, ss, motifs_path=desc_folder, parser='desc', solver=Solver.CP_SAT)
    result = predicter.iterate()

    assert(len(result.motifs) == 1)
    inserted_motif = result.motifs['0']
    assert(inserted_motif['name'] == 'single.desc')
    assert(len(inserted_motif['strands']) == 3)
    assert(inserted_motif['strands'][0]['seq'] == 'AAAAA')
    assert(inserted_motif['strands'][0]['strand_id'] == 0)
    assert(inserted_motif['strands'][0]['start'] == 1)
    assert(inserted_motif['strands'][0]['end'] == 5)
    assert(inserted_motif['strands'][1]['start'] == 9)
    assert(inserted_motif['strands'][1]['end'] == 13)
    assert(inserted_motif['strands'][2]['start'] == 18)
    assert(inserted_motif['strands'][2]['end'] == 22)


if __name__ == '__main__':
    test_double_insertion()
