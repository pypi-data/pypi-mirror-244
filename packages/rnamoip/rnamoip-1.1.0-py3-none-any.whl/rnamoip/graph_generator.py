
import json
import os
from collections import Counter, defaultdict
from itertools import chain, repeat

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from rnamoip.analysis.comparer import ComparerResult
from rnamoip.helpers.structure import StructureHelper
from rnamoip.multi_batch_analysis import get_f1_score

# IMPORTANT: Only work on python 3.9

result_file = ''

# Can be either 'METRIC' or 'INTERACTIONS'
result_type = 'METRIC'
result_columns_per_type = {
    'METRIC': ['PPV', 'Sensitivity', 'F1 Score'],
    'INTERACTIONS': [
        'Interactions',
        'Canonical Interactions', 'Non-canonical Interactions',
        'Generous Interactions', 'Generous Canonical Interactions',
        'Generous Non Canonical Interactions',
        'can_PPV', 'non_can_PPV', 'can_STY', 'non_can_STY', 'can_F1', 'non_can_F1',
    ],
}

title_translator = {
    'PPV': 'PPV',
    'Sensitivity': 'STY',
    'F1': 'F1 Score',
    'ratio_interactions': 'Interactions Ratio',
    'ratio_can_interactions': 'Canonical Interactions Ratio',
    'ratio_non_can_interactionss': 'Non-Canonical Interactions Ratio',
    'gen_ratio_interactions': 'Generous Interactions Ratio',
    'gen_ratio_can_interactions': 'Generous Canonical Interactions Ratio',
    'gen_ratio_non_can_interactions': 'Generous Non-Canonical Interactions Ratio',
    'can_motifs_count': 'Canonical interactions in motifs',
    'can_pdb_in_motifs_count': 'Canonical interactions of PDB',
    'non_can_motifs_count': 'Non-canonical interactions in motifs',
    'non_can_pdb_in_motifs_count': 'Non-canonical interactions of PDB',
    'can_PPV': 'PPV in canonical interactions',
    'non_can_PPV': 'PPV in non-canonical interactions',
    'can_STY': 'STY in canonical interactions',
    'non_can_STY': 'STY in non-canonical interactions',
    'can_F1': 'F1 in canonical interactions',
    'non_can_F1': 'F1 in non-canonical interactions',
}

RNAFOLD = 'RNAAlifold'


def calculate_interactions_metric(
    alpha,
    inters_result,
    ppv_interactions_by_alpha,
    sty_interactions_by_alpha,
    f1_interactions_by_alpha,
):
    for inter_type in ['can', 'non_can']:
        tp = inters_result[f'{inter_type}_count_of_pdb_in_motifs'] * inters_result[f'interactions_ratio_{inter_type}']
        tp = round(tp, 1)
        fp = inters_result.get(f'{inter_type}_count_of_pdb_in_motifs') - tp
        fn = inters_result.get(f'total_motifs_interactions_{inter_type}') - tp

        comparer_results = ComparerResult(tp, fp, fn)
        ppv_interactions_by_alpha[inter_type][alpha].append(comparer_results.PPV)
        sty_interactions_by_alpha[inter_type][alpha].append(comparer_results.sensitivity)
        f1_interactions_by_alpha[inter_type][alpha].append(comparer_results.f1_score)


def skip_result(result) -> bool:
    return result['solutions_count'] == 0


