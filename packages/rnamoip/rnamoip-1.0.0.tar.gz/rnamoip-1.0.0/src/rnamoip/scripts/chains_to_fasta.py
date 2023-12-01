
import os
from rnamoip.execute_pdb import read_chains
from rnamoip.multi_batch_analysis import is_interesting


def main():
    pdb_source = 'data/chain/chains.json'
    chain_list = read_chains(pdb_source)
    chains_interesting = list(filter(lambda c: is_interesting(c), chain_list))

    with open('chains.fasta', 'wt') as fasta_out:
        for chain in chains_interesting:
            fasta_out.writelines([
                f'>{chain.full_name}\n',
                f'{chain.sequence}\n',
            ])

    os.makedirs('chains/input', exist_ok=True)
    for chain in chains_interesting:
        with open(f'chains/input/{chain.full_name}.fasta', 'wt') as fasta_out:
            fasta_out.writelines([
                f'>{chain.full_name}\n',
                f'{chain.sequence}\n',
            ])

    os.makedirs('chains/seqs', exist_ok=True)
    for chain in chains_interesting:
        with open(f'chains/seqs/{chain.full_name}.seq', 'wt') as fasta_out:
            fasta_out.writelines([
                f'{chain.sequence}\n',
            ])


if __name__ == '__main__':
    main()
