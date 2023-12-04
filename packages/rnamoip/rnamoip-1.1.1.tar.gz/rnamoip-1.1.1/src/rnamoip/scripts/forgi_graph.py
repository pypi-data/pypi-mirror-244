
import matplotlib.pyplot as plt
import forgi.graph.bulge_graph as fgb
import forgi.visual.mplotlib as fvm

original_structur = ".((((...(((({{.....((((.[[[..}})))).....))))..]]]))))."
rnafold_structure = "((((((..((((.......((((........)))).....))))....))))))"
rnamoip_structure = "(((.((..(((.....((.((.(([[...))..))))....)))..]])).)))"

real = fgb.BulgeGraph.from_dotbracket(original_structur)
fvm.plot_rna(
    real,
    text_kwargs={"fontweight": "black"},
    lighten=0.7,
    backbone_kwargs={"linewidth": 3},
)
plt.show()
rnafold = fgb.BulgeGraph.from_dotbracket(rnafold_structure)
fvm.plot_rna(
    rnafold,
    text_kwargs={"fontweight": "black"},
    lighten=0.7,
    backbone_kwargs={"linewidth": 3},
)
plt.show()
rnamoip = fgb.BulgeGraph.from_dotbracket(rnamoip_structure)
fvm.plot_rna(
    rnamoip,
    text_kwargs={"fontweight": "black"},
    lighten=0.7,
    backbone_kwargs={"linewidth": 3},
)
plt.show()