def generate_pd_data(results_dict: dict):
    first_result_set = list(results_dict.values())[0]
    ppv_by_chain = defaultdict(list)
    sensitivity_by_chain = defaultdict(list)
    ppv_values_by_alpha = defaultdict(list)
    sensitivity_values_by_alpha = defaultdict(list)
    f1_score_by_alpha = defaultdict(list)
    f1_score_labeled_by_alpha = defaultdict(list)
    interactions_by_alpha = defaultdict(dict)
    gen_interactions_by_alpha = defaultdict(dict)
    ppv_interactions_by_alpha = defaultdict(dict)
    sty_interactions_by_alpha = defaultdict(dict)
    f1_interactions_by_alpha = defaultdict(dict)
    interactions_count_by_alpha = {}
    interactions_count_by_alpha['can'] = defaultdict(dict)
    interactions_count_by_alpha['non_can'] = defaultdict(dict)

    columns = [RNAFOLD] if result_type == 'METRIC' else []
    alphas = set(results_dict.keys())
    if result_type == 'INTERACTIONS':
        alphas.remove('0.00')
    alphas = sorted(alphas)
    columns.extend(alphas)

    columns.remove('1.00')

    for alpha in alphas:
        interactions_by_alpha['all'] = defaultdict(list)
        interactions_by_alpha['can'] = defaultdict(list)
        interactions_by_alpha['non_can'] = defaultdict(list)
        gen_interactions_by_alpha['all'] = defaultdict(list)
        gen_interactions_by_alpha['can'] = defaultdict(list)
        gen_interactions_by_alpha['non_can'] = defaultdict(list)
        interactions_count_by_alpha['can']['pdb'] = defaultdict(list)
        interactions_count_by_alpha['can']['motif'] = defaultdict(list)
        interactions_count_by_alpha['non_can']['pdb'] = defaultdict(list)
        interactions_count_by_alpha['non_can']['motif'] = defaultdict(list)
        ppv_interactions_by_alpha['can'] = defaultdict(list)
        ppv_interactions_by_alpha['non_can'] = defaultdict(list)
        sty_interactions_by_alpha['can'] = defaultdict(list)
        sty_interactions_by_alpha['non_can'] = defaultdict(list)
        f1_interactions_by_alpha['can'] = defaultdict(list)
        f1_interactions_by_alpha['non_can'] = defaultdict(list)

    empty_count_of_pdb_in_motifs = 0

    # Add rnafold result
    for res in first_result_set:
        if skip_result(res):
            continue
        chain_name = f"{res['pdb_name']}-{res['chain_name']}"
        ppv = res['rnafold_result']['PPV']
        sensitivity = res['rnafold_result']['sensitivity']
        ppv_by_chain[chain_name].append((RNAFOLD, ppv))
        sensitivity_by_chain[chain_name].append((RNAFOLD, sensitivity))
        ppv_values_by_alpha[RNAFOLD].append(ppv)
        sensitivity_values_by_alpha[RNAFOLD].append(sensitivity)
        f1_score_by_alpha[RNAFOLD].append(get_f1_score(ppv, sensitivity))
        f1_score_labeled_by_alpha[RNAFOLD].append((chain_name, get_f1_score(ppv, sensitivity)))
        if res['interactions_result']['interactions_count_of_pdb_in_motifs'] == 0:
            empty_count_of_pdb_in_motifs += 1

    # Add alpha results
    pdbs_no_can_interactions = 0
    pdbs_no_non_can_interactions = 0
    for alpha in alphas:
        result_list = results_dict[alpha]
        for res in result_list:
            if skip_result(res):
                continue
            chain_name = f"{res['pdb_name']}-{res['chain_name']}"
            ppv = res['rnamoip_result']['PPV']
            sensitivity = res['rnamoip_result']['sensitivity']
            ppv_by_chain[chain_name].append((alpha, ppv))
            sensitivity_by_chain[chain_name].append((alpha, sensitivity))
            ppv_values_by_alpha[alpha].append(ppv)
            sensitivity_values_by_alpha[alpha].append(sensitivity)
            f1_score_by_alpha[alpha].append(get_f1_score(ppv, sensitivity))
            f1_score_labeled_by_alpha[alpha].append((chain_name, get_f1_score(ppv, sensitivity)))

            if result_type == 'METRIC' or alpha == '0.00':
                continue
            inters_res = res['interactions_result']
            interactions_by_alpha['all'][alpha].append(inters_res['interactions_ratio'])
            if inters_res.get('can_count_of_pdb_in_motifs', None):
                interactions_by_alpha['can'][alpha].append(inters_res['interactions_ratio_can'])
            else:
                if alpha == '0.10':
                    pdbs_no_can_interactions += 1
            if inters_res.get('non_can_count_of_pdb_in_motifs', None):
                interactions_by_alpha['non_can'][alpha].append(inters_res['interactions_ratio_non_can'])
            else:
                if alpha == '0.10':
                    pdbs_no_non_can_interactions += 1
            gen_interactions_by_alpha['all'][alpha].append(inters_res['generous_interactions_ratio'])
            gen_interactions_by_alpha['can'][alpha].append(inters_res['generous_interactions_ratio_can'])
            gen_interactions_by_alpha['non_can'][alpha].append(inters_res['generous_interactions_ratio_non_can'])
            interactions_count_by_alpha['can']['pdb'][alpha].append(inters_res.get('can_count_of_pdb_in_motifs'))
            interactions_count_by_alpha['can']['motif'][alpha].append(inters_res.get('correct_can_count_of_motifs'))
            interactions_count_by_alpha['non_can']['pdb'][alpha].append(
                inters_res.get('non_can_count_of_pdb_in_motifs'),
            )
            interactions_count_by_alpha['non_can']['motif'][alpha].append(
                inters_res.get('correct_non_can_count_of_motifs'),
            )

            calculate_interactions_metric(
                alpha,
                inters_res,
                ppv_interactions_by_alpha,
                sty_interactions_by_alpha,
                f1_interactions_by_alpha,
            )

    print(f'No canonical interactions count: {pdbs_no_can_interactions}')
    print(f'No Non-canonical interactions count: {pdbs_no_non_can_interactions}')
    if not os.path.exists('z_output/violons/pairings'):
        os.makedirs('z_output/violons/pairings')

    if result_type == 'METRIC':
        line_ppv = np.median(ppv_values_by_alpha[RNAFOLD])
        line_sty = np.median(sensitivity_values_by_alpha[RNAFOLD])
        line_f1 = np.median(f1_score_by_alpha[RNAFOLD])
        stats = {
            'PPV': ppv_values_by_alpha,
            'Sensitivity': sensitivity_values_by_alpha,
            'F1': f1_score_by_alpha,
        }
        do_graph(stats, columns, metric='F1', line=line_f1)
        do_graph(stats, columns, metric='Sensitivity', line=line_sty)
        do_graph(stats, columns, metric='PPV', line=line_ppv)
        # do_combine_graph(stats, columns, metrics=['PPV', 'Sensitivity', 'F1'])
        # do_f1_correlation_graph(f1_score_labeled_by_alpha)
    else:
        stats = {
            'ratio_interactions': interactions_by_alpha['all'],
            'ratio_can_interactions': interactions_by_alpha['can'],
            'ratio_non_can_interactionss': interactions_by_alpha['non_can'],
            'gen_ratio_interactions': gen_interactions_by_alpha['all'],
            'gen_ratio_can_interactions': gen_interactions_by_alpha['can'],
            'gen_ratio_non_can_interactions': gen_interactions_by_alpha['non_can'],
            'can_motifs_count': interactions_count_by_alpha['can']['motif'],
            'can_pdb_in_motifs_count': interactions_count_by_alpha['can']['pdb'],
            'non_can_motifs_count': interactions_count_by_alpha['non_can']['motif'],
            'non_can_pdb_in_motifs_count': interactions_count_by_alpha['non_can']['pdb'],
            'can_PPV': ppv_interactions_by_alpha['can'],
            'non_can_PPV': ppv_interactions_by_alpha['non_can'],
            'can_STY': sty_interactions_by_alpha['can'],
            'non_can_STY': sty_interactions_by_alpha['non_can'],
            'can_F1': f1_interactions_by_alpha['can'],
            'non_can_F1': f1_interactions_by_alpha['non_can'],
        }
        do_graph(stats, columns, metric='ratio_interactions')
        do_graph(stats, columns, metric='ratio_can_interactions')
        do_graph(stats, columns, metric='ratio_non_can_interactionss')
        do_graph(stats, columns, metric='gen_ratio_interactions')
        do_graph(stats, columns, metric='gen_ratio_can_interactions')
        do_graph(stats, columns, metric='gen_ratio_non_can_interactions')
        do_graph(stats, columns, metric='can_PPV')
        do_graph(stats, columns, metric='non_can_PPV')
        do_graph(stats, columns, metric='can_STY')
        do_graph(stats, columns, metric='non_can_STY')
        do_graph(stats, columns, metric='can_F1')
        do_graph(stats, columns, metric='non_can_F1')
        do_interactions_heat_map(stats, columns)
        print(f'Empty count of interactions in pdbs: {empty_count_of_pdb_in_motifs}')
    pass


