
import json
import os
from dataclasses import asdict

from rnamoip.helpers.parser.raw_pdbs_json import RawPDBParser


kinks_turns = [
    '4GXY-A',
    '4AOB-A',
    '4KQY-A',
    '5FJC-A',
    '3V7E-C',
]


def prepare_chains_for_ali_file():
    pdbs_folder = os.path.join('data', 'pdb')
    all_pdbs = RawPDBParser.parse_folder(pdbs_folder)
    kink_turns_chains = [
        chain for pdb in all_pdbs for chain in pdb.chains
        if chain.full_name in kinks_turns
    ]
    print(f'Number of chains with kink turn in alignments: {len(kink_turns_chains)}')
    with open(os.path.join('data', 'kink_turn', 'kink_turn_chains_with_ali.json'), 'w') as outfile:
        dict_list = [asdict(chain) for chain in kink_turns_chains]
        json.dump(dict_list, outfile, indent=2)


if __name__ == '__main__':
    prepare_chains_for_ali_file()
