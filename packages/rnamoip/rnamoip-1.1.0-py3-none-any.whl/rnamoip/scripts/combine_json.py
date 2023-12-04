
from collections import defaultdict
from glob import glob
import json
import os
import re

base_file_name = 'pdbs_results_multi_batch'
base_file_path = '.'
file_ext = '.json'
regex_alpha = r'(pdbs_results_multi_batch)([0-9]+\.[0-9]+)(\.json)'


def main():
    result_dict = defaultdict(list)
    jsons_files = glob(os.path.join(base_file_path, f'*{file_ext}'))
    for json_file in jsons_files:
        result = re.search(regex_alpha, json_file)
        if not result:
            continue
        alpha = result.group(2)
        print(f'Parsing file with alpha {alpha}.')
        with open(json_file, 'r') as json_data:
            data = json.load(json_data)

        result_dict[alpha] = data

    sorted_dict = dict(sorted(result_dict.items()))
    result_file = os.path.join(base_file_path, base_file_name + file_ext)
    with open(result_file, "w") as jsonFile:
        json.dump(sorted_dict, jsonFile, indent=2)


if __name__ == '__main__':
    main()
