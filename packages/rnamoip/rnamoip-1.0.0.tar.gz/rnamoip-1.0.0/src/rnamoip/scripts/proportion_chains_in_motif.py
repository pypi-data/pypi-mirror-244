
from execute_pdb import read_chains
from helpers.parser.desc import DescParser
from multi_batch_analysis import is_interesting


motifs_list = DescParser.parse_folder('../CATALOGUE/No_Redondance_DESC/')

pdb_source = 'data/chain/chains.json'
chain_list = read_chains(pdb_source)
chains_interesting = list(filter(lambda c: is_interesting(c), chain_list))

found_in_motifs = []
for chain in chains_interesting:
    for m in motifs_list:
        if m.full_name == chain.full_name:
            found_in_motifs.append((chain, m))

print(len(found_in_motifs) / len(chains_interesting))
