
import json
import os
import random
import re
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from forgi.utilities.stuff import bpseq_to_tuples_and_seq

import colorcet as cc
from rnamoip.analysis.model.chain import Chain
from rnamoip.analysis.comparer import Comparer, ComparerResult
from rnamoip.execute_pdb import read_chains
from rnamoip.helpers.structure import StructureHelper
from rnamoip.multi_batch_analysis import is_interesting


def weird_bpseq_to_tuples_and_seq(bpseq_str: str):
    """
    Implementation from forgi, but with adjust line splitting for threshknot.
    Convert a bpseq string to a list of pair tuples and a sequence
    dictionary. The return value is a tuple of the list of pair tuples
    and a sequence string.

    :param bpseq_str: The bpseq string
    :return: ([(1,5),(2,4),(3,0),(4,2),(5,1)], 'ACCAA')
    """
    lines = bpseq_str.split('\n')
    seq = []
    tuples = []
    pairing_partner = {}
    for line in lines:
        parts = line.split()

        if len(parts) == 0:
            continue

        (t1, s, t2) = (int(parts[0]), parts[1], int(parts[4]))
        if t2 in pairing_partner and t1 != pairing_partner[t2]:
            raise Exception("Faulty bpseq string. {} pairs with {}, "
                            "but {} pairs with {}".format(t2, pairing_partner[t2], t1, t2))
        if t1 in pairing_partner and t2 != pairing_partner[t1]:
            raise Exception("Faulty bpseq string. {} pairs with {}, "
                            "but {} pairs with {}".format(pairing_partner[t1], t1, t1, t2))

        pairing_partner[t1] = t2
        if t2 != 0:
            pairing_partner[t2] = t1
        tuples += [(t1, t2)]
        seq += [s]

    seq = ''.join(seq).upper()
    return (tuples, seq)


def parse_knotty() -> dict[str, str]:
    knotty_dir = '../my_results/tools/results_knotty'

    results = {}
    for res_filename in os.listdir(knotty_dir):
        chain_name = res_filename.split('.')[0]
        with open(os.path.join(knotty_dir, res_filename), 'rt') as result_file:
            # First line is seq
            _ = result_file.readline()
            res_line = result_file.readline()
            ss = res_line.split(' ')[1]
            # Parse
            results[chain_name] = ss
    return results


def parse_hotknot() -> dict[str, str]:
    hotknot_dir = '../my_results/tools/results_hotknots'

    results = {}
    for res_filename in os.listdir(hotknot_dir):
        chain_name = res_filename.split('.')[0]
        with open(os.path.join(hotknot_dir, res_filename), 'rt') as result_file:
            # First line is info
            _ = result_file.readline()
            # Second line is seq
            _ = result_file.readline()
            res_line = result_file.readline()
            if not res_line:
                continue
            ss = res_line.split(' ')[2]
            ss = ss.split('\t')[0]
            # Parse
            results[chain_name] = ss
    return results


def parse_pknots() -> dict[str, str]:
    pknots_dir = '../my_results/tools/results_pknots'
    results = {}
    for res_filename in os.listdir(pknots_dir):
        chain_name = res_filename.split('.')[0]
        with open(os.path.join(pknots_dir, res_filename), 'rt') as result_file:
            # 3 first lines is info
            _ = result_file.readline()
            _ = result_file.readline()
            _ = result_file.readline()

            pos_list = []
            match_list = []
            line = result_file.readline()
            while line != '----------------------------------------------------------------------\n':
                first_line_seq = result_file.readline().strip('\n').split(' ')
                seq_pos_list = [p for p in first_line_seq if p]
                pos_list.extend(seq_pos_list)

                second_line_seq = result_file.readline().strip('\n').split(' ')
                match_pos_list = [p for p in second_line_seq if p]
                match_list.extend(match_pos_list)
                line = result_file.readline()
                line = result_file.readline()

            pairings_list: list[tuple[int, int]] = []
            for pos, matching in zip(pos_list, match_list):
                if matching == '.':
                    continue
                new_pair = int(pos) - 1, int(matching) - 1
                if (
                    new_pair not in pairings_list
                    or (new_pair[1], new_pair[0]) not in pairings_list
                ):
                    pairings_list.append(new_pair)

            results[chain_name] = StructureHelper.pairings_to_str(pairings_list, len(pos_list))[1]
    return results


