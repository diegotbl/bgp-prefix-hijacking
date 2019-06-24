import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation
import debug
import queue


def bgp_update(graph):
    """Updates accessible ips and paths, using path vector algorithm for each node"""
    # Figure initialization
    pos = nx.spring_layout(graph)           # positions for all nodes
    labels = {}                             # labels definition

    for i in range(len(graph)):
        labels[str(i)] = graph.node[str(i)]['label']

    q = queue.Queue()                       # create queue

    for i in range(len(graph)):             # for each node in the graph
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.remove()
        print("node " + str(i) + ":")       # DEBUG
        q.put(str(i))                       # initialize queue to start até node i
        print("Queue initialized")          # DEBUG
        for j in range(len(graph)):         # sets 'visited' fields to false
            graph.node[str(j)]['visited'] = False
        print("Visited fields set to false\n")    # DEBUG

        path_vector(graph, q, fig, pos, labels)   # runs algorithm and animates

    return graph


def path_vector(graph, q, fig, pos, labels):
    """Runs path vector protocol on the graph"""

    def update(num):
        fig.clear()

        # Gets first element os queue and find its neighbors
        neighbors = []
        node_string = ""
        if q.empty() is False:
            node_string = q.get()
            print("node_string: " + node_string)                # DEBUG
            neighbors = list(graph.neighbors(node_string))
            print(neighbors)                                    # DEBUG

        # Sends message asking for each neighbor to add announced ip's
        for neighbor in neighbors:
            debug.print_nodes(graph)
            send(graph, node_string, neighbor)

        nodes = nx.draw_networkx_nodes(graph, pos, node_size=1000, node_color="#1FB5B4", alpha=0.9)
        nx.draw_networkx_edges(graph, pos, width=1.0)
        nx.draw_networkx_labels(graph, pos, labels, font_size=10)

        if num % 2 == 0:
            nodes.set_edgecolor("white")
        else:
            nodes.set_edgecolor("black")

    ani = matplotlib.animation.FuncAnimation(fig, update, frames=6, interval=1000, repeat=False)
    plt.show()  # display


def bgp_hijack(graph):
    pass


def send(graph, source_id, dest_id):
    """Updates path table and accessible ip's according to source and destination id's"""

    # for index, ip_accessible_dest in enumerate(graph.node[source_id]['accessible']):
    #     if ip_accessible_dest not in graph.node[dest_id]['accessible']:
    #         graph.node[dest_id]['accessible'].append(ip_accessible_dest)
    #         index_path_to_update = eval_index_path_to_update(graph, source_id, index)
    #         graph.node[dest_id]['path'][index_path_to_update].append(graph.node[source_id]['label'])

    return graph


def eval_index_path_to_update(graph, source_id, index):
    idx = index
    # for i in range(int(source_id)):
    #     idx = idx + len(graph.node[str(i)]['announced'])

    return idx
