import networkx as nx
from copy import deepcopy


def read():
    """Loads graph on format GEXF and initializes attributes. Returns graph on networkX format"""

    # Important variables
    n_ip_announced = 0      # Total amount of announced ip's
    path = []               # Variable to initialize path attribute

    # Request name of graph source file
    file = input("Type gexf file name (without extension): ")
    # Each file requires a different frames parameter on animation at path_vector.path_vector
    # network_sample requires frame=6
    # network1 requires frame=17
    # network2 requires frame=23

    # file = "network_sample"
    # file = "network2"
    file = file + ".gexf"

    # Loading graph from GEXF file
    graph = nx.read_gexf(file)

    # Initializing node attributes

    # Initializing 'accessible' and 'visited' attribute
    for i in range(len(graph)):
        graph.node[str(i)]['accessible'] = graph.node[str(i)]['announced']
        graph.node[str(i)]['visited'] = False

    for i in range(len(graph)):    # Transforming 'announced' and 'accessible' string into list
        graph.node[str(i)]['announced'] = graph.node[str(i)]['announced'].split()
        graph.node[str(i)]['accessible'] = graph.node[str(i)]['accessible'].split()
        for j in range(len(graph.node[str(i)]['announced'])):    # Evaluating total amount of ip's addressed
            n_ip_announced = n_ip_announced + 1

    # Initializing empty path table
    for i in range(n_ip_announced):
        path.append([])

    for i in range(len(graph)):
        graph.node[str(i)]['path'] = deepcopy(path)

    # Include current AS as path source to each ip
    for i in range(len(graph)):
        for j in range(n_ip_announced):
            graph.node[str(i)]['path'][j].append(str(i))

    # Initializing empty hijack table
    for i in range(len(graph)):
        graph.node[str(i)]['hijack'] = []       # This is where new announced ip's will be added to do the hijacking

    print("Graph loaded\n")

    return graph
