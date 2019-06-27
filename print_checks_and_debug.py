import networkx as nx
import matplotlib.pyplot as plt


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


def list_to_string_path(graph, list_path):
    """Converts a path list to a more comprehensible string path. Example: [1916, 262847] becomes "1916 -> 262847" """

    string_path = ""
    for node in list_path:
        if string_path != "":
            string_path = string_path + " -> " + graph.node[node]['label']
        else:
            string_path = graph.node[node]['label']

    return string_path


def draw_graph(fig, graph, pos, labels, node_color):
    fig.clear()
    nx.draw_networkx_nodes(graph, pos, node_size=1200, node_color=node_color, alpha=0.9)  # path vector ended
    nx.draw_networkx_edges(graph, pos, width=1.0)
    nx.draw_networkx_labels(graph, pos, labels, font_size=10)
    plt.show()
