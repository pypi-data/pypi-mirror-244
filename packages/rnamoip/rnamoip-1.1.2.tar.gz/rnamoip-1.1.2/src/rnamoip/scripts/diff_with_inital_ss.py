
from collections import defaultdict
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from rnamoip.analysis.comparer import ComparerResult
from rnamoip.compare_tools import get_rnamoip_result
from rnamoip.execute_pdb import read_chains
from rnamoip.multi_batch_analysis import is_interesting

# IMPORTANT: Only work on python 3.9


def do_violin_graph(score_df, filename: str):
    # line_ppv = np.median(result_df['RNAMoIP'])
    # score_df = score_df.melt('chain_name', var_name='Alpha', value_name='Score F1')
    sns.set(font_scale=1.50)
    plt.rcParams["xtick.labelsize"] = 14
    plt.rcParams["figure.figsize"] = (10, 7)
    ax = sns.violinplot(
        data=score_df,
        x='Alpha',
        y='Delta',
        # hue='Tool',
        scale="area",
        cut=0,
        bw=.2,
        inner="box",
    )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=30, ha="right")
    # plt.axhline(y=line_ppv, linestyle='--', color='r', alpha=0.8)
    plt.ylim(0, 1)
    plt.savefig(f'z_output/{filename}.png')
    plt.show()


def do_delta_graph(delta_score: list[float], filename):
    sns.set(font_scale=1.25)

    delta_data = pd.DataFrame(delta_score, columns=['Delta'])
    sns.displot(x='Delta', data=delta_data)
    # ax.set_label(f'Delta F1 Score (Knotty - RNAMoIP)')
    plt.savefig(f'z_output/{filename}.png')
    plt.close()


if __name__ == '__main__':
    google_file = '../results/5_sol_google/pdbs_results_multi_batch.json'
    gurobi_file = '../results/gurobi/pdbs_results_multi_batch.json'
    google_1_sol_file = '../results/memoire/pdbs_results_multi_batch.json'
    pdb_source = '../data/chain/chains.json'
    chain_list = read_chains(pdb_source)
    chain_list = list(filter(lambda c: is_interesting(c), chain_list))

    result_google_5_sol: dict = {}
    result_gurobi: dict = {}
    result_google_1_sol: dict = {}
    alphas = ['{:.2f}'.format(alpha) for alpha in [0, 0.05, 0.1, 0.15, 1]]
    for alpha in alphas:
        result_google_5_sol[alpha]: dict[int, dict[str, ComparerResult]] = get_rnamoip_result(
            alpha=alpha, result_file=google_file, all_res=True,
        )
        result_gurobi[alpha]: dict[int, dict[str, ComparerResult]] = get_rnamoip_result(
            alpha=alpha, result_file=gurobi_file, all_res=True,
        )
        result_google_1_sol[alpha]: dict[int, dict[str, ComparerResult]] = get_rnamoip_result(
            alpha=alpha, result_file=google_1_sol_file, all_res=True,
        )

    delta_score_per_alpha = defaultdict(list)
    google_scores = []
    gurobi_scores = []
    records = []
    stats_per_alpha = {}
    names: list[str] = ['Gurobi', 'Or-Tools-5-sols', 'Or-Tools-1-sol']

    def is_completed(res):
        return res and res['solutions_count']

    for alpha in alphas:
        stats = {
            'Count': len(chain_list),
            **{name: {
                'Incompleted': 0,
                'Total_time': 0,
                'Total_iteration_count': 0,
                'Finished_time': 0,
                'Finished_iteration_count': 0,

            } for name in names},
        }
        for chain in chain_list:
            scores = []
            google_5_sol_res = result_google_5_sol[alpha].get(chain.full_name)
            google_1_sol_res = result_google_1_sol[alpha].get(chain.full_name)
            gurobi_res = result_gurobi[alpha].get(chain.full_name)

            res_by_names = [
                ('Gurobi', gurobi_res),
                ('Or-Tools-5-sols', google_5_sol_res),
                ('Or-Tools-1-sol', google_1_sol_res),
            ]
            for name, res in res_by_names:
                if not res or res['solutions_count'] == 0:
                    stats[name]['Incompleted'] += 1
                stats[name]['Total_time'] += res['execution_time_in_sec']
                stats[name]['Total_iteration_count'] += res['iteration_count']

            if all([is_completed(res) for name, res in res_by_names]):
                for name, res in res_by_names:
                    score = ComparerResult(**res['rnamoip_result']).f1_score
                    scores.append((name, score))
                google_score = ComparerResult(**google_5_sol_res['rnamoip_result']).f1_score
                gurobi_score = ComparerResult(**gurobi_res['rnamoip_result']).f1_score
                delta = gurobi_score - google_score
                delta_score_per_alpha[alpha].append(delta)

                for tool, score in scores:
                    records.append({
                        'chain_name': chain.full_name,
                        'Tool': tool,
                        'Score F1': score,
                        'Alpha': alpha,
                    })

                for name, res in res_by_names:
                    stats[name]['Finished_time'] += res['execution_time_in_sec']
                    stats[name]['Finished_iteration_count'] += res['iteration_count']

        stats_per_alpha[alpha] = stats

    for alpha, stats in stats_per_alpha.items():
        for name in names:
            print('########################')
            print(f'{name} - alpha {alpha}')
            print(f"Incompleted: {stats[name]['Incompleted']} / {stats['Count']}")
            print(f"Total execution in seconds: {stats[name]['Total_time']}")
            print(f"Total iterations: {stats[name]['Total_iteration_count']}")
            print(f"Total Average iteration time : {stats[name]['Total_time'] / stats[name]['Total_iteration_count']}")
            print(f"Finished execution in seconds: {stats[name]['Finished_time']}")
            print(f"Finished iterations: {stats[name]['Finished_iteration_count']}")
            print(f"""
                Average Finished iteration time : {stats[name]['Finished_time'] /
                stats[name]['Finished_iteration_count']}
            """)

    do_delta_graph(delta_score_per_alpha['1.00'], 'Gurobi_vs_Google_distrib_1.00')

    # result_df = pd.DataFrame.from_records(records)
    # do_violin_graph(result_df, 'Gurobi_vs_Google')
