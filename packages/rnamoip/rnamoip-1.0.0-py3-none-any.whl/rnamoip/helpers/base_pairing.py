
from typing import Union
import RNA

from ..database.model.common import Pairing


class BasePairingProbaHelper:
    BASE_PAIRING_WEIGHT = 10

    @classmethod
    def get_base_pairing_proba(
        cls,
        sequence: str,
        minimum_probability: float,
        minimum_pairing_distance: int,
    ) -> dict[Pairing: float]:
        basepair_probs = BasePairingProbaHelper._fold_structure(sequence)
        return cls._extract_probabilities(basepair_probs, minimum_probability, minimum_pairing_distance)

    @classmethod
    def get_base_pairings_proba_with_sc(
        cls,
        sequence: str,
        structure: str,
        minimum_probability: float,
        minimum_pairing_distance: int,
    ):
        basepair_probs = BasePairingProbaHelper._fold_structure(sequence, structure)
        return cls._extract_probabilities(basepair_probs, minimum_probability, minimum_pairing_distance)

    @classmethod
    def get_base_pairings_proba_with_lvl(
        cls,
        sequence: Union[str, list],
        structure_per_lvl: dict[int, str],
        minimum_probability: float,
        minimum_pairing_distance: int,
    ) -> dict:
        matrix_list = [
            BasePairingProbaHelper._fold_structure(sequence, structure)
            for structure in structure_per_lvl.values()
        ]

        combined_matrix = []
        matrix_zip = list(zip(*matrix_list))
        for row in matrix_zip:
            combined_matrix.append([cls.BASE_PAIRING_WEIGHT * (sum(x) / len(matrix_list)) for x in zip(*row)])

        return cls._extract_probabilities(combined_matrix, minimum_probability, minimum_pairing_distance)

    @staticmethod
    def _fold_structure(
        sequence: Union[str, list],
        structure: str,
    ):
        # ViennaRNA automaticly detect if we have a unique sequence or alignments
        fc = RNA.fold_compound(sequence)
        if structure:
            fc.hc_add_from_db(structure, RNA.CONSTRAINT_DB_DEFAULT | RNA.CONSTRAINT_DB_ENFORCE_BP)
        (propensity, ensemble_energy) = fc.pf()
        basepair_probs = fc.bpp()
        return basepair_probs

    @staticmethod
    def _extract_probabilities(
        basepair_probs,
        minimum_probability: float,
        minimum_pairing_distance: int,
    ) -> dict[Pairing: float]:
        bps = {}
        for i in range(1, len(basepair_probs)):
            for j in range(i + 1, len(basepair_probs[i])):
                if basepair_probs[i][j] > (minimum_probability * 10) and j - i > minimum_pairing_distance:
                    bps[(i - 1, j - 1)] = basepair_probs[i][j]

        # Remove lonely pairings
        lefties = [i for (i, _) in bps.keys()]
        righties = [j for (_, j) in bps.keys()]
        bps_to_remove = []
        for (i, j) in bps.keys():
            if (not i - 1 in lefties and i + 1 in lefties) and \
               (not j - 1 in righties and j + 1 in righties):
                bps_to_remove.append((i, j))

        map(lambda key: bps.pop(key), bps_to_remove)
        return bps
