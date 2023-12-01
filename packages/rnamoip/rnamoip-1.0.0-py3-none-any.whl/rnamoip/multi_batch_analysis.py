import json
import os
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go

from rnamoip import logger
from rnamoip.analysis.comparer import Comparer
from rnamoip.batch_execute import batch_execute, is_interesting, parse_args
# , get_filter_for_specific_pdb, PDB_LIST
from rnamoip.execute_pdb import read_chains
from rnamoip.helpers.structure import StructureHelper

RNAFOLD = 'RNAalifold'


def get_f1_score(ppv, sensitivity):
    if ppv + sensitivity == 0:
        return 0
    return (2 * ppv * sensitivity) / (ppv + sensitivity)


def f1_score(ppvs_per_chain, sens_per_chain):
    f1_score_by_chain = {}
    f1_score_by_alpha = defaultdict(list)
    colors = plt.cm.jet(np.linspace(0, 1, len(ppvs_per_chain.keys())))
    for color, (label, ppv_items), (label2, sens_items) in zip(colors, ppvs_per_chain.items(), sens_per_chain.items()):
        assert label == label2
        y = [(label1, get_f1_score(ppv, sens)) for (label1, ppv), (label2, sens) in zip(ppv_items, sens_items)]
        f1_score_by_chain[label] = y
        for alpha, value in y:
            f1_score_by_alpha[alpha].append(value)

    for color, (label, f1) in zip(colors, f1_score_by_chain.items()):
        x, y = zip(*f1)
        plt.scatter(x, y, color=color, label=label, alpha=.5)

    f1_means_by_alpha = {}
    f1_std_by_alpha = {}
    for alpha, values in f1_score_by_alpha.items():
        f1_means_by_alpha[alpha] = np.mean(values)
        f1_std_by_alpha[alpha] = np.std(values)

    plt.errorbar(
        f1_means_by_alpha.keys(), f1_means_by_alpha.values(),
        yerr=list(f1_std_by_alpha.values()),
        label='mean', color='gray', marker='o', linestyle='--', alpha=.8,
    )

    plt.gca().set(title='Score based on alpha', ylabel='F1 Score')
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig('z_output/figures/pairings/f1_score')
    plt.close()

    return f1_score_by_alpha


def average_time_per_nucs(result_dict: dict):
    times = []
    nucs = []
    labels = []
    if '0.10' not in result_dict:
        return

    for res in result_dict['0.10']:
        # Here was a time I didn't rename execution_time_in_ms correctly
        secs = res.get('execution_time_in_sec', res.get('execution_time_in_ms', 0))
        times.append(secs)
        nucs.append(len(res['sequence_original']))
        labels.append(f"{res['pdb_name']}-{res['chain_name']}")

    for nuc, time, label in zip(nucs, times, labels):
        plt.scatter(
            nuc, time, label=label, marker='o', alpha=.8, c='c',
        )
    ax = plt.gca()
    ax.set(
        # title="Temps d'exécution par rapport aux nombres de nucléotides",
        # ylabel='Temps (s) (log)',
        # xlabel='Nombres de nucléotides',
        title='Execution time based on nucleotides count',
        ylabel='Time (s) (log)',
        xlabel='Nucleotides Count',
    )
    # plt.legend(bbox_to_anchor=(1, 1), loc='upper left')

    ax.set_yscale('log')
    plt.tight_layout()
    plt.savefig('z_output/figures/execution_time', dpi=400)


