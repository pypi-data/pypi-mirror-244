
from functools import lru_cache
import logging
from pathlib import Path
import os

from ...database.model.motif import Motif
from ..sequence import SequenceHelper


class DescParser:
    MOTIF_FILE_EXTENSION = '.desc'

    @classmethod
    @lru_cache
    def parse_folder(cls, folder_path: Path) -> list[Motif]:
        # Make sure path exists
        if not folder_path:
            raise Exception('The path to desc motifs database must be provided.')

        if not os.path.exists(folder_path):
            raise OSError(f'The path {folder_path} does not exists')

        motifs_file_list = [f for f in os.listdir(folder_path)
                            if f.endswith(cls.MOTIF_FILE_EXTENSION)]

        motifs = []
        for motif_file in motifs_file_list:
            with open(os.path.join(folder_path, motif_file), 'r') as f:
                # Skip first line
                f.readline()
                desc_line = f.readline().split(':')[1]
                strands = SequenceHelper.get_strands_of_desc_line(
                    desc_line.strip(),
                )
                if strands is None or len(strands) == 0:
                    logging.warn(f"Error in the motif file '{motif_file}'.")
                    continue

                motifs.append(Motif(name=os.path.basename(motif_file), strands=strands))
        return motifs