def do_graph(stats, alphas, metric='PPV', line=None):
    dataset = pd.DataFrame()
    stat = stats[metric]
    for column in alphas:
        data = list(zip(stat[column], repeat(column)))
        frame = pd.DataFrame(
            data,
            columns=[metric, 'alpha'],
        )
        dataset = pd.concat([dataset, frame], ignore_index=True)

    sns.set(font_scale=1.25)
    ax = sns.violinplot(
        x='alpha',
        y=metric,
        data=dataset,
        scale="area",
        cut=0,
        bw=.2,
        inner="box",
    )
    ax.set(xlabel='Alpha', ylabel=title_translator[metric])
    if line:
        plt.axhline(y=line, linestyle='--', color='r', alpha=0.8)
    plt.ylim(0, 1)
    plt.savefig(f'z_output/violons/pairings/{metric}')
    plt.close()


def do_combine_graph(stats, alphas, metrics):
    dataset = pd.DataFrame()
    for metric in metrics:
        for column in alphas:
            data = list(zip(stats[metric][column], repeat(column), repeat(metric)))
            frame = pd.DataFrame(
                data,
                columns=['Score', 'Alpha', 'Metric'],
            )
            dataset = pd.concat([dataset, frame], ignore_index=True)

    sns.set(font_scale=1.25)
    sns.violinplot(
        x='Alpha',
        y='Score',
        data=dataset,
        scale="area",
        cut=0,
        bw=.2,
        inner="box",
        hue='Metric',
        # split=True,
        # palette='plasma',
    )
    plt.ylim(0, 1)
    name = '_'.join(metrics)
    plt.savefig(f'z_output/violons/pairings/{name}')
    plt.close()


