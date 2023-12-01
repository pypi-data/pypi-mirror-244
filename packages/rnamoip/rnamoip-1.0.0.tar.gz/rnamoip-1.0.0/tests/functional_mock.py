
from rnamoip.ip_model.ip_manager import Solver
from rnamoip.predicter import Predicter


def without_possible_insertion():
    ss = '....'
    sequence = 'AAAA'
    desc_folder = 'tests/desc_mocks/single'

    result = Predicter(None, sequence, ss, desc_folder, solver=Solver.CP_SAT).iterate()

    assert(len(result.motifs) == 0)


def single_insertion_with_pairing():
    ss = '((..))'
    sequence = 'AAAAAA'
    desc_folder = 'tests/desc_mocks/single'

    result = Predicter(None, sequence, ss, desc_folder, solver=Solver.CP_SAT).iterate()

    assert(len(result.motifs) == 1)
    inserted_motif = result.motifs[0][0]
    assert(inserted_motif['id'] == 0)
    assert(inserted_motif['name'] == 'single.desc')
    assert(inserted_motif['seq'] == 'AAAA')
    assert(inserted_motif['strand_id'] == 0)


def double_insertion():
    ss = '((...)).((...))..((...))'
    sequence = 'AAAAAAAAAAAAAAAAAAAAAAAA'
    desc_folder = 'tests/desc_mocks/single'

    result = Predicter(None, sequence, ss, desc_folder, solver=Solver.MIP).iterate()

    assert(len(result.motifs) == 2)
    inserted_motif = result.motifs[0][0]
    second_motif = result.motifs[4][0]
    assert(inserted_motif['id'] == 0)
    assert(inserted_motif['name'] == 'single.desc')
    assert(inserted_motif['seq'] == 'AAAA')
    assert(inserted_motif['strand_id'] == 0)
    assert(second_motif == inserted_motif)


if __name__ == '__main__':
    double_insertion()
