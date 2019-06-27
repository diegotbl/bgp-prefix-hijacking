import bgp
import path_vector


def simulate(graph):
    """Starts BGP simulation: Draws, runs BGP algorithm and BGP Hijacking"""

    # Starts by updating all tables to make all ip's accessible for all AS's using path vector protocol
    bgp.bgp_update(graph)

    # Now we select an IP and an AS. Both can be random or user-provided
    ip = bgp.select_ip(graph)
    aut_sys = bgp.select_as(graph, ip)
    path_vector.list_paths(graph, ip)

    print("\nNow that we have a consistent network, a victim IP and an attacker AS, we can start the hijack itself.\n")

    bgp.bgp_hijack(graph, ip, aut_sys)
