
import json
from pathlib import Path

from rnamoip.batch_execute import batch_execute, parse_args
from rnamoip.execute_pdb import read_chains


def main(result_file, single_process: bool, motifs_path: Path, add_alignments: bool, use_gurobi: bool, pdb_source: str):
    with open('../knotty_results.json') as json_file:
        result_knotty = json.load(json_file)

    all_chains = read_chains(pdb_source)
    chains_interesting = []
    for chain in all_chains:
        if chain.full_name in result_knotty:
            chain.inital_ss = result_knotty[chain.full_name]
            chains_interesting.append(chain)
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


if __name__ == '__main__':
    result_file = 'pdbs_results_multi_batch_knotty.json'
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
