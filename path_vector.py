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
        wrong_paths, correct_paths = find_correct_and_wrong_paths(graph)
        node_colors = node_coloring(graph, wrong_paths)
        print_checks_and_debug.draw_graph(fig, graph, pos, labels, node_colors, wrong_paths, correct_paths)

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

        wrong_paths, correct_paths = find_correct_and_wrong_paths(graph)

        # Specifying colors for nodes
        node_colors = node_coloring(graph, wrong_paths)

        print_checks_and_debug.draw_graph(fig, graph, pos, labels, node_colors, wrong_paths, correct_paths)

        if q.empty():
            print("empty queue")                                                    # DEBUG
            return

    # Unfortunately FuncAnimation doesn't accept a dynamic frame number, so we need to specify a sufficiently big
    # number so that all nodes are visited and the queue is empty at the end
    if has_been_hijacked(graph):
        ani = matplotlib.animation.FuncAnimation(fig, update, frames=200000, interval=100, repeat=False)
    else:
        ani = matplotlib.animation.FuncAnimation(fig, update, frames=200000, interval=1, repeat=False)
    plt.show(block=False)                                                           # display
    plt.pause(3)
    plt.close()


def send(graph, source_id, dest_id):
    """Updates destination's path table and accessible ip's according to source and destination id's"""

    # Make IPs accessible by source AS also accessible to destination AS
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


def find_correct_and_wrong_paths(graph):
    """Returns the paths that are have been mistakenly followed (when hijack has happened) and the paths that have
    been correctly followed"""

    wrong_paths = []            # initialization
    correct_paths = []          # initialization
    hijacked = has_been_hijacked(graph)

    for i in range(len(graph)):
        if hijacked:
            if graph.node[str(i)]['hijack']:                        # if node i hijacked some IP
                # If it's possible to hijack more than one IP, the following line should be fixed
                idx = eval_index_path_to_update(graph, '0', graph.node[str(i)]['hijack'][0])
                for j in range(len(graph)):
                    path = graph.node[str(j)]['path'][idx]          # check all paths related to that IP
                    # If the last element of path is the node that hijacked, that means the path is wrong
                    if len(path) != 1 and path[-1] == str(i):
                        for k in range(len(path) - 1):
                            aux = small_first(path[k], path[k+1])   # to avoid duplicated tuples: ('0','1')!=('1','0')

                            if tuple(aux) not in wrong_paths:
                                wrong_paths.append(tuple(aux))

                    if len(path) != 1 and path[-1] != str(i):
                        for k in range(len(path) - 1):
                            aux = small_first(path[k], path[k + 1])  # to avoid duplicated tuples: ('0','1')!=('1','0')

                            if tuple(aux) not in correct_paths:
                                correct_paths.append(tuple(aux))
        else:
            for j in range(len(graph)):
                for path in graph.node[str(j)]['path']:
                    if len(path) != 1:
                        for k in range(len(path) - 1):
                            aux = small_first(path[k], path[k + 1])  # to avoid duplicated tuples: ('0','1')!=('1','0')

                            if tuple(aux) not in correct_paths:
                                    correct_paths.append(tuple(aux))

    return wrong_paths, correct_paths


def small_first(a, b):
    if int(a) > int(b):
        return [b, a]
    else:
        return [a, b]


def has_been_hijacked(graph):
    """Informs if the hijack has already happened or not"""

    for i in range(len(graph)):
        if graph.node[str(i)]['hijack']:
            return True
    return False


def node_coloring(graph, wrong_paths):
    node_colors = []

    for i in range(len(graph)):
        if graph.node[str(i)]['hijack']:
            node_colors.append("#880000")                       # red for attacker
        elif graph.node[str(i)]['visited']:
            affected = False
            for edge in wrong_paths:
                if (str(i) == edge[0] or str(i) == edge[1]) and (not affected):
                    node_colors.append("#881177")               # purple for affected AS's
                    affected = True
            if not affected:
                node_colors.append("#008844")                   # green for visited and not affected by hijack AS's
        else:
            node_colors.append("#008844")

    return node_colors
