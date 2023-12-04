
import json
import logging
import os
from pathlib import Path

import gurobipy as gp

from rnamoip import logger
from rnamoip.analysis.analysis_result import AnalysisResult
from rnamoip.analysis.model.chain import Chain
from rnamoip.helpers.parser.rin import RinParser
from rnamoip.predicter import Predicter

PDB_ID = '1L2X'
CHAIN_NAME = 'A'
RESULT_FILE = 'pdbs_results.json'


def filter_specific_pdb(chain: Chain) -> bool:
    return chain.pdb_name == PDB_ID and (not CHAIN_NAME or chain.name == CHAIN_NAME)


def predict_chain(
    chain: Chain,
    alpha: float = None,
    motifs_path: Path = None,
    pdbs_to_ignore: list = [],
    alignments: list[str] = None,
    queue=None,
    use_Gurobi: bool = False,
    rins: dict = None,
):
    predicter_args = {
        'rna_sequence': chain.sequence,
        'motifs_path': motifs_path,
        'pdb_name': chain.pdb_name,
        'pdbs_to_ignore': pdbs_to_ignore,
        'alpha': alpha,
        'alignment': alignments,
        'motifs': rins,
        'secondary_structure': chain.inital_ss,
    }
    try:
        if use_Gurobi:
            with gp.Env() as env:
                predicter = Predicter(
                    **predicter_args,
                    gurobi_env=env,
                )

            result = predicter.iterate()
            predicter.dispose()
        else:
            predicter = Predicter(**predicter_args)
            result = predicter.iterate()
            predicter.dispose()
    except Exception as e:
        logging.error(f"Exception while prediction pdb '{chain.full_name}' at alpha '{alpha}'.")
        raise e

    rnafold_seq = alignments if alignments else chain.sequence
    analysis_result = AnalysisResult(
        pdb_name=chain.pdb_name,
        chain_name=chain.name,
        sequence_original=chain.sequence,
        pdb_ori_structure=chain.secondary_structure,
        initial_structure=result.initial_structure,
        original_motifs=chain.motifs_list,
        rnamoip_structure=result.new_structure,
        rnafold_structure=chain.rnafold_ss(rnafold_seq),
        motifs_structuree=result.motif_sequence,
        highest_junctions=chain.biggest_multiloop,
        highest_pseudoknot_lvl=chain.highest_pseudoknot_lvl,
        alignments=predicter.alignment,
        motifs_inserted=result.motifs,
        iteration_count=result.iterations_count,
        execution_time_in_sec=result.execution_time_in_sec,
        solutions_count=result.solutions_count,
        solution_score=result.solution_score,
        solution_code=result.solution_code,
        solution_list=result.solutions_list,
        alpha=result.alpha,
        motif_type=result.motif_type,
    )

    result = analysis_result.asdict()
    if queue:
        queue.put(result)
    return result


def execute_pdb(chain: Chain, rins_data=None):
    result_list = [predict_chain(chain, rins=rins_data)]
    if os.path.isfile(RESULT_FILE):
        with open(RESULT_FILE, 'r') as json_file:
            result_list.extend(json.load(json_file))

    with open(RESULT_FILE, 'w') as json_file:
        json.dump(result_list, json_file, indent=2)


def read_chains(file_path) -> list[Chain]:
    with open(file_path, 'r') as jsonfile:
        chains_json = json.load(jsonfile)

    chain_list = [
        Chain(chain_dict['name'], chain_dict['pdb_name'], chain_dict['sequence'], chain_dict['bps'])
        for chain_dict in chains_json
    ]
    return chain_list


def main(pdb_source, filter_function):
    logger.init('execute_pdb.log')
    chain_list = read_chains(pdb_source)
    chains_interesting = list(filter(lambda c: filter_function(c), chain_list))
    print(f'Found {len(chains_interesting)} chains with the corresponding criteria.')

    rins_data: dict = RinParser.parse_folder()
    for chain in chains_interesting:
        execute_pdb(chain, rins_data)


if __name__ == '__main__':
    pdb_source = '../data/chain/chains.json'
    filter_function = filter_specific_pdb
    main(pdb_source, filter_function)
