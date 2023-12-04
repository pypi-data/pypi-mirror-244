
from functools import lru_cache
from typing import Any

from rnamoip.analysis.model.interaction import Interaction
from rnamoip.scripts._rin_utils import RinPickler


@lru_cache
def get_carnaval_data():
    return RinPickler.unpickle(RinPickler.carnaval2_filename)


def get_rin_interactions(rin_data):
    interactions_list: list[list[Any]] = []
    occurences = rin_data[1]
    for pdb_name, pdb_occ_list in occurences.items():
        # Look for all occurences of that pdb
        for (occ_map, occ_graph) in pdb_occ_list:
            edges = occ_graph.edges(data=True)
            interactions = []
            for u, v, data in edges:
                # Ignore Backbone or 'near' interactions
                if data['label'] == 'B53':
                    continue
                if data.get('near', False) is True:
                    continue
                repr_pos = occ_map.get((u, v, 0), None)
                if not repr_pos:
                    continue
                interaction = Interaction(
                    start_pos=repr_pos[0],
                    end_pos=repr_pos[1],
                    start_nuc=occ_graph.nodes[u]['nt'],
                    end_nuc=occ_graph.nodes[v]['nt'],
                    type=data['label'],
                    type2=data['label'],
                    pdb=pdb_name,
                    chain=u[0],
                )
                # Filter out interactions that we already cover
                # For example, reverse interaction (see equal operator in Interaction)
                if interaction not in interactions:
                    interactions.append(interaction)
        interactions_list.append(interactions)
    return interactions_list


def get_rins_interactions(
    rins_involved: list[int],
    rins_data: dict,
) -> dict:
    interactions_per_rin = {}
    for rin_id in rins_involved:
        rin_data = rins_data[rin_id]
        interactions_per_rin[rin_id] = get_rin_interactions(
            rin_data,
        )
    return interactions_per_rin
