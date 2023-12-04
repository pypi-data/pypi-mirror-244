
## IP Model

Here is a breakdown of the IP model, its variables and its constraints.

### Model

The model is optimize to return the motifs of the longest sequence possible, while maximising the sum of the probabilities of the base pair that we insert.

### Variables

Each nucleotide of the original sequence is represented through a list of variables, representing each motifs that can be inserted at that position.

### Constraints

1. Nucleotide Uniqueness:
Each nucleotide can only be associated to at most one motif.
1. Strand Completeness:
Each Strand need to be inserted completly to be consider valid.
1. Motif Completeness:
Each Motif need to have all their Strands inserted to be consider valid.

And More...
