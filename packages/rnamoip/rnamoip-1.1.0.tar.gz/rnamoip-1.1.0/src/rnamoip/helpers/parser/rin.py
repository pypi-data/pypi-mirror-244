
import json
import os
from functools import lru_cache
from importlib.resources import files
from pathlib import Path
from typing import Any, Optional

from ...database.model.motif import Motif
from ...database.model.strand import Strand


class RinParser:
    @classmethod
    @lru_cache
    def parse_folder(cls, rins_path: Optional[Path]) -> list[Any]:
        # Make sure path exists
        if rins_path and not os.path.exists(rins_path):
            raise OSError(f'The path {rins_path} does not exists')

        elif not rins_path:
            # Default to RNAMoIP packaged rins
            rins_path = files('rnamoip').joinpath('data', 'rins.json')

        with open(rins_path, 'r') as rins_file:
            rin_list_dict = json.load(rins_file)
        motifs = []
        for index, (seq, rin_info) in enumerate(rin_list_dict.items()):
            # Create a Motif for all rins
            pseudoknotable_table = rin_info.get('pseudokontable_pos', [])
            strands = []
            index = 0
            for sub_seq in seq.split('-'):
                pseudoknotable_list = pseudoknotable_table[index:index + len(sub_seq)]
                strands.append(Strand(sub_seq, pseudoknotable_list))
                index += len(sub_seq)
            related_rins = set([occ['rin_id'] for occ in rin_info['occurences']])
            motifs.append(Motif(strands, seq, list(related_rins)))
        return motifs


if __name__ == '__main__':
    rin_list = RinParser.parse_folder('.')
