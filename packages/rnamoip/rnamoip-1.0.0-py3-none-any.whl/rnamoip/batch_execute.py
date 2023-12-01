
import argparse
import itertools
import json
import logging
import multiprocessing as mp
import os
from pathlib import Path
from typing import Callable

from rnamoip import logger
from rnamoip.analysis.analysis_result import AnalysisResult
from rnamoip.analysis.model.chain import Chain
from rnamoip.execute_pdb import predict_chain, read_chains
from rnamoip.helpers.parser.rin import RinParser
from rnamoip.helpers.validation import Validator
from rnamoip.parse_raw_pdbs import (
    get_class_members_of_repr, nrlist_file_path, parse_nrlist,
)

PDB_LIST = [
    ('3SUX', 'X'),
    ('6G7Z', 'A'),
    ('5AOX', 'C'),
    ('6VMY', 'A'),
    ('2TPK', 'A'),
]


def is_interesting(chain: Chain) -> bool:
    is_it = len(chain.sequence) <= 150
    is_it &= len(chain.sequence) >= 20
    # is_it &= chain.biggest_multiloop >= 3
    # is_it &= len(chain.motifs_list[MotifType.HAIRPIN.value]) >= 1
    # is_it &= len(chain.motifs_list[MotifType.STEM.value]) >= 1
    # is_it &= len(chain.motifs_list[MotifType.INTERIOR_LOOP.value]) >= 1
    is_it &= chain.highest_pseudoknot_lvl >= 1
    return is_it


def listener(queue, alpha):
    """
        listen other process sending data.
    """
    FILENAME = f'pdbs_results_multi_batch{alpha:.2f}.json'
    if not os.path.exists(FILENAME):
        with open(FILENAME, "w") as jsonFile:
            json.dump([], jsonFile, indent=2)
    while True:
        message = queue.get()
        if message == 'kill':
            break
        with open(FILENAME, "r") as jsonFile:
            data = json.load(jsonFile)

        data.append(message)
        with open(FILENAME, "w") as jsonFile:
            json.dump(data, jsonFile, indent=2)


def get_filter_for_specific_pdb(pdb_list) -> Callable:
    def is_pdb_in_list(chain: Chain):
        return (chain.pdb_name, chain.name) in pdb_list
    return is_pdb_in_list


def get_alignments_infos(alifile: Path) -> dict:
    with open(alifile, 'r') as jsonFile:
        alignments = json.load(jsonFile)
    return alignments


def compare_with_gap_seq(chain: Chain, ali_seq: str) -> tuple[int, int]:
    seq = chain.sequence
    for i, s in enumerate(ali_seq):
        if s == '-':
            continue
        index_in_pdb = 0
        for index_in_ali, t in enumerate(ali_seq[i:]):
            if t == '-':
                continue
            if t != seq[index_in_pdb]:
                # Not the subsequence
                break
            index_in_pdb += 1
            if index_in_pdb == len(seq):
                # Pdb sequence all found
                return i, index_in_ali + i
        else:
            # We didn't reach the end of the seq, but this is the longest subseq in ali.
            logging.warn(f'''
                Sequence of chain {chain.full_name} is potentially longer ({len(chain.sequence)})
                than the alignement without gap {len([c for c in ali_seq if c != '-'])}.
            ''')
            return i, index_in_ali + i
    return i, index_in_ali


def get_alignments(chain: Chain, alignments_list) -> list[str]:
    chain_name = chain.full_name
    ali = None
    for alignments in alignments_list:
        chains_infos = alignments['chains']
        for chain_info in chains_infos:
            if chain_name == chain_info[0]:
                ali = alignments['alignments']
                # Retrieve the correct position to align
                ali_seq = chain_info[3]
                start, end = compare_with_gap_seq(chain, ali_seq)
                croped_ali_seq = ali_seq[start: end + 1]
                croped_ali = []
                gap_positions = [i for i, c in enumerate(croped_ali_seq) if c == '-']
                for seq in ali:
                    croped = seq[start: end + 1]
                    ungaped_ali = ''.join([c for i, c in enumerate(croped) if i not in gap_positions])
                    croped_ali.append(ungaped_ali)
                return croped_ali
    logging.warning(f'Did not find chain {chain_name} in the RFAM alignments...')
    return ali


