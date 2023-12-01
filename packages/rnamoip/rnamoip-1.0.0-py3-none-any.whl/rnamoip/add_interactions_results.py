
import json
import os
import pickle
from collections import defaultdict

from tqdm import tqdm

from rnamoip.analysis.analysis_result import AnalysisResult
from rnamoip.analysis.pdb_interaction import get_pdb_interaction
from rnamoip.rin_v2 import rins_path

results_file_name = 'pdbs_results_multi_batch.json'


def get_rin_data(rin_id):
    with open(os.path.join(rins_path, f'local_rin_{rin_id}.pickle'), 'rb') as rin_file:
        return pickle.load(rin_file)


def main():
    with open(results_file_name, 'rt') as res_file:
        results_by_alpha = json.load(res_file)

    # Cast to AnalysisResult and sort by chains
    analysis_res_by_alpha = defaultdict(list)
    chains: dict[tuple[str, str], list[AnalysisResult]] = defaultdict(list)
    for alpha, items in results_by_alpha.items():
        for res in items:
            analysis_res = AnalysisResult(**res)
            analysis_res_by_alpha[alpha].append(analysis_res)
            chains[(analysis_res.pdb_name, analysis_res.chain_name)].append(analysis_res)

    motifs_count = defaultdict(dict)
    for alpha in results_by_alpha.keys():
        float_alpha = float(alpha)
        motifs_count[float_alpha]['motifs_count_in_pdb'] = 0
        motifs_count[float_alpha]['motifs_count_in_pdb_no_canonique'] = 0
        motifs_count[float_alpha]['motifs_count_in_pdb_no_non_canonique'] = 0

    for (pdb, chain_name), analysis_list in tqdm(chains.items()):
        # Get PDB interactions
        pdb_interactions = get_pdb_interaction(pdb, chain_name)
        rins_data = {}

        # For all results of alpha (expect 0.00), find the motifs interactions and
        for analysis in analysis_list:
            if analysis.alpha == 0:
                continue
            # Retrieve all related rins
            rins_related = set()
            for motif in analysis.motifs_inserted.values():
                # Get RIN interactions in range of motif
                rins_related.update([int(mr) for mr in motif['related_rins']])

            # Retrieve the rins data missing
            knows_rins = set(rins_data.keys())
            missing_rins = rins_related.difference(knows_rins)
            for rin in missing_rins:
                rins_data[rin] = get_rin_data(rin)

            interaction_results = analysis.analyse_motifs_interactions(
                pdb_name=analysis.pdb_name,
                chain_name=analysis.chain_name,
                motifs_inserted=analysis.motifs_inserted,
                rins_data=rins_data,
                pdb_interactions=pdb_interactions,
                motifs_count=motifs_count[analysis.alpha],
            )
            analysis.interaction_results = interaction_results

    with open('motifs_results.json', 'wt') as motif_res_file:
        json.dump(motifs_count, motif_res_file, indent=2)

    # sort again by alpha and go for write
    for alpha, analysis_list in analysis_res_by_alpha.items():
        analysis_res_by_alpha[alpha] = [analysis.asdict() for analysis in analysis_list]
    with open('pdbs_results_multi_batch_updated.json', 'wt') as res_file:
        json.dump(analysis_res_by_alpha, res_file, indent=2)


if __name__ == '__main__':
    main()
