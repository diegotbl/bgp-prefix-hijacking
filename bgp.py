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
        wrong_paths, correct_paths = path_vector.find_correct_and_wrong_paths(graph)
        node_colors = path_vector.node_coloring(graph, wrong_paths)

        print_checks_and_debug.draw_graph(fig, graph, pos, labels, node_colors, wrong_paths, correct_paths)

    else:
        print("Protocol failed! Not all AS's can access all announced ip's.")

    return graph


def select_ip(graph):
    """Returns a valid IP value that has been announced on the network, either random or user-provided"""

    ip = input("Select an IP to hijack: (type 'random' to select a random existing one)\n")
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


def select_as(graph, ip):
    """Returns an AS from the network, either random or user-provided.
    The AS cannot be the same that announces the hijacked IP"""

    aut_sys = input("Select an AS to be the hijacker: (type 'random' to select a random existing one)\n")
    if aut_sys != 'random':
        for i in range(len(graph)):
            if aut_sys == graph.node[str(i)]['label']:
                if ip in graph.node[str(i)]['announced']:
                    print("The chosen AS is the same that announced the selected IP. Try something else.")
                    return select_as(graph, ip)
                print("The Autonomous System that will hijack the selected IP is: " + aut_sys)
                return str(i)                                               # return index corresponding to that AS
        print("The provided AS is not part of this network. Try again.")
        return select_as(graph, ip)                                         # try again
    else:
        node_id = str(randint(0, len(graph)-1))                             # generate a random node
        while ip in graph.node[node_id]['announced']:
            node_id = str(randint(0, len(graph) - 1))
        print("The randomly selected AS is: " + graph.node[node_id]['label'])
        return node_id


def bgp_hijack(graph, ip, aut_sys):
    """Hijacking itself. Steps: attacker AS announces IP that has already been announced. BGP announces this new IP and
    some paths are updated according to path vector protocol, i.e. some ASs will be redirected to the malicious AS"""
    # AS announces ip on the hijack field
    graph.node[aut_sys]['hijack'].append(ip)
    index = path_vector.eval_index_path_to_update(graph, '0', ip)
    graph.node[aut_sys]['path'][index] = [aut_sys]
    bgp_update(graph)