def label_point(x, y, val, ax):
    a = pd.concat({'x': x, 'y': y, 'val': val}, axis=1)
    for i, point in a.iterrows():
        ax.text(
            point['x'] + .01, point['y'], str(point['val']), horizontalalignment='left',
            size='xx-small', color='black', weight='semibold',
        )


def do_interactions_heat_map(stats, columns):
    heat_map_set = (
        ('can_motifs_count', 'can_pdb_in_motifs_count', 'Interactions Canoniques dans les Motifs'),
        ('non_can_motifs_count', 'non_can_pdb_in_motifs_count', 'Interactions Non Canoniques dans les Motifs'),
    )

    for (metricx, metricy, title) in heat_map_set:
        alpha = '0.10'
        data = list(zip(stats[metricx][alpha], stats[metricy][alpha]))
        dataset = pd.DataFrame(data, columns=[metricx, metricy])
        sns.scatterplot(x=metricx, y=metricy, data=dataset, cmap="viridis")
        ax = sns.kdeplot(
            data=dataset,
            x=metricx,
            y=metricy,
            levels=5,
            fill=True,
            alpha=0.6,
            cut=0.05,
        )
        ax.yaxis.get_major_locator().set_params(integer=True)
        ax.xaxis.get_major_locator().set_params(integer=True)
        ax.set(xlabel=title_translator[metricx], ylabel=title_translator[metricy])
        plt.savefig(f'z_output/violons/pairings/heatmap_{metricx}')
        plt.close()


