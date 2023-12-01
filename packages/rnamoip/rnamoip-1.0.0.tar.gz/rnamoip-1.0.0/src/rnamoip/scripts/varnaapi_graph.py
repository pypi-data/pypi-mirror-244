from varnaapi import VARNA

sequence = "CCGCCUAACACUGCCAAUGCCGGUCCCAAGCCCGGAUAAAAGUGGAGGGGGCGG"
original_structur = ".((((...(((({{.....((((.[[[..}})))).....))))..]]]))))."
rnafold_structure = "((((((..((((.......((((........)))).....))))....))))))"
rnamoip_structure = "(((.((..(((.....((.((.(([[...))..))))....)))..]])).)))"

v = VARNA(structure=original_structur)
v.savefig("z_output/figures/real.png")
v = VARNA(structure=rnafold_structure)
v.savefig("z_output/figures/rnafold.png")
v = VARNA(structure=original_structur)
v.savefig("z_output/figures/rnamoip.png")
