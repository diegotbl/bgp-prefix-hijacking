def print_nodes(graph):
    """Prints graph nodes for debug"""

    for i in range(5):
        print(graph.nodes[str(i)])
    print("\n")


def check_all_ips_are_accessible(graph):
    """Verifies if all announced ips are accessible by all AS's"""

    total_announced_ips = 0
    for i in range(len(graph)):
        total_announced_ips += len(graph.node[str(i)]['announced'])

    for i in range(len(graph)):
        if len(graph.node[str(i)]['accessible']) != total_announced_ips:
            return False

    return True
