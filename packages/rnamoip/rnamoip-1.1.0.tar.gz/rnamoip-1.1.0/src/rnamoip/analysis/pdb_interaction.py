
from collections import defaultdict
import os
import csv
import logging

from Bio.PDB import MMCIF2Dict

from rnamoip.analysis.model.interaction import Interaction


PDB_motif_info_dir = os.path.join('..', '..', 'pdb_fr3d')
PDB_motif_cif_dir = os.path.join('..', '..', 'pdb_cif')


def get_position_mapping(pdb_name) -> dict[int, int]:
    file_name = os.path.join(PDB_motif_cif_dir, f'{pdb_name}.cif')
    cif = MMCIF2Dict.MMCIF2Dict(file_name)
    mapping = zip(
        cif['_pdbx_poly_seq_scheme.pdb_strand_id'],
        cif['_pdbx_poly_seq_scheme.seq_id'],
        cif['_pdbx_poly_seq_scheme.pdb_seq_num'],
        cif['_pdbx_poly_seq_scheme.pdb_ins_code'],
        cif['_pdbx_poly_seq_scheme.mon_id'],
    )

    pos_mapping = defaultdict(dict)
    for chain, position, pdb_pos, pdb_ins, nucleotide in mapping:
        # print(nucleotide, position, pdb_pos + (pdb_ins if pdb_ins != '.' else ''))
        pos = pdb_pos + (pdb_ins if pdb_ins != '.' else '')
        pos_mapping[chain][pos] = position

    return pos_mapping


def parse_infos(info: str) -> dict:
    details = info.split('|')
    return {
        'pdb': details[0],
        'model': details[1],
        'chain': details[2],
        'nuc': details[3],
        'pos': details[4],
    }


def parse_pdb_interactions(pdb: str, chain_name: str, csv_reader) -> dict[str, list[Interaction]]:
    pdb_infos = defaultdict(list)
    pos_mapping = get_position_mapping(pdb)
    for line in csv_reader:
        if len(line) <= 1:
            break
        if interaction := line[1]:
            info_start = parse_infos(line[0])
            model_str = info_start['model']
            chain_str = info_start['chain']
            info_end = parse_infos(line[5])
            chain_end = info_end['chain']
            if chain_end != chain_str:
                logging.warn('Interactions between chains, skipping')
                continue
            if chain_name not in [chain_end, chain_str]:
                logging.debug('Not in the chains we want')
                continue
            try:
                start = int(pos_mapping[chain_str][info_start['pos']])
                end = int(pos_mapping[chain_str][info_end['pos']])
            except KeyError:
                logging.exception(f"Error in accessing pos of chain {chain_str} of pdb {pdb}")
                continue
            if interaction[0] == 'n':
                logging.debug(f'Ignoring near interaction {interaction}.')
                continue
            # Don't forget to transform to 0-based index
            interaction = Interaction(
                model=model_str,
                pdb=pdb,
                chain=chain_str,
                type=interaction.upper(),
                type2=interaction,
                start_pos=start - 1,
                start_nuc=info_start['nuc'],
                end_pos=end - 1,
                end_nuc=info_end['nuc'],
            )
            # Check for opposite interaction
            for inter in pdb_infos[model_str]:
                if inter == interaction:
                    break
            else:
                pdb_infos[model_str].append(interaction)
    return pdb_infos


def get_pdb_interaction(pdb, chain_name) -> list[Interaction]:
    pdb_file = os.path.join(PDB_motif_info_dir, f'{pdb}.csv')
    with open(pdb_file, 'r') as pdb_motif_info_csv:
        csv_reader = csv.reader(pdb_motif_info_csv, delimiter=',')
        print(f'Doing pdb {pdb}')
        pdb_infos = parse_pdb_interactions(pdb, chain_name, csv_reader)
    return pdb_infos


if __name__ == '__main__':
    get_pdb_interaction('2GIS', 'A')
