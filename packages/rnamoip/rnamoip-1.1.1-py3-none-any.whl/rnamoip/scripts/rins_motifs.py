
import json


with open('rins_with_pdb_pos.json', 'r') as rins_in:
    rins_by_sequence = json.load(rins_in)

seqs = list(rins_by_sequence.keys())
one_strand = [s for s in seqs if s.count('-') == 0]
two_strand = [s for s in seqs if s.count('-') == 1]
three_strand = [s for s in seqs if s.count('-') == 2]
four_strand = [s for s in seqs if s.count('-') == 3]
five_strand = [s for s in seqs if s.count('-') >= 4]


print(f'Motifs count: {len(seqs)}.')
print(f'Motif of 1-strand: {len(one_strand)}')
print(f'Motif of 2-strand: {len(two_strand)}')
print(f'Motif of 3-strand: {len(three_strand)}')
print(f'Motif of 4-strand: {len(four_strand)}')
print(f'Motif of 5+ strand: {len(five_strand)}')


def extract_loops():
    loops = {
        s: infos for s, infos in rins_by_sequence.items()
        if s.count('-') >= 2
    }
    with open('loops.json', 'w') as rins_out:
        json.dump(loops, rins_out, indent=2)


if __name__ == '__main__':
    extract_loops()
