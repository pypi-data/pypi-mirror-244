
import json
import matplotlib.pyplot as plt
import seaborn as sns

from analysis.model.chain import Chain
from multi_batch_analysis import is_interesting
import numpy as np


def read_chains(file_path) -> list[Chain]:
    with open(file_path, 'r') as jsonfile:
        chains_json = json.load(jsonfile)

    chain_list = [
        Chain(chain_dict['name'], chain_dict['pdb_name'], chain_dict['sequence'], chain_dict['bps'])
        for chain_dict in chains_json
    ]
    return chain_list


def main():
    pdb_source = 'data/chain/chains.json'
    chains_list = read_chains(pdb_source)

    filter_function = is_interesting
    chains_interesting: list[Chain] = list(filter(lambda c: filter_function(c), chains_list))
    print(f'Found {len(chains_interesting)} chains with the corresponding criteria.')

    coverages = []
    for chain in chains_interesting:
        coverage = (len(chain.bps) * 2) / len(chain.sequence) * 100
        coverages.append(coverage)

    print(f'Min: {np.min(coverages)}')
    print(f'Median: {np.median(coverages)}')
    print(f'Mean: {np.mean(coverages)}')
    # plt.hist(coverages, bins=20, range=[0,100])
    # plt.gca().set(title='Pairing Coverage Distribution', ylabel='Coverage')
    # plt.show()
    # plt.savefig('figures_memoire/pairing_coverage.png')

    plt.figure(figsize=(10, 7), dpi=80)
    kwargs = dict(hist_kws={'alpha': 0.6}, kde_kws={'linewidth': 2})
    plot = sns.distplot(coverages, color='dodgerblue', **kwargs)
    plt.xlim(0, 100)
    plt.gca().set(title='Pairing Coverage Distribution', ylabel='Distribution', xlabel='Coverage')
    plot.figure.savefig('pairing_coverage_pk.png')


if __name__ == '__main__':
    main()
