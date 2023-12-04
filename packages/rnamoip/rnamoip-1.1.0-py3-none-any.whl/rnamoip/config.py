from importlib.resources import files
from enum import Enum
from typing import Union

from rnamoip.helpers.parser.config import ConfigParser
from rnamoip.helpers.validation import Validator


class Module(str, Enum):
    RNAMOIP = 'rnamoip'
    IPKNOT = 'ipknot'
    COMMON = 'common'


class CommonConfig(str, Enum):
    SEQUENCE = 'sequence'
    SECONDARY_STRUCTURE = 'secondary_structure'
    ALIGNMENT = 'alignment'
    MOTIFS_PATH = 'motifs_path'
    PDB_NAME = 'pdb_name'
    ITERATIVE = 'iterative'
    SOLVER_NAME = 'solver'
    SOLVER_MODE = 'solver_mode'
    ENABLE_DELETE_PAIR_IN_RNAMOIP = 'enable_delete_pair_in_rnamoip'
    MAXIMUM_PERCENTAGE_OF_DELETED_PAIRS = 'maximum_deleted_pairs'
    DELETION_PENALTY = 'deletion_penalty'
    MAXIMUM_COMPLEX_MOTIFS = 'maximum_count_of_complex_motifs'
    ALPHA_WEIGHT = 'alpha_weight'
    MINIMUM_PAIRING_PROBABILITY = 'minimum_pairing_probability'
    MINIMUM_PAIRING_DISTANCE = 'minimum_pairing_distance'
    MINIMUM_PAIRING_COVERAGE = 'minimum_pairing_coverage'
    MAXIMUM_PAIRING_LEVEL = 'maximum_pairing_level'
    MINIMUM_ALIGNMENT_MATCH_THRESHOLD = 'minimum_alignment_match_threshold'
    MAXIMUM_ALIGNMENT_DISTANCE = 'maximum_alignment_distance'
    ENABLE_PSEUDONOTABLE_MOTIF = 'enable_pseudonotable_motif'
    EQUATIONS = 'equations'
    TIME_LIMIT = 'time_limit'
    PARSER = 'parser'
    MAXIMUM_SOLUTION_COUNT = 'maximum_solution_count'


class CommonEquation(str, Enum):
    EQ_NO_LONELY_PAIRING = 'eq_no_lonely_pairings'
    EQ_MINIMUM_PAIRING_COVERAGE = 'eq_minimum_pairing_coverage'


class RNAMoIPConfig(str, Enum):
    EQ4_HAIRPIN_INSERTION = 'eq4_hairpins_insertion'
    EQ5_LOOPS_AND_BULGES_INSERTION = 'eq5_loops_and_bulges_insertion'
    EQ6_FILLED_AT_LEAST_2_UNPAIRED = 'eq6_filled_at_least_2_unpaired'
    EQ7_MAXIMUM_NUMBER_OF_K_JUNCTIONS = 'eq7_maximum_number_of_k_junction'
    EQ8_K_JUNCTIONS_INSERTION = 'eq8_k_junctions_insertion'
    EQ9_10_MOTIFS_COMPLETENESS = 'eq9_10_motifs_completness'
    EQ11_STRANDS_COMPLETENESS = 'eq11_strands_completeness'
    EQ12_INSERTIONS_OVERLAP_PAIRINGS = 'eq12_insertion_overlap_pairings'
    EQ13_PREVENT_STRANDS_OVERLAPPING = 'eq13_prevent_strands_overlapping'
    EQ14_PREVENT_LONELY_BASE_PAIRS = 'eq14_prevent_lonely_base_pairs'
    EQ15_MAXIMUM_DELETED_PAIR = 'eq15_maximum_deleted_pair'
    EQ_PREVENT_INSERTION_ON_PSEUDOKNOT = 'eq_prevent_insertion_on_pseudknot'


class IPKnotConfig(str, Enum):
    EQ_ENFORCE_LVL2_PSEUDOKNOT = 'eq_enforce_lvl2_pseudoknot'
    EQ5_ONE_PAIRING_PER_BASE = 'eq5_one_pairing_per_base'
    EQ6_PAIRING_POSSIBILITIES_CONSTRAINTS = 'eq6_pairings_possibilities_constraints'
    EQ7_ENSURE_CROSSING_IN_SUBLVL = 'eq7_ensure_crossing_in_sublvl'
    EQ8_9_PREVENT_LONELY_BASE_PAIR = 'eq8_9_prevent_lonely_base_pairs'


