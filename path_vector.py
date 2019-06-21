import queue


def bgp_update(graph):
    """Updates accessible ips and paths, using path_vector algorithm"""
    for i in len(graph):
        q = queue.Queue()
        q.put(str(i))
        for j in len(graph):
            graph.node[str(j)]['visited'] = False
        explore(graph, q)
    return graph


def explore(graph, q):
    pass


def send(graph, source_id, dest_id):
    """Updates path table and accessible ip's according to source and destination id's"""
    for index, ip_accessible_dest in enumerate(graph.node[str(source_id)]['accessible']):
        if ip_accessible_dest not in graph.node[str(dest_id)]['accessible']:
            graph.node[str(dest_id)]['accessible'].append(ip_accessible_dest)
            index_path_to_update = eval_index_path_to_update(graph, source_id, index)
            graph.node[str(dest_id)]['path'][index_path_to_update].append(graph.node[str(source_id)]['label'])

    return graph


def eval_index_path_to_update(graph, source_id, index):
    idx = index
    for i in range(source_id):
        idx = idx + len(graph.node[str(i)]['announced'])

    return idx
