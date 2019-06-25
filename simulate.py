import path_vector


def simulate(graph):
    """Starts BGP simulation: Draws, runs BGP algorithm and BGP Hijacking"""

    # Starts by updating all tables to make all ip's accessible for all AS's using path vector protocol
    path_vector.bgp_update(graph)

    # Now, the hijacking
    path_vector.bgp_hijack(graph)
