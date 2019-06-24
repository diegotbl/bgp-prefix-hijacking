import path_vector


def simulate(graph):
    """Starts BGP simulation: Draws, runs BGP algorithm and BGP Hijacking"""

    path_vector.bgp_update(graph)
    path_vector.bgp_hijack(graph)
