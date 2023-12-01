import argparse
import os
from pathlib import Path
from .structure import StructureHelper
from .sequence import IUPACConverter


class Validator:
    @staticmethod
    def validate_file_path(path: Path) -> Path:
        if not os.path.isfile(path):
            raise argparse.ArgumentTypeError(
                f"The path for the file '{path}' is not a valid path.")
        return path

    @staticmethod
    def validate_path(path: Path) -> Path:
        if not os.path.exists(path):
            raise argparse.ArgumentTypeError(
                f"The path '{path}' is not a valid path.")
        return path

    @staticmethod
    def validate_rna_seq(value: str, is_alignment=False) -> str:
        """
        Validate a RNA Sequence as a string input.
        @param value: a sequence as a string.
        @param is_alignment: Indicating if the sequence is from an alignment.
        @returns: A validated RNA sequence, upper cased.
        """
        if len(value) == 0:
            raise argparse.ArgumentTypeError("The value RNA sequence is empty.")
        rna_seq = value.upper()
        correct_nucs = IUPACConverter.POSSIBLE_VALUES
        if any(n not in correct_nucs for n in rna_seq):
            raise argparse.ArgumentTypeError(f"The value '{rna_seq}' is not a valid RNA sequence.")
        return rna_seq

    @staticmethod
    def validate_secondary_struct(structure: str, max_level: int) -> str:
        """
            Validate a secondary structure as a string input, hile verifying for
            invalid pairings inside.
            @param structure: a structure as a string.
            @returns: A validated RNA structure.
        """
        valid_chars = ''.join([
            StructureHelper.PAIRING_LEFT_CHAR[0:max_level],
            StructureHelper.PAIRING_RIGHT_CHAR[0:max_level],
            '.',
        ])
        if any(p not in valid_chars for p in structure):
            raise argparse.ArgumentTypeError(
                f"The value '{structure}' is not a valid RNA secondary structure.",
            )

        try:
            StructureHelper.find_base_pairings_with_level(structure, max_level)
        except Exception as e:
            raise argparse.ArgumentTypeError(f"""
                The value '{structure}' is not a valid RNA secondary:
                {str(e)}
            """)
        return structure

    @staticmethod
    def validate_alignment(alignments: list[str]) -> list[str]:
        validate_alignments = []
        seq_length = len(alignments[0])
        for seq in alignments:
            if len(seq) != seq_length:
                raise Exception('Sequences in alignment need to be the same length.')
            validate_alignments.append(Validator.validate_rna_seq(seq, is_alignment=True))
        return validate_alignments

    @staticmethod
    def validate_parser(parser: str):
        valid_parsers = ['desc', 'rin']
        if parser not in valid_parsers:
            raise argparse.ArgumentTypeError(
                f"Invalid parser selected. Valid choices are '{valid_parsers}'.",
            )

    @staticmethod
    def validate_max_solution_count(solution_count: int):
        if type(solution_count) is not int:
            raise argparse.ArgumentTypeError(
                'Maximum solution count is not an integer.',
            )
        if solution_count < 1:
            raise argparse.ArgumentTypeError(
                'Maximum solution count should be superior or equal to 1.',
            )
