import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation
import path_vector


def simulate(graph):
    """Starts BGP simulation: Draws, runs BGP algorithm and BGP Hijacking"""

    pos = nx.spring_layout(graph)  # positions for all nodes

    # Labels definition
    labels = {}

    for i in range(len(graph)):
        labels[str(i)] = graph.node[str(i)]['label']

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.remove()

    def update(num):
        fig.clear()

        nodes = nx.draw_networkx_nodes(graph, pos, node_size=1000, node_color="#1FB5B4", alpha=0.9)
        nx.draw_networkx_edges(graph, pos, width=1.0)
        nx.draw_networkx_labels(graph, pos, labels, font_size=10)

        # Use the BGP algorithm
        # path_vector.bgp_update(graph)

        if num % 2 == 0:
            nodes.set_edgecolor("white")
        else:
            nodes.set_edgecolor("black")

    ani = matplotlib.animation.FuncAnimation(fig, update, frames=6, interval=1000, repeat=False)
    plt.show()  # display
