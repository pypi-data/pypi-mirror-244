
import json
import os
from dataclasses import asdict
from functools import lru_cache

from Bio import AlignIO

from rnamoip.helpers.parser.raw_pdbs_json import RawPDBParser
from rnamoip.parse_raw_pdbs import filter_unique_and_pick_repr


@lru_cache
def get_chains_with_alignemnts() -> list[str]:
    chains_with_ali_file = os.path.join('data', 'alignment', 'all_chains_with_ali.json')
    aligments_with_chains = []
    with open(chains_with_ali_file) as ali_file:
        aligments_with_chains = json.load(ali_file)
    return aligments_with_chains


def prepare_chains_for_ali_file():
    chains_list = get_chains_with_alignemnts()

    pdbs_folder = os.path.join('data', 'pdb')
    all_pdbs = RawPDBParser.parse_folder(pdbs_folder)
    all_chains = [chain for pdb in all_pdbs for chain in pdb.chains]

    chains_present = [chain for chain in all_chains if chain.full_name in chains_list]

    print(f'Number of chains in alignments: {len(chains_list)}')
    print(f'Number of chains in seq_bps: {len(chains_present)}')

    # Keep only unique
    unique_chains = filter_unique_and_pick_repr(chains_present)

    print(f'Chains unique and representative: {len(unique_chains)}')
    with open(os.path.join('data', 'alignment', 'chains_with_ali.json'), 'w') as outfile:
        dict_list = [asdict(chain) for chain in unique_chains]
        json.dump(dict_list, outfile, indent=2)


def main():
    ali_file_name = os.path.join('data', 'alignment', 'Rfam.3d.seed')
    ali_out_file = os.path.join('data', 'alignment', 'alignments_with_chains.json')
    chains_with_ali_file = os.path.join('data', 'alignment', 'all_chains_with_ali.json')
    aligments_with_chains = []
    all_chains: list[tuple[str, str, str, str]] = []
    alignments = AlignIO.parse(ali_file_name, "stockholm")
    for ali in alignments:
        # Based on a somewhat format from BioPython
        annotations = ali._annotations.items()

        # Create a tuple of the pdb with his alignment id and positions
        chains_list: list[tuple[str, str, str, str]] = []
        for id_str_with_pos, pdbs_with_ss in annotations:
            id, pos_str = id_str_with_pos.split('/')

            # Retrieve the corresponding sequence with the pos
            ali_sequence = [seq_rec.seq for seq_rec in ali if seq_rec.id == id_str_with_pos]
            assert len(ali_sequence) != 0, f'Missing id {id} in alignment.'
            assert len(ali_sequence) == 1, f'Duplicate id {id} in alignment.'
            start, end = pos_str.split('-')
            start, end = int(start), int(end)
            record = ali_sequence[0]
            for pdb, ss in pdbs_with_ss.items():
                chain = '-'.join(pdb.split('_')[0:2])
                chains_list.append((chain, id_str_with_pos, pos_str, str(record)))

        print(chains_list)
        seq_list = []
        for seq in ali:
            seq_list.append(str(seq.seq))

        aligments_with_chains.append({
            'chains': chains_list,
            'alignments': seq_list,
        })
        all_chains.extend([chain[0] for chain in chains_list])

    with open(ali_out_file, 'wt') as ali_out:
        json.dump(aligments_with_chains, ali_out, indent=2)

    with open(chains_with_ali_file, 'wt') as chain_out:
        json.dump(all_chains, chain_out, indent=2)


if __name__ == '__main__':
    main()
    prepare_chains_for_ali_file()
