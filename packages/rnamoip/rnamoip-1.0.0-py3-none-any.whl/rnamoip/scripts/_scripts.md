# Scripts

Compilations of scripts related to rnaMoIP.
**Please note that some scripts need to be execute from the root folder to see rnamoip source**

## analysis_ps_only.py

Same as multi_batch_analysis, but will take a list of hardcoded PDBs to filter in the results. Useful if you want to generate graphs for only a small subset from the results dictionnary.

## combine_json.py

Will combine multiple `pdbs_results_multi_batch{x}.json` into a single dictionnary. Useful for batch operations, where sometime we execute different alphas values, and then want to compare using `graph_generator.py` or `multi_batch_analysis.py`.

## proportion_chains_in_motif.py

Need to be executed at root project (src/rnamoip).
Calculate the proportion of a filter chains list (filtered from `is_interesting` method) that can be found in the Catalogue list.

## pdb_pairing_coverage.py

Need to be executed at root project (src/rnamoip).
Analyse the pairing coverage of all pdbs in sample data.

## prepare_alignments_file.py

Need to be executed at root project (src/rnamoip).
From the seed file of RFAM alignments, perpare a list of chains and their alignments for a
rnamoip execution.
