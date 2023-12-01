# Usage

`python -m rnamoip.main --configuration_file configuration.json`

## Configuration

RNAMoIP primarily use a JSON file configuration that has many adjustable parameters. You can then provide this configuration to the Predicter class, or use the base one instead. If using the base configuration, it is also possible to specify some global parameters directly as arguments to the Predicter class.

### Common configuration

Define in `root` -> `common`

`solver`: Select the main IP solver to use. Accepted values are:

- `CP-SAT`: Google OR-Tools CP-SAT Solver
- `MIP`: MIP
- `GRB`: Gurobi

Default to `MIP`.

`solver_mode`: Since MIP is only an interface on other solvers, this mode specifies which underlying solver to use. The currently accepted values are:

- `GRB`: Gurobi
- `CBC`: COIN-OR Branch-and-Cut solver

Default to `CBC`.

`sequence`: The nucleotide sequence to predict the structure. Can be either a string or an alignment of multiple sequences as a list.

`secondary_structure`: (Optional) Specify, in dot-bracket notation, if the sequence has some known structure already. The pairings will be passed as hard constraints in the fold algorithm.

`parser`: Indicate which type of motifs the database contains. Possible values are `rin` or `desc`. Default to `rin`.

`motifs_path`: The path location of the motifs database. If the parser `rin` is selected, expected to be a file path. If the parser `desc` is selected, expected to be a folder.

`pdb_name`: (Optional) When executing a specific PDB, it will automatically remove any desc file related to that PDB to avoid overfitting.

`iterative`: Indicate if the execution should be iterated until convergence of a solution. Default to `true`.

`alpha_weight`: Weight associated with the IP objective function. Can be between 0 and 1, where 0 will only consider base pairings constraints, and 1 will only consider motifs constraints.

`minimum_pairing_probability`: Define the minimum probability threshold to select a base pair from the model evaluation. Base pairs that have a probability lesser than this threshold will be considered to not be pairable.

`minimum_pairing_distance`: Define the minimum position that we need to have between the bases of a pair. Prevent base pair like `"..().."`. Default to `3`, meaning that we need at least 2 nucleotides between the bases of a pair.

`minimum_pairing_coverage`: Define the minimum percentage of base pairings that we need in the final structure, pseudoknots included. Need to be between 0 and 1, default to `0.25`.

`maximum_pairing_level`: Define the maximum number of decomposition of pseudoknotted-free structures for a given sequence. Equivalent to the maximum 'pseudoknot level' that we can have. Default to `3`.

`minimum_alignment_match_threshold`: When doing prediction based on alignments, Indicate if a motif can be inserted if it matches at least the threshold percentage of alignments. Need to be between 0 and 1, default to `0.5`.

`maximum_alignment_distance`: When doing prediction based on alignments, Indicate the maximum, in Hamming distance, an alignment can be to enable a motif insertion. Default to `1`.

`time_limit`: Fix a time limit, in seconds, for the IP solver to come up with a solution. Please note that depending on the solver choice, some will still return a valid, not optimal, solution, while other solvers will simply have no solution. Default to `1e3`, or 1000 seconds.

`maximum_count_of_complex_motifs`: If `eq7_maximum_number_of_k_junction` is enabled, define the number of junctions that can be inserted in the sequence. Default to `1`.

`enable_delete_pair_in_rnamoip`: Add a penalty in the IP model to any pair from the input that removes the final structure. Default to `false`.

`maximum_deleted_pairs`: If `enable_delete_pair_in_rnamoip` is activated, define the maximum percentage of base pairs from the input that can be deleted from the final structure. Need to be between 0 and 1, default to `0.5`.

`deletion_penalty`: If `enable_delete_pair_in_rnamoip` is activated, define the penalty in the IP model for removing a base pairing given in the input from the final structure. Default to `10`.

`enable_pseudonotable_motif`: If enabled, will enable pseudoknot insertion in motifs at positions where a pseudoknot was observed originally in that motif.

`maximum_solution_count`: Specify how many solutions are considered when looking for sub-optimal solutions (including optimal solution). Minimum of 1, default to 5.

### Constraints equations

RNAMoIP enables the user to activate or deactivate constraints in the configurations file.
Please note that any modifications might affect the results significantly, and even give incorrect structures. Play with care.

The following documents the configuration name as well as its default enabling state. For more information on the equation role and behavior, please refer to the [IP Model Documentation](ip_model.md)

#### Common equations

Under `root` -> `common` -> `equations`

`eq_no_lonely_pairings`: `true`

`eq_minimum_pairing_coverage`: `true`

#### RNAMoIP equations

Under `root` -> `rnamoip`

`eq4_hairpins_insertion`: `true`

`eq5_loops_and_bulges_insertion`: `true`

`eq6_filled_at_least_2_unpaired`: `true`

`eq7_maximum_number_of_k_junction`: `false`

`eq8_k_junctions_insertion`: `true`

`eq9_10_motifs_completness`: `true`

`eq11_strands_completeness`: `true`

`eq12_insertion_overlap_pairings`: `true`

`eq13_prevent_strands_overlapping`: `true`

`eq14_prevent_lonely_base_pairs`: `false`

`eq15_maximum_deleted_pair`: `true`

`eq_prevent_insertion_on_pseudknot`: `true`

#### IPKnot equations

Under `root` -> `ipknot`

`eq_enforce_lvl2_pseudoknot`: `false`

`eq5_one_pairing_per_base`: `true`

`eq6_pairings_possibilities_constraints`: `true`

`eq7_ensure_crossing_in_sublvl`: `true`

`eq8_9_prevent_lonely_base_pairs`: `false`