def get_rnamoip_result(
    alpha, result_file='../results/pdbs/pdbs_results_multi_batch.json',
    all_res=False,
) -> dict[str, ComparerResult]:
    # result_file = 'ismb-results/alignment/with_ali/pdbs_results_multi_batch.json'
    with open(result_file, 'r') as json_file:
        results_dict = json.load(json_file)

    results = {}
    for res in results_dict[alpha]:
        chain_name = f"{res['pdb_name']}-{res['chain_name']}"
        if all_res:
            results[chain_name] = res
        elif res['solutions_count'] > 0:
            results[chain_name] = ComparerResult(**res['rnamoip_result'])
    # Print stats
    return results


def parse_spotrna(dir_name='results_spotrna'):
    spotrna_dir = f'../my_results/tools/{dir_name}'
    results = {}
    for res_filename in os.listdir(spotrna_dir):
        chain_name = res_filename.split('.')[0]

        with open(os.path.join(spotrna_dir, res_filename), 'rt') as result_file:
            # First line is info
            _ = result_file.readline()
            bpseq_data = result_file.read()
            pairings, seq = bpseq_to_tuples_and_seq(bpseq_data)

            # Remove pairings with 0
            pairings = [p for p in pairings if p[1] != 0]
            pairings = [(i - 1, j - 1) for (i, j) in pairings]

            _, ss = StructureHelper.pairings_to_str(pairings, len(seq))
            results[chain_name] = ss
    return results


def parse_threshknot():
    threshknot_dir = '../my_results/tools/results_threshknot'
    results = {}
    for res_filename in os.listdir(threshknot_dir):
        chain_name = res_filename.split('.')[0]
        with open(os.path.join(threshknot_dir, res_filename), 'rt') as result_file:
            # First line is info
            _ = result_file.readline()
            bpseq_data = result_file.read()
            pairings, seq = weird_bpseq_to_tuples_and_seq(bpseq_data)

            # Remove pairings with 0
            pairings = [p for p in pairings if p[1] != 0]
            pairings = [(i - 1, j - 1) for (i, j) in pairings]

            _, ss = StructureHelper.pairings_to_str(pairings, len(seq))
            results[chain_name] = ss
    return results


def parse_rscape():
    rscape_dir = '../my_results/tools/results_rscape'

    results = {}
    for res_filename in os.listdir(rscape_dir):
        if res_filename.split('.')[1:] != ['cacofold', 'power']:
            continue
        BPAIR_START = '#-----------------'
        chain_filename = res_filename.split('.')[0]
        chain_name = '-'.join(chain_filename.split('-')[1:3])
        with open(os.path.join(rscape_dir, res_filename), 'rt') as result_file:
            line = result_file.readline()
            while (not line.startswith(BPAIR_START)):
                line = result_file.readline()

            power_by_base_pairs: dict[tuple[int, int], float] = {}
            line = result_file.readline()
            while (not line.startswith('#')):
                bp_infos = re.findall(r'[\d*\.?\d*]+', line)
                if bp_infos[-1] != '0.00':
                    if bp_infos[0] == '*':
                        bp = int(bp_infos[1].strip()) - 1, int(bp_infos[2].strip()) - 1
                        bp_power = float(bp_infos[-1])

                        already_present = False
                        pair_to_remove = []
                        for pair, power in power_by_base_pairs.items():
                            if bp[0] in pair or bp[1] in pair:
                                if bp_power > power:
                                    if pair != bp:
                                        pair_to_remove.append(pair)
                                else:
                                    already_present = True
                        for pair in pair_to_remove:
                            power_by_base_pairs.pop(pair)
                        if not already_present:
                            power_by_base_pairs[bp] = bp_power

                line = result_file.readline()

        with open(os.path.join(rscape_dir, f'{chain_filename}.helixcov'), 'rt') as helix_file:
            line = helix_file.readline()
            length = int(line.split('=')[-1].strip())

        base_pairs = list(power_by_base_pairs.keys())
        if base_pairs:
            _, ss = StructureHelper.pairings_to_str(base_pairs, length)
            results[chain_name] = ss
    return results


