
import json


def main():
    with open('Roman/alignments_mappings.json', 'r') as data_file:
        data = json.load(data_file)
    seqs = []
    for seq_data in data[1]:
        seqs.append(seq_data[0])

    with open('sequences.json', 'w') as seq_file:
        json.dump(seqs, seq_file)


if __name__ == '__main__':
    main()