def create_results_table(results_dict: dict):
    values_by_chain = defaultdict(list)
    header = ['Chain Name', 'PseudoKnot lvl']
    for res in results_dict['0.10']:
        chain_name = f"{res['pdb_name']}-{res['chain_name']}"
        ss = res.get('pdb_ori_structure', res.get('original_structur'))
        lvl = StructureHelper.get_pairing_level_of(ss)
        values_by_chain[chain_name].append(chain_name)
        values_by_chain[chain_name].append(lvl)

    # Add alpha results
    values_by_chain["Mean"].append("Mean")
    values_by_chain["Mean"].append("Mean")
    for alpha, result_list in results_dict.items():
        ppv_values = []
        sens_values = []
        lvl_values = []
        for res in result_list:
            chain_name = f"{res['pdb_name']}-{res['chain_name']}"
            ppv = res['rnamoip_result']['PPV']
            sensitivity = res['rnamoip_result']['sensitivity']
            ss = res['rnamoip_structure']
            lvl = StructureHelper.get_pairing_level_of(ss)
            values_by_chain[chain_name].append(ppv)
            values_by_chain[chain_name].append(sensitivity)
            values_by_chain[chain_name].append(lvl)
            ppv_values.append(ppv)
            sens_values.append(sensitivity)
            lvl_values.append(lvl)
        values_by_chain["Mean"].append(round(np.mean(ppv_values), 4))
        values_by_chain["Mean"].append(round(np.mean(sens_values), 4))
        values_by_chain["Mean"].append(round(np.mean(lvl_values), 4))

    for alpha in result_dict:
        header.append(f'PPV for Alpha {alpha}')
        header.append(f'Sensitivity for Alpha {alpha}')
        header.append(f'Highest Pseudoknot level for Alpha {alpha}')

    table = go.Table(
        header=dict(values=header),
        cells=dict(values=list(zip(*values_by_chain.values()))),
    )
    fig = go.Figure(data=[table])
    fig.show()
    fig.write_image("z_output/figures/table.png", width=1920, height=1080)


def analyse_results_dict(results_dict: dict):
    first_result_set = list(results_dict.values())[0]
    ppv_by_chain = defaultdict(list)
    sensitivity_by_chain = defaultdict(list)
    ppv_values_by_alpha = defaultdict(list)
    sensitivity_values_by_alpha = defaultdict(list)
    timeout_by_alpha = defaultdict(list)

    # Add rnafold result
    for res in first_result_set:
        chain_name = f"{res['pdb_name']}-{res['chain_name']}"
        ppv = res['rnafold_result']['PPV']
        sensitivity = res['rnafold_result']['sensitivity']
        ppv_by_chain[chain_name].append((RNAFOLD, ppv))
        sensitivity_by_chain[chain_name].append((RNAFOLD, sensitivity))
        ppv_values_by_alpha[RNAFOLD].append(ppv)
        sensitivity_values_by_alpha[RNAFOLD].append(sensitivity)

    # Add alpha results
    for alpha, result_list in results_dict.items():
        for res in result_list:
            if res['solutions_count'] == 0:
                timeout_by_alpha[alpha].append(res)
                continue
            chain_name = f"{res['pdb_name']}-{res['chain_name']}"
            ppv = res['rnamoip_result']['PPV']
            sensitivity = res['rnamoip_result']['sensitivity']
            ppv_by_chain[chain_name].append((alpha, ppv))
            sensitivity_by_chain[chain_name].append((alpha, sensitivity))
            ppv_values_by_alpha[alpha].append(ppv)
            sensitivity_values_by_alpha[alpha].append(sensitivity)

    colors = plt.cm.jet(np.linspace(0, 1, len(ppv_by_chain.keys())))

    plt.rcParams["figure.figsize"] = (8, 6)
    for color, (label, data) in zip(colors, ppv_by_chain.items()):
        x, y = zip(*data)
        plt.scatter(x, y, color=color, label=label, alpha=.5)

    ppv_means_by_alpha = {}
    ppv_std_by_alpha = {}
    for alpha, values in ppv_values_by_alpha.items():
        ppv_means_by_alpha[alpha] = np.mean(values)
        ppv_std_by_alpha[alpha] = np.std(values)

    plt.errorbar(
        ppv_means_by_alpha.keys(), ppv_means_by_alpha.values(),
        yerr=list(ppv_std_by_alpha.values()),
        label='mean', color='gray', marker='o', linestyle='--', alpha=.8,
    )
    plt.gca().set(title='Score based on alpha', ylabel='PPV')
    # plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.ylim(0, 1)
    plt.tight_layout()
    if not os.path.exists('z_output/figures/pairings'):
        os.makedirs('z_output/figures/pairings')
    plt.savefig('z_output/figures/pairings/ppv')

    plt.close()
    for color, (label, data) in zip(colors, sensitivity_by_chain.items()):
        x, y = zip(*data)
        plt.scatter(x, y, color=color, label=label, alpha=.5)

    sensitivity_means_by_alpha = {}
    sensitivity_std_by_alpha = {}
    for alpha, values in sensitivity_values_by_alpha.items():
        sensitivity_means_by_alpha[alpha] = np.mean(values)
        sensitivity_std_by_alpha[alpha] = np.std(values)

    plt.errorbar(
        sensitivity_means_by_alpha.keys(), sensitivity_means_by_alpha.values(),
        yerr=list(sensitivity_std_by_alpha.values()),
        label='mean', color='gray', marker='o', linestyle='--', alpha=.8,
    )
    plt.gca().set(title='Score based on alpha', ylabel='Sensitivity')
    # plt.legend(bbox_to_anchor=(1, 1), loc='upper left')
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.savefig('z_output/figures/pairings/sensitivity')
    plt.close()

    # Time per nucs for alpha at 0.5
    f1_res = f1_score(ppv_by_chain, sensitivity_by_chain)

    means = {}
    for alpha in ppv_means_by_alpha.keys():
        means[alpha] = [
            round(np.mean(ppv_values_by_alpha[alpha]), 3),
            round(np.mean(sensitivity_values_by_alpha[alpha]), 3),
            round(np.mean(f1_res[alpha]), 3),
        ]
    print('Alpha | PPV | Sens | F1')
    for alpha, values in means.items():
        print(f'{alpha}: {values}')
    average_time_per_nucs(results_dict)
    create_results_table(results_dict)