def parse_linear_fold():
    linearfold_dir = '../my_results/tools/results_linearfold'
    results = {}
    for res_filename in os.listdir(linearfold_dir):
        chain_name = res_filename.split('.')[0]

        with open(os.path.join(linearfold_dir, res_filename), 'rt') as result_file:
            # First line is seq
            _ = result_file.readline()
            ss: str = result_file.readline().split(' ')[0]
            results[chain_name] = ss
    return results


def parse_palikiss_mfe():
    palikiss_dir = '../my_results/tools/results_pAliKiss_MFE'
    results = {}
    for res_filename in os.listdir(palikiss_dir):
        chain_name = res_filename.split('.')[0]

        with open(os.path.join(palikiss_dir, res_filename), 'rt') as result_file:
            # Skip first 9 lines
            for _ in range(9):
                result_file.readline()
            answer: str = result_file.readline()
            ss = answer.rstrip().rstrip(')').split(',')[1].strip(' ')
            results[chain_name] = ss
    return results


def parse_palikiss_ali(chain_list: list[Chain]):
    palikiss_dir = '../my_results/tools/results_pAliKiss_Ali'
    results_best = {}
    results_random = {}
    for res_filename in os.listdir(palikiss_dir):
        chain_name = res_filename.split('.')[0]
        ss_list = []
        with open(os.path.join(palikiss_dir, res_filename), 'rt') as result_file:
            # Skip first line
            for _ in range(1):
                result_file.readline()
            while result_ss_str := result_file.readline():
                ss = result_ss_str.split('  ')[1].strip(' ').strip('\n')
                ss_list.append(ss)

            scoring_dict = {}
            chain_obj = [chain for chain in chain_list if chain.full_name == chain_name]
            if not chain_obj:
                continue
            chain_obj = chain_obj[0]
            for ss in ss_list:
                try:
                    scoring_dict[ss] = Comparer.get_compare_result(chain_obj.secondary_structure, ss).f1_score
                except Exception:
                    continue
            results_best[chain_name] = max(scoring_dict, key=scoring_dict.get) or None
            valid_ss = list(scoring_dict.keys())
            if valid_ss:
                results_random[chain_name] = valid_ss[random.randint(0, len(valid_ss) - 1)]
    return results_best, results_random


def parse_mxfold2():
    mxfold_dir = '../my_results/tools/results_mxfold2'
    results = {}
    for res_filename in os.listdir(mxfold_dir):
        chain_name = res_filename.split('.')[0]

        with open(os.path.join(mxfold_dir, res_filename), 'rt') as result_file:
            # Skip first 2 lines
            for _ in range(2):
                result_file.readline()
            answer: str = result_file.readline()
            ss = answer.split(' ')[0].strip(' ')
            results[chain_name] = ss
    return results


def parse_biokop(chain_list):
    biokop_dir = '../my_results/tools/results_biokop'
    results_best = {}
    results_random = {}
    for res_filename in os.listdir(biokop_dir):
        chain_name = res_filename.split('.')[0]
        ss_list = []
        with open(os.path.join(biokop_dir, res_filename), 'rt') as result_file:
            # Skip first 2 lines
            for _ in range(2):
                result_file.readline()
            while result_ss_str := result_file.readline():
                ss = result_ss_str.split('\t')[0].strip(' ')
                if ss == '\n':
                    continue
                ss = ss.split(' + ')[0].strip(' ')
                ss_list.append(ss)
        if not ss_list:
            continue
        results_random[chain_name] = ss_list[random.randint(0, len(ss_list) - 1)]
        scoring_dict = {}
        chain_obj = [chain for chain in chain_list if chain.full_name == chain_name]
        if not chain_obj:
            continue
        chain_obj = chain_obj[0]
        for ss in ss_list:
            scoring_dict[ss] = Comparer.get_compare_result(chain_obj.secondary_structure, ss).f1_score
        results_best[chain_name] = max(scoring_dict, key=scoring_dict.get)
    return results_best, results_random


