import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.animation
import print_checks_and_debug
import queue


def bgp_update(graph):
    """Updates accessible ips and paths, using path vector algorithm for each node"""

    # Figure initialization
    pos = nx.spring_layout(graph)                                               # positions for all nodes
    labels = {}                                                                 # labels definition
    for i in range(len(graph)):
        labels[str(i)] = graph.node[str(i)]['label']

    q = queue.Queue()                                                           # create queue

    for i in range(len(graph)):                                                 # for each node in the graph
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.remove()
        print("node " + graph.node[str(i)]['label'] + ":")                      # DEBUG
        q.put(str(i))                                                           # initialize queue to start até node i
        print("node " + str(i) + " added to queue")                             # DEBUG
        for j in range(len(graph)):                                             # sets 'visited' fields to false
            graph.node[str(j)]['visited'] = False
        print("Visited fields set to false\n")                                  # DEBUG

        path_vector(graph, q, fig, pos, labels)                                 # runs algorithm and animates

    # DEBUG - check if number of accessible ips match for each AS
    if print_checks_and_debug.check_all_ips_are_accessible(graph):
        print("Protocol succeeded! All AS's can access all announced ip's. Printing final graph.")
        print_checks_and_debug.draw_graph(fig, graph, pos, labels, "#008800")

    else:
        print("Protocol failed! Not all AS's can access all announced ip's.")
        exit()

    return graph


def path_vector(graph, q, fig, pos, labels):
    """Runs path vector protocol on the graph"""

    def update(num):
        # Gets first element of queue and find its neighbors
        if q.empty() is False:
            node_string = q.get()
            print("node " + graph.node[node_string]['label'] + " removed from queue")       # DEBUG
            neighbors = list(graph.neighbors(node_string))
            print("Neighbors:")                                                             # DEBUG
            for neighbor in neighbors:
                print("\t" + graph.node[neighbor]['label'])                                 # DEBUG
            if not graph.node[node_string]['visited']:
                # Sends message asking for each neighbor to add announced ip's
                for neighbor in neighbors:
                    if not graph.node[neighbor]['visited']:
                        send(graph, node_string, neighbor)
                        print_checks_and_debug.print_nodes(graph)                           # DEBUG
                        q.put(neighbor)                                                     # add neighbor to queue
                        print(graph.node[neighbor]['label'] + " has been added to queue")   # DEBUG

                graph.node[node_string]['visited'] = True                                   # sets AS as visited
                print(graph.node[node_string]['label'] + " has been visited")               # DEBUG

        # Specifying colors for nodes
        node_colors = []
        for i in range(len(graph)):
            if graph.node[str(i)]['visited']:                                       # bluish green for visited AS's
                node_colors.append("#008888")
            else:                                                                   # red for not visited
                node_colors.append("#880000")

        print_checks_and_debug.draw_graph(fig, graph, pos, labels, node_colors)

        if q.empty():
            print("empty queue")  # DEBUG
            return

    # Unfortunately FuncAnimation doesn't accept a dynamic frame number, so we need to specify a sufficiently big
    # number so that all nodes are visited and the queue is empty at the end
    ani = matplotlib.animation.FuncAnimation(fig, update, frames=6, interval=100, repeat=False)
    plt.show(block=False)  # display
    plt.pause(3)  # display
    plt.close()


def send(graph, source_id, dest_id):
    """Updates destination's path table and accessible ip's according to source and destination id's"""

    print("sending message from " + graph.node[source_id]['label'] + " to " + graph.node[dest_id]['label'])     # DEBUG
    # Make ip's accessible by source AS also accessible to destination AS
    for ip_accessible_dest in graph.node[source_id]['accessible']:
        index_path_to_update = eval_index_path_to_update(graph, source_id, ip_accessible_dest)  # finds index of path
        # If this ip is not yet accessible by dest then make it accessible and update path
        if ip_accessible_dest not in graph.node[dest_id]['accessible']:
            graph.node[dest_id]['accessible'].append(ip_accessible_dest)                        # add ip to accessible
            for node_in_path in graph.node[source_id]['path'][index_path_to_update]:            # update path
                graph.node[dest_id]['path'][index_path_to_update].append(node_in_path)
        # Else, check if it's possible to improve the current path and improve it. The parameter used for evaluating
        # which path is better is the number of hops i.e. the amount of nodes on the path.
        else:
            current_path_size = len(graph.node[dest_id]['path'][index_path_to_update])          # get current path
            possible_new_path = [dest_id]
            for node_in_path in graph.node[source_id]['path'][index_path_to_update]:            # assemble new path
                possible_new_path.append(node_in_path)

            if current_path_size > len(possible_new_path):
                graph.node[dest_id]['path'][index_path_to_update] = possible_new_path           # swap current for new

    return graph


def eval_index_path_to_update(graph, source_id, ip):
    """Finds index of path list that correspond to the ip provided. source_id corresponds to an AS that can access
    the ip. By taking the last element from the path of source we get the AS that announces the ip without iterating
    over the graph."""

    source_that_announced = ""                      # initializing
    idx = 0                                         # initializing

    for path in graph.node[source_id]['path']:
        if ip in graph.node[path[-1]]['announced']:
            source_that_announced = path[-1]        # the last element from path is the AS that originally announced ip
            idx = graph.node[path[-1]]['announced'].index(ip)

    for i in range(int(source_that_announced)):
        idx = idx + len(graph.node[str(i)]['announced'])

    return idx


def path_source_ip(graph, source, ip):
    """Shows path traveled by a packet from source AS to a destination AS that has announced the informed IP"""

    path = graph.node[source]['path'][eval_index_path_to_update(graph, source, ip)]
    string_path = print_checks_and_debug.list_to_string_path(graph, path)

    print("path from " + graph.node[source]['label'] + " to AS that announced ip " + ip + " is: ")
    print("\t" + string_path)
    print("\n")


def list_paths(graph, ip):
    """List current paths from all AS's to that IP"""
    for i in range(len(graph)):
        path_source_ip(graph, str(i), ip)
