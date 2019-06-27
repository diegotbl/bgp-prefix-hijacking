import bgp


def simulate(graph):
    """Starts BGP simulation: Draws, runs BGP algorithm and BGP Hijacking"""

    # Starts by updating all tables to make all ip's accessible for all AS's using path vector protocol
    bgp.bgp_update(graph)

    # Now we select an IP and an AS. Both can be random or user-provided
    ip = bgp.select_ip(graph)

    # Now, the hijacking
    bgp.bgp_hijack(graph)
