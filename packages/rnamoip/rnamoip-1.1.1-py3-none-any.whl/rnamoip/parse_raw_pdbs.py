
import csv
# from dataclasses import asdict
import logging
# import json
import os

from rnamoip import logger
from rnamoip.analysis.model.chain import Chain
from rnamoip.helpers.parser.raw_pdbs_json import RawPDBParser

nrlist_file_path = os.path.join('..', 'data', 'pdb', 'nrlist_3.208_all.csv')


def remove_middle_component(element: str):
    comps = element.split('|')
    return '-'.join([comps[0], comps[2]])


def add_corresponding_chain(chain: Chain, nr: str, nr_dict, pdb_per_unique_sequence) -> bool:
    if chain.sequence in pdb_per_unique_sequence:
        logging.warn(f"Skipping chain {chain.full_name}")
        logging.warn('Multiple pdb with the same sequences:')
        logging.warn(f'Sequence: {chain.sequence}')
        return False
    chain.nr = nr
    nr_dict.pop(nr)
    pdb_per_unique_sequence.setdefault(chain.sequence, []).append(chain.full_name)
    return True


def parse_nrlist(nrlist_file_name):
    nr_dict = {}
    with open(nrlist_file_name, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line in csv_reader:
            id = line[0]
            nr_dict[id] = {
                'repr': [remove_middle_component(elem) for elem in line[1].split('+')],
                'members': [
                    remove_middle_component(elem)
                    for members in line[2].split(',')
                    for elem in members.split('+')
                ],
            }
    return nr_dict


def get_class_members_of_repr(repr, nr_dict):
    for values in nr_dict.values():
        if repr in values['repr']:
            return values['members']
    for values in nr_dict.values():
        if repr in values['members']:
            return values['members']
    return [repr]


def filter_unique_and_pick_repr(chains):
    nr_dict = parse_nrlist(nrlist_file_path)

    logging.info(f'Found "{len(nr_dict.values())}" possibles entries in nr.')
    final_chains = []
    pdb_per_unique_sequence: dict[str, list] = {}
    # First loop to Check for representative in our list
    for chain in chains:
        for key, nr in nr_dict.items():
            if chain.full_name in nr['repr']:
                if add_corresponding_chain(chain, key, nr_dict, pdb_per_unique_sequence):
                    final_chains.append(chain)
                    break

    logging.info(f'Match "{len(final_chains)}" chain with representative.')
    for chain in [c for c in chains if c not in final_chains]:
        for key, nr in nr_dict.items():
            if chain.full_name in nr['members']:
                if add_corresponding_chain(chain, key, nr_dict, pdb_per_unique_sequence):
                    final_chains.append(chain)
                    break
    return final_chains


def main():
    logger.init('parsing_pdbs.log')
    pdbs = RawPDBParser.parse_folder('../../CATALOGUE/')
    chains = [chain for pdb in pdbs for chain in pdb.chains]
    final_chains = filter_unique_and_pick_repr(chains)

    logging.info(f'Match "{len(final_chains)}" chain in total.')
    # with open('chains.json', 'w') as outfile:
    #     dict_list = [asdict(chain) for chain in final_chains]
    #     json.dump(dict_list, outfile, indent=2)


if __name__ == '__main__':
    main()
