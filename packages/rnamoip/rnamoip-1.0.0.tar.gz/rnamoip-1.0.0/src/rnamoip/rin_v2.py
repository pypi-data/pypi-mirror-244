
import json
import logging
import os
import pickle
import re
import time

from tqdm import tqdm

from rnamoip.helpers.sequence import SequenceHelper, DEFAULT_WILDCARD_THRESHOLD
from rnamoip.scripts._rin_utils import (
    Occurence, Position, RINHolder, SeqsHolder,
)

# basedir = os.path.join('..', '..', '..')
basedir = os.path.join('..', '..')
rins_path = os.path.join(basedir, 'RinV2')
pdb_infos_path = os.path.join(basedir, 'pdb_interactions')
rin_holder_folder = os.path.join(basedir, 'rin_holders')

# Nagagamisis configuration
# basedir = os.path.join('/', 'srv', 'rna')
# rins_path = os.path.join(basedir, 'RNAMoIP2', 'data', 'all_occurrences')
# pdb_infos_path = os.path.join(basedir, 'PDB', 'Src', 'javona-2022-06-29')
# rin_holder_folder = os.path.join('..', '..', 'rin_holders')


def group_rins_by_sequence(rins_holder_list, wildcard_threshold):
    # Find Unique sequence within each RIN
    rins_by_sequence: dict[str, list[RINHolder]] = {}
    for rin in rins_holder_list:
        for seq, occ_list in rin.occ_by_sequence.items():
            sequence_list = [
                (SequenceHelper.get_sequence_from_list(
                    [p for (_, p) in occ.occ_positions], seq, wildcard_threshold,
                ), occ)
                for occ in occ_list
            ]
            for seq, occ in sequence_list:
                if seq:
                    seq_holder = rins_by_sequence.setdefault(seq, SeqsHolder())
                    seq_holder.occurences.append(occ)
                else:
                    logging.warning(f'Wtf no seq? {seq}')
    return rins_by_sequence


def retrieve_pos_mapping(occ_map) -> dict[int, Position]:
    '''
    Retrieve positions mapping from the occurence,
    which has the data as the following format :
    (('BA', 252), ('BA', 456), 0): (14, 15)
    '''
    pos_map = {}
    node_seen = set()
    for (start, end, zero), repr_pair in occ_map.items():
        if start not in node_seen:
            pos_map[repr_pair[0]] = start
            node_seen.add(start)
        if end not in node_seen:
            pos_map[repr_pair[1]] = end
            node_seen.add(end)
    return dict(sorted(pos_map.items()))


def extract_pdb_data(pdb_name: str) -> dict:
    '''
    Extract pdb informations in a directory. Use caching size above the 6031 pdbs.
    '''
    try:
        with open(os.path.join(pdb_infos_path, f'{pdb_name}.nxpickle'), 'rb') as pdb_file:
            return pickle.load(pdb_file)
    except FileNotFoundError:
        logging.warning(f'Could not find the pdb {pdb_name}.')
        return None


def parse_rin_data(rin_data, rin_id: int) -> RINHolder:
    repr = rin_data[0]
    occurences = rin_data[1]
    repr_pos_list = list(repr.nodes())
    rin_holder = RINHolder(rin_id, (rin_id, repr_pos_list))

    pseudoknotable_pos_list: list[list[bool]] = []
    for pdb_name, pdb_occ_list in occurences.items():
        # Open pdb information
        pdb_data = extract_pdb_data(pdb_name)

        # Look for all occurences of that pdb
        for (occ_map, occ_graph) in pdb_occ_list:
            # Retrieve the positions list
            position_map: dict[int, Position] = retrieve_pos_mapping(occ_map)
            # Retrieve sequence
            occ_positions: list[Position] = [position_map[repr_pos] for repr_pos in repr_pos_list]
            sequence = ''.join([occ_graph.nodes[pos]['nt'] for pos in occ_positions])

            # Add it to the list
            rin_holder.occ_by_sequence[sequence].append(Occurence(
                pdb_name,
                chain_name=occ_positions[0][0],
                occ_positions=occ_positions,
                occ_mapping=position_map,
                rin_id=rin_id,
                sequence=sequence,
            ))

            if not pdb_data:
                continue

            # Find if there are pseudoknotable positions in this occurence
            pseudoknotable_pos: list[bool] = [False] * len(occ_positions)
            for index, pos in enumerate(occ_positions):
                node_interactions = pdb_data.edges(pos, data=True)
                # Check if their are cWW or Wobble interactions,
                # External to the rin
                for inter in node_interactions:
                    # Format: ('B', 1), ('B', 20), {'label': 'CWW', 'near': False, 'long_range': False})
                    if inter[1] in occ_positions:
                        continue
                    if inter[2]['label'] == 'CWW':
                        pseudoknotable_pos[index] |= True
            pseudoknotable_pos_list.append(pseudoknotable_pos)

    # Build the final pseudoknotable list
    final_pseudoknotable_list: list[bool] = [False] * len(repr_pos_list)
    for able_list in pseudoknotable_pos_list:
        for index, able in enumerate(able_list):
            final_pseudoknotable_list[index] |= able
    rin_holder.pseudoknotable_pos_list = final_pseudoknotable_list
    return rin_holder


