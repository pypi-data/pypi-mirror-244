
import os
from rnamoip.batch_execute import get_alignments, get_alignments_infos
from rnamoip.execute_pdb import read_chains
from rnamoip.multi_batch_analysis import is_interesting


def to_clustalW():
    ali_folder = os.path.join('..', 'chains', 'sto')
    ali_folder_out = os.path.join('..', 'chains', 'clustal')

    from Bio import AlignIO

    for _, _, ali_file_list in os.walk(ali_folder):
        for ali_file in ali_file_list:
            full_path = os.path.join(ali_folder, ali_file)
            records = AlignIO.read(full_path, "stockholm")
            base_name = ali_file.split('.')[0]
            count = AlignIO.write(records, os.path.join(ali_folder_out, f'{base_name}.cls'), "clustal")
    print("Converted %i records" % count)


def main():
    pdb_source = 'data/alignment/chains_with_ali.json'
    ali_file_name = os.path.join('data', 'alignment', 'alignments_with_chains.json')
    chain_list = read_chains(pdb_source)
    chains_interesting = list(filter(lambda c: is_interesting(c), chain_list))
    alignments_dict = get_alignments_infos(ali_file_name)

    os.makedirs('chains/sto', exist_ok=True)
    for chain in chains_interesting:
        with open(f'chains/sto/{chain.full_name}.sto', 'wt') as sto_out:
            sto_out.writelines([
                '# STOCKHOLM 1.0\n',
                f'#=GF ID chain-{chain.full_name}\n',
                '#=GF AU Gabriel L\n',
                f'#=GF DE Alignements of chain {chain.full_name}\n',
            ])
            alignments = get_alignments(chain, alignments_dict)
            sto_out.writelines([
                f'{chain.full_name}/{1}-{len(chain.sequence)} {chain.sequence}\n',
            ])
            for index, ali in enumerate(alignments, 1):
                sto_out.writelines([
                    f'Ali-{index}-/{1}-{len(ali)} {ali}\n',
                ])
            sto_out.write('//\n')


if __name__ == '__main__':
    # main()
    to_clustalW()