def batch_execute(
    chains_list: list[Chain],
    alpha: float = None,
    single_process=False,
    motifs_path: Path = '../CATALOGUE/No_Redondance_DESC/',
    add_alignments=False,
    use_gurobi=False,
) -> list[AnalysisResult]:
    ali_file_name = os.path.join('..', 'data', 'alignment', 'alignments_with_chains.json')
    nr_dict = parse_nrlist(nrlist_file_path)
    rins_data = RinParser.parse_folder(motifs_path)
    if add_alignments:
        alignments_dict = get_alignments_infos(ali_file_name)
    if single_process:
        result_list = []
        for chain in chains_list:
            pdbs_to_ignore = get_class_members_of_repr(chain.full_name, nr_dict)
            alignments = get_alignments(chain, alignments_dict) if add_alignments else None
            result = predict_chain(
                chain,
                alpha,
                motifs_path=motifs_path,
                pdbs_to_ignore=pdbs_to_ignore,
                alignments=alignments,
                use_Gurobi=use_gurobi,
                rins=rins_data,
            )
            result_list.append(result)
        return result_list
    else:
        manager = mp.Manager()
        q = manager.Queue()
        with mp.Pool() as pool:
            watcher = pool.apply_async(listener, (q, alpha))

            pdbs_to_ignore_list = [
                get_class_members_of_repr(chain.full_name, nr_dict)
                for chain in chains_list
            ]
            if add_alignments:
                alignments = [
                    get_alignments(chain, alignments_dict) for chain in chains_list
                ]
            else:
                alignments = itertools.repeat(None)
            inputs_list = list(zip(
                chains_list,
                itertools.repeat(alpha),
                itertools.repeat(motifs_path),
                pdbs_to_ignore_list,
                alignments,
                itertools.repeat(q),
                itertools.repeat(use_gurobi),
                itertools.repeat(rins_data),
            ))
            jobs = pool.starmap_async(predict_chain, inputs_list)
            # jobs = pool.starmap(predict_chain, inputs_list)

            # collect results from the workers through the pool result queue
            jobs.get()
            q.put('kill')
            watcher.get()


def parse_args():
    logger.init('batch.log')
    parser = argparse.ArgumentParser(
        prog="RNAMoIP Multibatch", description="IP RNA structures predicter in multi batch.",
    )
    parser.add_argument('--single_process', action='store_true', help='Execute sequencially.')
    parser.add_argument('--add_alignments', action='store_true', help='Add alignments.')
    parser.add_argument('--use_gurobi', action='store_true', default=False, help='Use gurobi environment.')
    parser.add_argument(
        '--motifs_path',
        dest='motifs_path',
        type=Validator.validate_path,
        help='The path to the file containing the configurations.',
    )
    parser.add_argument(
        '--chains_source',
        dest='chains_source',
        type=Validator.validate_file_path,
        default='../data/chain/chains.json',
        help='The path to the file containing the chains.',
    )
    return parser.parse_args()


def main():
    args = parse_args()
    result_file = 'pdbs_results.json'
    # filter_function = get_filter_for_specific_pdb(PDB_LIST)
    filter_function = is_interesting
    chain_list = read_chains(args.chains_source)
    chains_interesting = list(filter(lambda c: filter_function(c), chain_list))
    print(f'Found {len(chains_interesting)} chains with the corresponding criteria.')

    result_list = batch_execute(
        chains_interesting,
        single_process=args.single_process,
        motifs_path=args.motifs_path,
        add_alignments=args.add_alignments,
        use_gurobi=args.use_gurobi,
        alpha=0.10,
    )

    with open(result_file, 'w') as json_file:
        json.dump(result_list, json_file, indent=2)


if __name__ == '__main__':
    main()
