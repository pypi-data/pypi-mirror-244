
import argparse

from rnamoip import logger

from rnamoip.predicter import Predicter
from rnamoip.helpers.validation import Validator


def main():
    logger.init('rnamoip.log')
    parser = argparse.ArgumentParser(
        prog="RNAMoIP v2.0", description="IP RNA structures predicter.",
    )
    parser.add_argument('--configuration_file', dest='configuration_file', type=Validator.validate_file_path,
                        required=False, help='The path to the file containing the configurations.')
    parser.add_argument('--sequence', dest='sequence', type=Validator.validate_rna_seq,
                        required=False, help='The RNA Sequence.')
    parser.add_argument('--structure', dest='structure', type=Validator.validate_secondary_struct,
                        required=False, help='Theinitial secondary strcuture as constraints for the prediction.')
    parser.add_argument('--alpha', dest='alpha', type=float,
                        required=False, help='''
                        The alpha parameter for RNAMoIP algorithm, between 0 and 1. An alpha close to zero prioritize
                        more base pairing coverage, and an alpha closer to 1 prioritize motif insertion as an objective.
                        ''')
    args = parser.parse_args()

    predicter = Predicter(
        configuration_file=args.configuration_file,
        rna_sequence=args.sequence,
        secondary_structure=args.structure,
        alpha=args.alpha,
    )

    predicter.iterate()


if __name__ == '__main__':
    main()