def main(result_file, single_process: bool, motifs_path: Path, add_alignments: bool, use_gurobi: bool, pdb_source: str):
    # filter_function = get_filter_for_specific_pdb(PDB_LIST)
    filter_function = is_interesting

    chains_interesting = read_chains(pdb_source)
    chains_interesting = list(filter(lambda c: filter_function(c), chains_interesting))
    print(f'Found {len(chains_interesting)} chains with the corresponding criteria.')

    alphas = [0, 0.05, 0.1, 0.15, 1]

    results_dict = {}
    for alpha in alphas:
        print('########')
        print(f'Running Batch with alpha: {alpha}')
        print('########')

        results = batch_execute(
            chains_interesting,
            alpha,
            single_process,
            motifs_path,
            add_alignments,
            use_gurobi,
        )
        results_dict[f'{alpha:.3f}'] = results

    # Save file in case
    with open(result_file, 'w') as json_file:
        json.dump(results_dict, json_file, indent=2)


def recalculate_ratio(results_dict: dict):
    for alpha, result_list in results_dict.items():
        for res in result_list:
            real_struct = res.get('pdb_ori_structure', res['original_structur'])
            output_struct = res['rnamoip_structure']
            motifs_list = res['motifs_inserted']
            try:
                compare_result = Comparer.get_compare_result(
                    real_struct,
                    output_struct,
                    motifs_list,
                )
            except Exception:
                continue

            # Overwrite value
            res['rnamoip_result']['PPV'] = compare_result.PPV
            res['rnamoip_result']['sensitivity'] = compare_result.sensitivity
            res['rnamoip_result']['true_positives'] = compare_result.true_positives
            res['rnamoip_result']['false_positives'] = compare_result.false_positives
            res['rnamoip_result']['false_negatives'] = compare_result.false_negatives

    # Save file in case
    with open(result_file, 'w') as json_file:
        json.dump(results_dict, json_file, indent=2)


if __name__ == '__main__':
    logger.init('multi_batch.log')
    result_file = '../pdbs_results_multi_batch.json'
    if not os.path.isfile(result_file):
        # Run a batch
        args = parse_args()
        main(
            result_file,
            args.single_process,
            args.motifs_path,
            args.add_alignments,
            args.use_gurobi,
            args.chains_source,
        )
    else:
        # load one already saved
        with open(result_file, 'r') as json_file:
            result_dict = json.load(json_file)
            # recalculate_ratio(result_dict)
            analyse_results_dict(result_dict)
