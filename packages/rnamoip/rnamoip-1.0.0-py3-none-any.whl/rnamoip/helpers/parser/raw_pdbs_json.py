from itertools import chain
import json
from pathlib import Path
import os

from rnamoip.analysis.model.chain import Chain
from rnamoip.analysis.model.pdb import PDB
from rnamoip.helpers.sequence import SequenceHelper
from rnamoip.helpers.structure import StructureHelper


class RawPDBParser:
    file_name = 'seq_bps.json'

    @classmethod
    def parse_folder(cls, folder_path: Path) -> list[PDB]:
        # Make sure path exists
        if not os.path.exists(folder_path):
            raise OSError(f'The path {folder_path} does not exists.')

        file_path = os.path.join(folder_path, cls.file_name)
        if not os.path.exists(file_path):
            raise OSError(f'The path {file_path} does not exists.')

        with open(file_path, 'r') as f:
            json_data = json.load(f)

        pdbs = []
        for pdb_name, pdb_info in json_data.items():
            chain_list = []
            for chain_name, chain_info in pdb_info.items():
                pairings_list = chain_info['bps']
                sequence = chain_info['seq']
                pairings = map(
                    lambda nucs: (nucs[0], nucs[1]),
                    pairings_list,
                )
                canons_pairs = SequenceHelper.filter_canonical_pair(sequence, pairings)
                pairings_per_lvl, secondary_strucure = StructureHelper.pairings_to_str(canons_pairs, len(sequence))
                new_pairings_per_lvl = StructureHelper.remove_lonely_pairings_with_lvl(pairings_per_lvl)
                new_pairings = list(chain(*new_pairings_per_lvl.values()))
                chain_list.append(Chain(chain_name, pdb_name, sequence, new_pairings))
            pdbs.append(PDB(pdb_name, chain_list))
        return pdbs