def parse_biorseo(chain_list: list[Chain]):
    biorseo_dir = '../my_results/tools/results_biorseo'
    results_best = {}
    results_random = {}
    for res_filename in os.listdir(biorseo_dir):
        chain_name = res_filename.split('.')[0]
        ss_list = []
        with open(os.path.join(biorseo_dir, res_filename), 'rt') as result_file:
            # Skip first 2 lines
            for _ in range(2):
                result_file.readline()
            while result_ss_str := result_file.readline():
                ss = result_ss_str.split('\t')[0].strip(' ')
                ss = ss.split(' + ')[0].strip(' ')
                ss_list.append(ss)
        results_random[chain_name] = ss_list[random.randint(0, len(ss_list) - 1)]
        scoring_dict = {}
        chain_obj = [chain for chain in chain_list if chain.full_name == chain_name]
        if not chain_obj:
            continue
        chain_obj = chain_obj[0]
        for ss in ss_list:
            scoring_dict[ss] = Comparer.get_compare_result(chain_obj.secondary_structure, ss).f1_score
        results_best[chain_name] = max(scoring_dict, key=scoring_dict.get)
    return results_best, results_random


def get_rnamoip_with_knotty_result():
    result_file = '../my_results/ss_from_knotty/1_sol/pdbs_results_multi_batch.json'
    result_rnamoip_knotty: dict[str, ComparerResult] = get_rnamoip_result(
        alpha='0.10', result_file=result_file,
    )
    return result_rnamoip_knotty


def open_solutions_of_result_file(filename):
    with open(filename, 'r') as json_file:
        results_list = json.load(json_file)

    results = defaultdict(dict)
    for res in results_list:
        result = {}
        chain_name = f"{res['pdb_name']}-{res['chain_name']}"
        result['optimal'] = ComparerResult(**res['rnamoip_result'])
        result['optimal_motifs'] = res['motifs_inserted']
        result['optimal_score'] = res['solution_score']
        result['solution_code'] = res['solution_code']
        solutions_results = []
        for index, solution_res in enumerate(res['solution_list'], 1):
            sol_comp_res = Comparer.get_compare_result(
                real_ss=res['pdb_ori_structure'],
                secondary_structure=solution_res['secondary_structure'],
                motifs_inserted=solution_res['motifs_result'],
            )
            solutions_results.append({
                'index': index,
                'secondary_structure': solution_res['secondary_structure'],
                'motifs_inserted': solution_res['motifs_result'],
                'solution_score': solution_res['solution_score'],
                'solution_code': solution_res['solution_code'],
                'comparer_result': sol_comp_res,
            })
        result['solutions'] = solutions_results
        results[chain_name] = result
    return results


def get_optimal_and_best_sol(results: dict[str, dict[str, any]]):
    best_ss_not_optimal_count = 0
    sol_found = 0
    optimal_solutions = []
    best_solutions = []
    for chain, result in results.items():
        if not result['solutions']:
            # Pass case without solutions
            continue

        optimal_solutions.append(result['optimal'])
        sol_found += 1
        # Check if optimal solution has the best structure
        sorted_res = sorted(
            result['solutions'],
            key=lambda c: c['comparer_result'].f1_score,
            reverse=True,
        )
        best = sorted_res[0]

        if best['index'] != 1:
            # best_solutions.append(best['comparer_result'])
            best_solutions.append({
                'compare_result': best['comparer_result'],
                'motifs': best['motifs_inserted'],
                'pdb_name': chain.split('-')[0],
                'chain_name': chain.split('-')[1],
            })
            best_ss_not_optimal_count += 1
            print(f'''
                Optimal ss of chain {chain} was found in solution #{best["index"]}.
                Out of {len(best)} solutions.
            ''')
        else:
            # best_solutions.append(result['optimal'])
            best_solutions.append({
                'compare_result': result['optimal'],
                'motifs': result['optimal_motifs'],
                'pdb_name': chain.split('-')[0],
                'chain_name': chain.split('-')[1],
            })

    nb_sol_mean = np.mean([len(res['solutions']) for res in results.values() if res['solutions']])

    print(f'Number of case solved (optimal): {sol_found}')
    print(f'Average of solutions count: {nb_sol_mean}')
    print(f'Number of times best ss was found in sub-optimals: {best_ss_not_optimal_count}')
    return optimal_solutions, best_solutions


