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

    q = queue.Queue()                               # create queue

    for i in range(len(graph)):                     # for each node in the graph
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.remove()
        print("node " + graph.node[str(i)]['label'] + ":")               # DEBUG
        q.put(str(i))                               # initialize queue to start até node i
        print("node " + str(i) + " added to queue")     # DEBUG
        for j in range(len(graph)):  # sets 'visited' fields to false
            graph.node[str(j)]['visited'] = False
        print("Visited fields set to false\n")  # DEBUG

        path_vector(graph, q, fig, pos, labels)     # runs algorithm and animates

    # DEBUG - check if number of accessible ips match for each AS
    if debug.check_all_ips_are_accessible(graph):
        print("Protocol succeeded! All AS's can access all announced ip's.")
    else:
        print("Protocol failed! Not all AS's can access all announced ip's.")

    # DEBUG - check some paths to see if they are as expected
    path_source_ip(graph, 0, "23.1.208.0/20")
    path_source_ip(graph, 0, "213.130.32.0/19")
    path_source_ip(graph, 0, "143.137.84.0/23")
    path_source_ip(graph, 1, "23.1.208.0/20")
    path_source_ip(graph, 1, "213.130.32.0/19")
    path_source_ip(graph, 1, "143.137.84.0/23")

    return graph


def path_vector(graph, q, fig, pos, labels):
    """Runs path vector protocol on the graph"""

    def update(num):
        fig.clear()

        # Gets first element of queue and find its neighbors
        neighbors = []
        node_string = ""
        if q.empty() is False:
            node_string = q.get()
            print("node " + graph.node[node_string]['label'] + " removed from queue")                # DEBUG
            neighbors = list(graph.neighbors(node_string))
            print("Neighbors:")
            for neighbor in neighbors:
                print("\t" + graph.node[neighbor]['label'])                                    # DEBUG
            if not graph.node[node_string]['visited']:
                # Sends message asking for each neighbor to add announced ip's
                for neighbor in neighbors:
                    if not graph.node[neighbor]['visited']:
                        send(graph, node_string, neighbor)
                        debug.print_nodes(graph)
                        q.put(neighbor)
                        print(graph.node[neighbor]['label'] + " has been added to queue")       # DEBUG

                # Sets AS as visited
                graph.node[node_string]['visited'] = True
                print(graph.node[node_string]['label'] + " has been visited")           # DEBUG

        nodes = nx.draw_networkx_nodes(graph, pos, node_size=1200, node_color="#1FB5B4", alpha=0.9)
        nx.draw_networkx_edges(graph, pos, width=1.0)
        nx.draw_networkx_labels(graph, pos, labels, font_size=10)

        if num % 2 == 0:
            nodes.set_edgecolor("white")
        else:
            nodes.set_edgecolor("black")

        if q.empty():
            print("empty queue")  # DEBUG

            return

    ani = matplotlib.animation.FuncAnimation(fig, update, frames=5, interval=1000, repeat=False)
    plt.show()  # display


def bgp_hijack(graph):
    pass


def send(graph, source_id, dest_id):
    """Updates path table and accessible ip's according to source and destination id's"""

    print("sending message from " + graph.node[source_id]['label'] + " to " + graph.node[dest_id]['label'])     # DEBUG
    for ip_accessible_dest in graph.node[source_id]['accessible']:
        if ip_accessible_dest not in graph.node[dest_id]['accessible']:
            graph.node[dest_id]['accessible'].append(ip_accessible_dest)
            index_path_to_update = eval_index_path_to_update(graph, source_id, ip_accessible_dest)
            for node_in_path in graph.node[source_id]['path'][index_path_to_update]:
                graph.node[dest_id]['path'][index_path_to_update].append(node_in_path)
            if source_id == '2' and dest_id == '4':
                print(index_path_to_update)
                debug.print_nodes(graph)

    return graph


def eval_index_path_to_update(graph, source_id, ip):
    source_that_announced = ""
    idx = 0

    for path in graph.node[source_id]['path']:
        if ip in graph.node[path[-1]]['announced']:
            source_that_announced = path[-1]
            idx = graph.node[path[-1]]['announced'].index(ip)

    for i in range(int(source_that_announced)):
        idx = idx + len(graph.node[str(i)]['announced'])

    return idx


def path_source_ip(graph, source, ip):
    """Shows path traveled by a packet from source AS to a destination AS that has announced the informed ip"""

    path = graph.node[str(source)]['path'][eval_index_path_to_update(graph, str(source), ip)]
    string_path = ""
    for node in path:
        if string_path != "":
            string_path = string_path + " -> " + graph.node[node]['label']
        else:
            string_path = graph.node[node]['label']

    print("path from " + graph.node[str(source)]['label'] + " to AS that announced ip " + ip + " is: ")
    print("\t" + string_path)
    print("\n")
