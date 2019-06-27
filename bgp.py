import path_vector
import networkx as nx
import matplotlib.pyplot as plt
import print_checks_and_debug
import queue
from random import randint


def bgp_update(graph):
    """Updates accessible ips and paths, using path vector algorithm for each node. The goal is to make each IP
    accessible to any AS so we can see the attack take place later"""

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

        path_vector.path_vector(graph, q, fig, pos, labels)                     # runs algorithm and animates

    # DEBUG - check if number of accessible ips match for each AS
    if print_checks_and_debug.check_all_ips_are_accessible(graph):
        print("Protocol succeeded! All AS's can access all announced ip's. Printing final graph.")
        print_checks_and_debug.draw_graph(fig, graph, pos, labels, "#008800")

    else:
        print("Protocol failed! Not all AS's can access all announced ip's.")

    # DEBUG - check some paths to see if they are as expected
    path_vector.path_source_ip(graph, "0", "23.1.208.0/20")
    path_vector.path_source_ip(graph, "0", "213.130.32.0/19")
    path_vector.path_source_ip(graph, "0", "143.137.84.0/23")
    path_vector.path_source_ip(graph, "1", "23.1.208.0/20")
    path_vector.path_source_ip(graph, "1", "213.130.32.0/19")
    path_vector.path_source_ip(graph, "1", "143.137.84.0/23")

    return graph


def select_ip(graph):
    """Returns a valid IP value that has been announced on the network, either random or user-provided"""

    ip = input("Select an IP to hijack: (type 'random' to select a random existing one)")
    if ip != 'random':
        if ip not in graph.node['0']['accessible']:
            print("The provided IP has not been announced on this network.")
            return select_ip(graph)                                         # try again
        else:
            print("IP to be hijacked: " + ip)
            return ip
    else:
        node_id = str(randint(0, len(graph)-1))                             # generate a random node
        # Pick random position on announced list of that node
        random_ip_position = randint(0, len(graph.node[node_id]['announced'])-1)
        ip = graph.node[node_id]['announced'][random_ip_position]           # select ip on that position
        print("The randomly selected ip is: " + ip)
        return ip


def bgp_hijack(graph):
    pass