def do_graph(result_df, filename: str):
    line_ppv = np.median(result_df['RNAMoIP'])
    f1_df = result_df.melt('chain_name', var_name='Tool', value_name='Score F1')

    order = (
        f1_df[~f1_df['Tool'].isin(['RNAMoIP', 'RNAMoIP-Knotty'])]
        .groupby(by=["Tool"])['Score F1']
        .median()
        .sort_values()
        .index
    )
    # data = pd.concat([ppv_df, pd.DataFrame({'bob': [1] * len(ppv_df)})])
    sns.set(font_scale=1.00)
    # plt.rcParams["xtick.labelsize"] = 14
    plt.rcParams["figure.figsize"] = (10, 7)

    order = ['RNAMoIP', *order]
    if 'RNAMoIP-Knotty' in f1_df['Tool'].unique():
        order.append('RNAMoIP-Knotty')
    ax = sns.violinplot(
        data=f1_df,
        x='Tool',
        y='Score F1',
        # scale="area",
        scale='width',
        cut=0,
        # bw='scott',
        bw=.2,
        # width=3,
        # scale_hue=True,
        inner="box",
        hue='Tool',
        dodge=False,
        palette=sns.color_palette(cc.glasbey_light, n_colors=len(order)),
        order=order,
        hue_order=order,
    )
    # ax.legend()
    sns.move_legend(ax, "lower left", ncol=4)
    ax.set(xlabel='')
    ax.set(xticklabels=[])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1])
    # ax.legend(loc='upper left',ncol=2, title="Title")
    # ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right", fontsize=9)
    plt.axhline(y=line_ppv, linestyle='--', color='r', alpha=0.8)
    plt.ylim(-.3, 1)
    plt.savefig(f'z_output/{filename}.png')
    # plt.show()


def main_ali():
    pdb_source = '../data/alignment/chains_with_ali.json'
    result_file = '../results/alignment/with_ali/pdbs_results_multi_batch.json'
    chain_list = read_chains(pdb_source)
    chain_list = list(filter(lambda c: is_interesting(c), chain_list))
    result_rscape: dict[str, str] = parse_rscape()
    result_rscape_best, result_rscape_random = parse_palikiss_ali(chain_list)
    result_rnamoip: dict[str, ComparerResult] = get_rnamoip_result(alpha='0.10', result_file=result_file)
    result_ipknot: dict[str, ComparerResult] = get_rnamoip_result(alpha='0.00', result_file=result_file)

    result_df = pd.DataFrame.from_records([
        {
            'chain_name': chain.full_name,
            'RNAMoIP': result_rnamoip[chain.full_name].f1_score,
            'RNAAlifold': Comparer.get_compare_result(
                chain.secondary_structure, chain.rnafold_ss(chain.sequence),
            ).f1_score,
            'IPknot': result_ipknot[chain.full_name].f1_score,
            'R-Scape': Comparer.get_compare_result(
                chain.secondary_structure, result_rscape[chain.full_name],
            ).f1_score if chain.full_name in result_rscape else 0,
            'pAliKiss-Best': Comparer.get_compare_result(
                chain.secondary_structure, result_rscape_best[chain.full_name],
            ).f1_score if chain.full_name in result_rscape_best else 0,
            'pAliKiss-Random': Comparer.get_compare_result(
                chain.secondary_structure, result_rscape_random[chain.full_name],
            ).f1_score if chain.full_name in result_rscape_random else 0,
        }
        for chain in chain_list
    ])

    print(result_df)
    do_graph(result_df, 'tools_ali')


