
import csv
import json
import os


def kink_turn_pos_by_chain() -> dict[str, list[int]]:
    pos_list_by_chain = {}
    kink_turn_file = os.path.join('data', 'kink_turn', 'IL_29549.9rfam.csv')
    with open(kink_turn_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for line in csv_reader:
            first_pos = line[0]
            infos = first_pos.split('|')
            chain_name = f'{infos[0]}-{infos[2]}'
            pos_list = []
            for pos_info in line:
                pos_list.append(int(pos_info.split('|')[4]) - 1)
            pos_list_by_chain[chain_name] = pos_list
    return pos_list_by_chain


def map_kink_turn_motif(result_dict, pos_list_by_chain, only_id=False):
    kink_turn_mapping_by_chain = {}
    for chain_res in result_dict:
        chain_name = f"{chain_res['pdb_name']}-{chain_res['chain_name']}"
        pos_list = pos_list_by_chain.get(chain_name)
        res_by_pos = {p: '' for p in pos_list}
        if not pos_list:
            raise Exception(f'Unknown chain with kink turn {chain_name} in results, verify csv.')

        for motif_id, motif_infos in chain_res['motifs_inserted'].items():
            for strand_info in motif_infos['strands']:
                start, end = strand_info['start'], strand_info['end']
                for i in range(start, end + 1):
                    if i in pos_list:
                        res_by_pos[i] = (
                            f"motif {motif_id} ({len(motif_infos['strands'])} strands)-"
                            f"strand {strand_info['strand_id']}(len: {end - start + 1})-pos {i - start}"
                        ) if not only_id else motif_id
        kink_turn_mapping_by_chain[chain_name] = res_by_pos
    return kink_turn_mapping_by_chain


def main():
    result_name = '1_with_ali'
    # result_name = '2_without_ali'
    result_file = os.path.join('results', 'kink_turn', result_name, 'pdbs_results_multi_batch.json')
    pos_list_by_chain = kink_turn_pos_by_chain()
    with open(result_file, 'r') as json_file:
        result_dict = json.load(json_file)

    alphas = list(result_dict.keys())
    alphas = ['0.10']

    res_by_alpha = {}
    for alpha in alphas:
        res_by_alpha[alpha] = map_kink_turn_motif(result_dict[alpha], pos_list_by_chain)

    out_file_name = os.path.join('results', 'kink_turn', result_name, 'kink_turn_res.json')
    with open(out_file_name, 'w') as out_file:
        json.dump(res_by_alpha, out_file, indent=2)


if __name__ == '__main__':
    main()
