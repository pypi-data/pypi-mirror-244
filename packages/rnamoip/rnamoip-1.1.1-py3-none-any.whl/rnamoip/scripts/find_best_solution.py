
import json
import os
from collections import defaultdict
from dataclasses import asdict

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from rnamoip.add_interactions_results import get_rin_data
from rnamoip.analysis.analysis_result import AnalysisResult
from rnamoip.analysis.comparer import (
    InteractionResult, InteractionType,
)
from rnamoip.analysis.comparer_result import ComparerResult
from rnamoip.analysis.pdb_interaction import get_pdb_interaction
from rnamoip.compare_tools import get_optimal_and_best_sol, get_rnamoip_result, open_solutions_of_result_file

base_result_dir = '../results/multi_sols'
result_filename = 'pdbs_results_multi_batch0.10.json'
gurobi_file = os.path.join(base_result_dir, '1_gurobi', result_filename)
google_file = os.path.join(base_result_dir, '2_google_time_1e4', result_filename)
alpha = '0.10'
METRIC = 'Sensitivity'
INTERACTION_TYPE = InteractionType.CANONICAL
SOL_NAME = 'Best of 10; α=0.10'


def do_violin_graph(score_df, filename: str):
    line_median = np.median(score_df[score_df['Tool'] == 'RNAFold'][METRIC])
    # score_df = score_df.melt('chain_name', var_name='Alpha', value_name='Score F1')
    sns.set(font_scale=1.50)
    plt.rcParams["xtick.labelsize"] = 14
    plt.rcParams["figure.figsize"] = (10, 7)
    ax = sns.violinplot(
        data=score_df,
        x='Tool',
        y=METRIC,
        # hue='Tool',
        scale="area",
        cut=0,
        bw=.2,
        inner="box",
    )
    ax.set_xticklabels(ax.get_xticklabels())
    plt.axhline(y=line_median, linestyle='--', color='r', alpha=0.8)
    ax.set(xlabel='')
    plt.ylim(0, 1)
    plt.savefig(f'z_output/{filename}_{METRIC.replace(" ", "_")}.png')
    # plt.show()


def get_records(comparer_results, name):
    records = []
    for res in comparer_results:
        records.append({
            # 'chain_name': chain.full_name,
            'Tool': name,
            METRIC: res.get_metric(METRIC, INTERACTION_TYPE),
        })
    return records


def pairings():
    # gurobi_results = open_solutions_of_result_file(gurobi_file)
    google_results = open_solutions_of_result_file(google_file)

    records = []

    # Add RNAFold
    result_file = '../results/memoire/pdbs_results_multi_batch.json'
    with open(result_file, 'r') as json_file:
        results_dict = json.load(json_file)
    RNAfold_result = []
    for chain_dict in results_dict['0.00']:
        RNAfold_result.append(ComparerResult(**chain_dict['rnafold_result']))
    records.extend(get_records(RNAfold_result, 'RNAFold'))

    # Add regular views
    for alpha in ['0.00', '0.05', '0.10', '0.15', '1.00']:
        result = get_rnamoip_result(alpha=alpha, result_file=result_file)
        records.extend(get_records(result.values(), alpha))

    # # Add Optimal
    # for name, res in [('Gurobi', gurobi_results), ('Or-tools', google_results)]:
    #     print('#################')
    #     print(f'{name}')
    #     optimal_solutions, best_solutions = analyse_sol_res(res)
    #     print(f'{name}')
    #     print('#################')

        # records.extend(get_records(optimal_solutions, f'Optimal {name}'))
        # records.extend(get_records(best_solutions, f'Best {name}'))
    optimal_solutions, best_solutions = get_optimal_and_best_sol(google_results)
    records.extend(get_records([res['compare_result'] for res in best_solutions], SOL_NAME))
    # Compare all of them
    result_df = pd.DataFrame.from_records(records)
    do_violin_graph(result_df, 'result')


def motifs():
    google_results = open_solutions_of_result_file(google_file)
    records = []

    result_file = '../results/memoire/pdbs_results_multi_batch_updated.json'
    with open(result_file, 'r') as json_file:
        results_dict = json.load(json_file)
    for alpha, chain_list in results_dict.items():
        if alpha == '0.00':
            continue
        results = []
        for chain_dict in chain_list:
            results.append(InteractionResult(**chain_dict['interactions_result']))
        records.extend(get_records(results, alpha))

    best_interactions_res_file = 'best_solution.json'
    if os.path.exists(best_interactions_res_file):
        with open('best_solution.json', 'r') as json_file:
            json_data = json.load(json_file)
            best_interactions = [InteractionResult(**res) for res in json_data]

    else:
        optimal_solutions, best_solutions = get_optimal_and_best_sol(google_results)

        # Get best Solution interactions
        motifs_count = defaultdict(dict)
        motifs_count['motifs_count_in_pdb'] = 0
        motifs_count['motifs_count_in_pdb_no_canonique'] = 0
        motifs_count['motifs_count_in_pdb_no_non_canonique'] = 0
        best_interactions = []
        for sol in best_solutions:
            # Get PDB interactions
            pdb = sol['pdb_name']
            chain_name = sol['chain_name']
            motifs_inserted = sol['motifs']
            pdb_interactions = get_pdb_interaction(pdb, chain_name)
            rins_data = {}
            # Retrieve all related rins
            rins_related = set()
            for motif in motifs_inserted.values():
                # Get RIN interactions in range of motif
                rins_related.update([int(mr) for mr in motif['related_rins']])

            # Retrieve the rins data missing
            knows_rins = set(rins_data.keys())
            missing_rins = rins_related.difference(knows_rins)
            for rin in missing_rins:
                rins_data[rin] = get_rin_data(rin)

            best_interactions.append(
                AnalysisResult.analyse_motifs_interactions(
                    pdb,
                    chain_name,
                    motifs_inserted,
                    rins_data=rins_data,
                    pdb_interactions=pdb_interactions,
                    motifs_count=motifs_count,
                ),
            )

        with open('best_solution.json', 'w') as json_file:
            json.dump([asdict(inter) for inter in best_interactions], json_file, indent=2)

    # Compare all of them
    records.extend(get_records(best_interactions, SOL_NAME))
    result_df = pd.DataFrame.from_records(records)
    do_violin_graph(result_df, 'motifs')


if __name__ == '__main__':
    pairings()
    # motifs()