def main():
    pdb_source = '../data/chain/chains.json'
    chain_list = read_chains(pdb_source)
    chain_list = list(filter(lambda c: is_interesting(c), chain_list))

    result_rnamoip: dict[str, ComparerResult] = get_rnamoip_result(alpha='0.10')
    result_ipknot: dict[str, ComparerResult] = get_rnamoip_result(alpha='0.00')
    result_pknots: dict[str, str] = parse_pknots()
    result_knotty: dict[str, str] = parse_knotty()
    result_hotknot: dict[str, str] = parse_hotknot()
    result_spotrna_non_filtered: dict[str, str] = parse_spotrna('results_spotrna_non_filtered')
    result_spotrna: dict[str, str] = parse_spotrna()
    result_mxfold2: dict[str, str] = parse_mxfold2()
    result_biokop_best, result_biokop_random = parse_biokop(chain_list)
    result_biorseo_best, result_biorseo_random = parse_biorseo(chain_list)

    result_linearfold: dict[str, str] = parse_linear_fold()
    result_palikiss: dict[str, str] = parse_palikiss_mfe()
    # result_threshknot: dict[str, str] = parse_threshknot()
    result_rnamoip_knotty: dict[str, ComparerResult] = get_rnamoip_with_knotty_result()

    base_result_dir = '../my_results/multi_sols'
    result_filename = 'pdbs_results_multi_batch0.10.json'
    google_file = os.path.join(base_result_dir, '2_google_time_1e4', result_filename)
    res_multi_sol = open_solutions_of_result_file(google_file)
    _, result_best_solution = get_optimal_and_best_sol(res_multi_sol)
    records = [
        {
            'chain_name': chain.full_name,
            'RNAMoIP': result_rnamoip[chain.full_name].f1_score,
            'RNAfold*': Comparer.get_compare_result(
                chain.secondary_structure, chain.rnafold_ss(chain.sequence),
            ).f1_score,
            'IPknot': result_ipknot[chain.full_name].f1_score,
            'Pknots': Comparer.get_compare_result(
                chain.secondary_structure, result_pknots[chain.full_name],
            ).f1_score if chain.full_name in result_pknots else 0,
            'pAliKiss': Comparer.get_compare_result(
                chain.secondary_structure, result_palikiss[chain.full_name],
            ).f1_score if chain.full_name in result_palikiss else 0,
            'HotKnots': Comparer.get_compare_result(
                chain.secondary_structure, result_hotknot[chain.full_name],
            ).f1_score if chain.full_name in result_hotknot else 0,
            'LinearFold': Comparer.get_compare_result(
                chain.secondary_structure, result_linearfold[chain.full_name],
            ).f1_score if chain.full_name in result_linearfold else 0,
            'SPOT-RNA-non-filtered': Comparer.get_compare_result(
                chain.secondary_structure, result_spotrna_non_filtered[chain.full_name],
            ).f1_score if chain.full_name in result_spotrna_non_filtered else 0,
            'SPOT-RNA-filtered': Comparer.get_compare_result(
                chain.secondary_structure, result_spotrna[chain.full_name],
            ).f1_score if chain.full_name in result_spotrna else None,
            'MXFold2*': Comparer.get_compare_result(
                chain.secondary_structure, result_mxfold2[chain.full_name],
            ).f1_score if chain.full_name in result_mxfold2 else 0,
            'BiORSEO - Best': Comparer.get_compare_result(
                chain.secondary_structure, result_biorseo_best[chain.full_name],
            ).f1_score if chain.full_name in result_biorseo_best else 0,
            'BiORSEO - Random': Comparer.get_compare_result(
                chain.secondary_structure, result_biorseo_random[chain.full_name],
            ).f1_score if chain.full_name in result_biorseo_random else 0,
            'BiokoP - Best': Comparer.get_compare_result(
                chain.secondary_structure, result_biokop_best[chain.full_name],
            ).f1_score if chain.full_name in result_biokop_best else 0,
            'BiokoP - Random': Comparer.get_compare_result(
                chain.secondary_structure, result_biokop_random[chain.full_name],
            ).f1_score if chain.full_name in result_biokop_random else 0,
            'Knotty': Comparer.get_compare_result(
                chain.secondary_structure, result_knotty[chain.full_name],
            ).f1_score if chain.full_name in result_knotty else 0,
            'RNAMoIP-Knotty': result_rnamoip_knotty[chain.full_name].f1_score
            if chain.full_name in result_rnamoip_knotty else 0,
        }
        for chain in chain_list
    ]
    # records.extend([
    #     {'Best of 10; α=0.10': res['compare_result'].f1_score}
    #     for res in result_best_solution
    # ])
    result_df = pd.DataFrame.from_records(records)

    print(result_df)
    print(result_df.mean())
    do_graph(result_df, 'tools')


