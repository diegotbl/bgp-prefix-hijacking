import loader
import simulate
import debug


def main():
    graph = loader.read()
    debug.print_nodes(graph)
    print("\n")                             # DEBUG
    simulate.simulate(graph)
    # path_vector.send(graph, 0, 1)
    # path_vector.send(graph, 1, 2)
    # path_vector.send(graph, 0, 2)


if __name__ == '__main__':
    main()