class Config:
    _default_config = {
        Module.COMMON: {
            CommonConfig.SOLVER_NAME: 'CP-SAT',
            CommonConfig.SOLVER_MODE: 'CBC',
            CommonConfig.SEQUENCE: '',
            CommonConfig.SECONDARY_STRUCTURE: '',
            CommonConfig.ALIGNMENT: [],
            CommonConfig.MOTIFS_PATH: '',
            CommonConfig.PDB_NAME: '',
            CommonConfig.ITERATIVE: True,
            CommonConfig.ENABLE_DELETE_PAIR_IN_RNAMOIP: False,
            CommonConfig.MAXIMUM_PERCENTAGE_OF_DELETED_PAIRS: 0.5,
            CommonConfig.DELETION_PENALTY: 10,
            CommonConfig.MAXIMUM_COMPLEX_MOTIFS: 1,
            CommonConfig.ALPHA_WEIGHT: 0.1,
            CommonConfig.MINIMUM_PAIRING_PROBABILITY: 5e-2,
            CommonConfig.MINIMUM_PAIRING_DISTANCE: 3,
            CommonConfig.MINIMUM_PAIRING_COVERAGE: 0.25,
            CommonConfig.MAXIMUM_PAIRING_LEVEL: 3,
            CommonConfig.MINIMUM_ALIGNMENT_MATCH_THRESHOLD: 0.5,
            CommonConfig.MAXIMUM_ALIGNMENT_DISTANCE: 1,
            CommonConfig.ENABLE_PSEUDONOTABLE_MOTIF: False,
            CommonConfig.TIME_LIMIT: 1e3,
            CommonConfig.PARSER: 'rin',
            CommonConfig.MAXIMUM_SOLUTION_COUNT: 10,
            CommonConfig.EQUATIONS: {
                CommonEquation.EQ_NO_LONELY_PAIRING.value: True,
                CommonEquation.EQ_MINIMUM_PAIRING_COVERAGE.value: True,
            },
        },
        Module.RNAMOIP: {
            RNAMoIPConfig.EQ4_HAIRPIN_INSERTION: True,
            RNAMoIPConfig.EQ5_LOOPS_AND_BULGES_INSERTION: True,
            RNAMoIPConfig.EQ6_FILLED_AT_LEAST_2_UNPAIRED: True,
            RNAMoIPConfig.EQ7_MAXIMUM_NUMBER_OF_K_JUNCTIONS: False,
            RNAMoIPConfig.EQ8_K_JUNCTIONS_INSERTION: True,
            RNAMoIPConfig.EQ9_10_MOTIFS_COMPLETENESS: True,
            RNAMoIPConfig.EQ11_STRANDS_COMPLETENESS: True,
            RNAMoIPConfig.EQ12_INSERTIONS_OVERLAP_PAIRINGS: True,
            RNAMoIPConfig.EQ13_PREVENT_STRANDS_OVERLAPPING: True,
            RNAMoIPConfig.EQ14_PREVENT_LONELY_BASE_PAIRS: False,
            RNAMoIPConfig.EQ15_MAXIMUM_DELETED_PAIR: True,
            RNAMoIPConfig.EQ_PREVENT_INSERTION_ON_PSEUDOKNOT: True,
        },
        Module.IPKNOT: {
            IPKnotConfig.EQ_ENFORCE_LVL2_PSEUDOKNOT: False,
            IPKnotConfig.EQ5_ONE_PAIRING_PER_BASE: True,
            IPKnotConfig.EQ6_PAIRING_POSSIBILITIES_CONSTRAINTS: True,
            IPKnotConfig.EQ7_ENSURE_CROSSING_IN_SUBLVL: True,
            IPKnotConfig.EQ8_9_PREVENT_LONELY_BASE_PAIR: False,
        },
    }

    configuration = dict()

    def __init__(self, configuration_file: Union[str, dict]) -> None:
        if configuration_file:
            config_parser = ConfigParser(configuration_file)
        else:
            config_file = files('rnamoip').joinpath('data', 'configuration.json')
            config_parser = ConfigParser(config_file)
        self.init_parser(config_parser)
        self.validate_config()

    def init_parser(self, config_parser: ConfigParser):
        for module, module_config in self._default_config.items():
            self.configuration.setdefault(module, {})
            for property, default_value in module_config.items():
                # Update if value is present in configuration file
                if (value := config_parser.get_configuration_proprety(property.value, module.value)) is not None:
                    self.configuration[module][property] = value
                else:
                    self.configuration[module][property] = default_value

    def validate_sequence(self):
        if sequence := self.get_property(CommonConfig.SEQUENCE):
            sequence = Validator.validate_rna_seq(sequence)
        # Sequence can either be a str, or a list of alignement (also as string)
        if alignment := self.get_property(CommonConfig.ALIGNMENT):
            alignment = Validator.validate_alignment(alignment)
        return sequence, alignment

    def validate_config(self):
        secondary_struct = self.get_property(CommonConfig.SECONDARY_STRUCTURE)
        sequence, alignment = self.validate_sequence()
        motifs_path = self.get_property(CommonConfig.MOTIFS_PATH)
        parser = self.get_property(CommonConfig.PARSER)
        max_sol_count = self.get_property(CommonConfig.MAXIMUM_SOLUTION_COUNT)
        if not secondary_struct:
            secondary_struct = '.' * len(sequence)
            self.configuration[Module.COMMON][CommonConfig.SECONDARY_STRUCTURE] = secondary_struct

        if len(secondary_struct) != len(sequence):
            raise Exception('The length of the secondary structure and the sequence do not match !')

        maximum_pairing_level = self.get_property(CommonConfig.MAXIMUM_PAIRING_LEVEL)
        if maximum_pairing_level > 4 or maximum_pairing_level < 1:
            raise Exception('The maximum pairing level must be between 1 and 4 (included).')

        Validator.validate_secondary_struct(secondary_struct, maximum_pairing_level)
        if motifs_path:
            Validator.validate_path(motifs_path)
        Validator.validate_parser(parser)
        Validator.validate_max_solution_count(max_sol_count)

    def get_property(self, property: str, module: str = Module.COMMON):
        return self.configuration[module][property]