def do_f1_correlation_graph(f1_data_per_alpha: dict):
    rnafold_stat = f1_data_per_alpha.pop(RNAFOLD)
    for alpha, stat in f1_data_per_alpha.items():
        chains = [c for (c, v) in stat]
        values = [v for (c, v) in stat]
        frame = pd.DataFrame(
            {
                RNAFOLD: [v for (c, v) in rnafold_stat],
                'f1': values,
                'chain': chains,
            },
            columns=[RNAFOLD, 'f1', 'chain'],
        )
        sns.set(font_scale=1.25)
        ax = sns.scatterplot(x=RNAFOLD, y='f1', data=frame)
        ax.set_xlabel(f'F1 Score for {RNAFOLD}')
        ax.set_ylabel(f'F1 Score for alpha {alpha}')
        ax.plot([0, 1], [0, 1])
        label_point(frame[RNAFOLD], frame['f1'], frame['chain'], plt.gca())
        plt.ylim(0, 1)
        plt.xlim(0, 1)
        filename = f'f1_correlation_alpha_{alpha}'
        plt.savefig(f'z_output/violons/pairings/{filename}.png')
        plt.close()


def generate_pseudoknot_results(results_dict):
    pseudoknot_result = defaultdict(list)
    pseudoknot_ratio = defaultdict(list)
    pseudoknot_predicted_count = defaultdict(list)
    pseudoknot_og_count = defaultdict(list)
    for alpha, result_list in results_dict.items():
        for res in result_list:
            if skip_result(res):
                continue
            struct_predicted = res['rnamoip_structure']
            struct_original = res.get('pdb_ori_structure', res.get('original_structur'))
            predicted_pairings_per_lvl, _ = StructureHelper.find_base_pairings_with_level(struct_predicted)
            original_pairings_per_lvl, _ = StructureHelper.find_base_pairings_with_level(struct_original)

            max_pred_lvl = max([lvl for lvl, pairs in predicted_pairings_per_lvl.items() if pairs], default=1)
            max_og_lvl = max([lvl for lvl, pairs in original_pairings_per_lvl.items() if pairs], default=1)

            if max_pred_lvl > max_og_lvl:
                pseudoknot_result[alpha].append('over')
            elif max_og_lvl > max_pred_lvl:
                # if max_pred_lvl == 0:
                #     pseudoknot_result[alpha].append('wow')
                pseudoknot_result[alpha].append('under')
            else:
                pseudoknot_result[alpha].append('equal')

            ps_pred_pairings = [pairings for lvl, pairings in predicted_pairings_per_lvl.items() if lvl > 0]
            ps_pred_pairings = list(chain(*ps_pred_pairings))
            ps_og_pairings = [pairings for lvl, pairings in original_pairings_per_lvl.items() if lvl > 0]
            ps_og_pairings = list(chain(*ps_og_pairings))

            well_predicted = [pair for pair in ps_pred_pairings if pair in ps_og_pairings]

            pseudoknot_predicted_count[alpha].append(len(ps_pred_pairings))
            pseudoknot_og_count[alpha].append(len(ps_og_pairings))
            pseudoknot_ratio[alpha].append(len(well_predicted))

    print(
        '''Alpha | Count Over Lvl | count Under lvl | count Equal lvl |
        Count Total | OG ps Count | Pred PS Count | Ratio well predicted''',
    )
    for alpha, ps_values in zip(
        pseudoknot_result.keys(),
        pseudoknot_result.values(),
    ):
        res = Counter(ps_values)
        pred_count_mean = round(np.mean(pseudoknot_predicted_count[alpha]), 3)
        og_count_mean = round(np.mean(pseudoknot_og_count[alpha]), 3)
        ratio_mean = round(np.mean(pseudoknot_ratio[alpha]), 3)
        out = [
            res['over'],
            res['under'],
            res['equal'],
            len(ps_values),
            og_count_mean,
            pred_count_mean,
            ratio_mean,
        ]
        print(f'{alpha}: {out}')


if __name__ == '__main__':
    result_file = '../results/alignment/without_ali/pdbs_results_multi_batch.json'
    # load one already saved
    with open(result_file, 'r') as json_file:
        results_dict = json.load(json_file)
        # recalculate_ratio(result_dict)
        generate_pd_data(results_dict)
        generate_pseudoknot_results(results_dict)