def write_knotty_results():
    result_knotty: dict[str, str] = parse_knotty()
    with open('knotty_results.json', 'w') as json_out:
        json.dump(result_knotty, json_out, indent=2)


def main_with_and_without_ali():
    pdb_source = '../data/alignment/chains_with_ali.json'
    result_file = '../results/alignment/with_ali/pdbs_results_multi_batch.json'
    chain_list = read_chains(pdb_source)
    chain_list = list(filter(lambda c: is_interesting(c), chain_list))
    result_rscape: dict[str, str] = parse_rscape()
    result_rscape_best, result_rscape_random = parse_palikiss_ali(chain_list)
    result_ipknot: dict[str, ComparerResult] = get_rnamoip_result(alpha='0.00', result_file=result_file)
    with_ali_file = '../results/alignment/with_ali/pdbs_results_multi_batch.json'
    without_ali_file = '../results/alignment/without_ali/pdbs_results_multi_batch.json'
    result_ali_rnamoip05: dict[str, ComparerResult] = get_rnamoip_result(alpha='0.05', result_file=with_ali_file)
    result_ali_rnamoip10: dict[str, ComparerResult] = get_rnamoip_result(alpha='0.10', result_file=with_ali_file)
    result_ali_rnamoip15: dict[str, ComparerResult] = get_rnamoip_result(alpha='0.15', result_file=with_ali_file)

    result_df = pd.DataFrame.from_records([
        {
            'chain_name': chain.full_name,
            'RNAAlifold': Comparer.get_compare_result(
                chain.secondary_structure, chain.rnafold_ss(chain.sequence),
            ).f1_score,
            'IPknot': result_ipknot[chain.full_name].f1_score,
            'RNAMoIP - 0.05': result_ali_rnamoip05[chain.full_name].f1_score,
            'RNAMoIP - 0.10': result_ali_rnamoip10[chain.full_name].f1_score,
            'RNAMoIP - 0.15': result_ali_rnamoip15[chain.full_name].f1_score,
            # 'RNAMoIP - Without Ali 0.05': result_no_ali_rnamoip05[chain.full_name].f1_score,
            # 'RNAMoIP - Without Ali 0.10': result_no_ali_rnamoip10[chain.full_name].f1_score,
            # 'RNAMoIP - Without Ali 0.15': result_no_ali_rnamoip15[chain.full_name].f1_score,
            'R-Scape': Comparer.get_compare_result(
                chain.secondary_structure, result_rscape[chain.full_name],
            ).f1_score if chain.full_name in result_rscape else 0,
            'pAliKiss-Best': Comparer.get_compare_result(
                chain.secondary_structure, result_rscape_best[chain.full_name],
            ).f1_score if chain.full_name in result_rscape_best else 0,
            'pAliKiss-Random': Comparer.get_compare_result(
                chain.secondary_structure, result_rscape_random[chain.full_name],
            ).f1_score if chain.full_name in result_rscape_random else 0,
        }
        for chain in chain_list
    ])

    print(result_df)
    do_graph(result_df, 'tools_ali')


if __name__ == '__main__':
    # main()
    # main_ali()
    main_with_and_without_ali()
    # write_knotty_results()
