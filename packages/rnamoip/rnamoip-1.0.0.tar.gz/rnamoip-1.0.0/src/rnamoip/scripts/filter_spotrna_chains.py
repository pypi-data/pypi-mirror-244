# This script is use to filter out any chains that was use in
# SPOT-RNA training / validation from the chains list
# https://www.dropbox.com/s/apqrsl7hm1091ie/PDB_dataset.tar.xz

import os
from rnamoip.analysis.model.chain import Chain
from rnamoip.parse_raw_pdbs import get_class_members_of_repr, parse_nrlist, nrlist_file_path
from rnamoip.batch_execute import is_interesting

from rnamoip.execute_pdb import read_chains

PDB_DATASET_DIR = os.path.join('/', 'Users', 'gloyer', 'School', 'benchmark', 'Training_SPOT-RNA', 'PDB_dataset')


def read_training_dir():
    # Walk the dataset dir to find all pdb (all filenames)
    training_pdbs = []
    for root, dirs, files in os.walk(PDB_DATASET_DIR):
        for name in files:
            chain_name = name.split('.')[0].upper()
            # In RNAMoip, its <PDB_Name>-<chainname>
            # In SpotRNA, its <pdb_name>-<chain letter 1>-<chain letter 2>
            if chain_name.count('-') == 2:
                split = chain_name.split('-')
                chain_name = ''.join([split[0], '-', *split[2:]])
            if chain_name.count('_') == 2:
                split = chain_name.split('_')
                chain_name = ''.join([split[0], '-', *split[1:]])
            elif chain_name.count('_') == 1:
                split = chain_name.split('_')
                chain_name = ''.join([split[0], '-', *split[1:]])
            training_pdbs.append(chain_name)
    return training_pdbs


def filter_chains(training_pdbs: list[str]):
    chain_source = '../data/chain/chains.json'
    chain_list = read_chains(chain_source)
    chain_list = list(filter(lambda c: is_interesting(c), chain_list))

    nr_dict = parse_nrlist(nrlist_file_path)
    all_trainings_members = []
    for chain in training_pdbs:
        members = get_class_members_of_repr(chain, nr_dict)
        all_trainings_members.extend(members)

    filtered_chains = []
    for chain in chain_list:
        if chain.full_name in training_pdbs:
            continue
        # Check for non-redundancy in the family
        if chain.full_name in all_trainings_members:
            continue
        filtered_chains.append(chain)
    return filtered_chains


def write_filtered_chain(filtered_chains: list[Chain]):
    os.makedirs('../chains/input_spotrna', exist_ok=True)
    for chain in filtered_chains:
        with open(f'../chains/input_spotrna/{chain.full_name}.fasta', 'wt') as fasta_out:
            fasta_out.writelines([
                f'>{chain.full_name}\n',
                f'{chain.sequence}\n',
            ])


if __name__ == '__main__':
    training_pdbs = read_training_dir()
    filtered_chains = filter_chains(training_pdbs)

    print(len(filtered_chains))

    # Out for benchmark
    write_filtered_chain(filtered_chains)
