
import argparse
import pytest
from rnamoip.helpers.validation import Validator


def test_raise_exception_on_non_rna_seq():
    with pytest.raises(argparse.ArgumentTypeError):
        Validator.validate_rna_seq("Ce n'est pas une séquence RNA")


def test_validate_rna_seq():
    assert Validator.validate_rna_seq('ACGU') == 'ACGU'


def test_validate_lower_case_rna_seq():
    assert Validator.validate_rna_seq('accguag') == 'ACCGUAG'