def set_pkable_for_seq_holder(seq_holder_by_sequence: dict[str, SeqsHolder]):
    for seq, seq_holder in seq_holder_by_sequence.items():
        pkable_seq = seq.replace('-', '')
        final_pkable_list: list[bool] = [False] * len(pkable_seq)
        pkable_list_list = []
        for occ in seq_holder['occurences']:
            data = open_rin_holder(occ['rin_id'])
            pkable_list_list.append(data.pseudoknotable_pos_list)
        pkable_index = 0
        for index, (able, nuc) in enumerate(zip(final_pkable_list, pkable_seq)):
            # By default, extra gap are not pseudoknotable
            if nuc == SequenceHelper.ANY_NUCLEOTIDE:
                continue
            for pkable_list in pkable_list_list:
                final_pkable_list[index] |= pkable_list[pkable_index]
            pkable_index += 1
        seq_holder['pseudokontable_pos'] = final_pkable_list


def open_rin_holder(rin_id):
    with open(f'{os.path.join(rin_holder_folder, rin_id)}.pickle', 'rb') as rin_holder_file:
        data = pickle.load(rin_holder_file)
        return data


# import sys
# from rnamoip import scripts
# sys.modules['scripts'] = scripts
def main(rins=None, is_BP2=False):
    rins_holder_list: list[RINHolder] = []
    rin_id_regex = r'(local_rin_)([0-9]+)(\.pickle)'

    if rins:
        rins_file_list = [f'local_rin_{rin}.pickle' for rin in rins]
    else:
        rins_file_list = os.listdir(rins_path)
    for rin_file_str in tqdm(rins_file_list):
        with open(os.path.join(rins_path, rin_file_str), 'rb') as rin_file:
            rin_data = pickle.load(rin_file)
        rin_id = re.search(rin_id_regex, rin_file_str).group(2)
        rin_holder = parse_rin_data(rin_data, rin_id)

        # Optional step if done in multiple pass
        # with open(f'{os.path.join(rin_holder_folder, rin_id)}.pickle', 'wb') as rin_holder_file:
        #     pickle.dump(rin_holder, rin_holder_file)
        with open(f'{os.path.join(rin_holder_folder, rin_id)}.pickle', 'rb') as rin_holder_file:
            rin_holder = pickle.load(rin_holder_file, fix_imports=True)

        rins_holder_list.append(rin_holder)

    # Find Unique sequence within each RIN
    wildcard_threshold = 9999 if is_BP2 else DEFAULT_WILDCARD_THRESHOLD
    rins_by_sequence: dict[str, SeqsHolder] = group_rins_by_sequence(rins_holder_list, wildcard_threshold)

    # Could be done within group_rins_by_sequence instead, but I had to do it manually afterwards,
    # so this step exists.
    # set_pkable_for_seq_holder(rins_by_sequence)

    filename = 'rins_for_bp2_no_threshold.json' if is_BP2 else 'rins.json'
    with open(filename, 'w') as rins_out:
        json_list = {s: seq_holder.to_dict() for s, seq_holder in rins_by_sequence.items()}
        json.dump(json_list, rins_out, indent=2)


def hijack_pkable_to_seq_holder():
    start = time.perf_counter()
    with open('rins.json', 'r') as rins_in:
        rins_by_sequence = json.load(rins_in)
    end = time.perf_counter()
    print(f'Time: {end - start} sec.')

    set_pkable_for_seq_holder(rins_by_sequence)

    with open('rins.json', 'w') as rins_out:
        json_list = {s: seq_holder for s, seq_holder in rins_by_sequence.items()}
        json.dump(json_list, rins_out, indent=2)


if __name__ == '__main__':
    start = time.perf_counter()
    main(is_BP2=True)
    end = time.perf_counter()
    print(f'Time: {end - start}sec')
