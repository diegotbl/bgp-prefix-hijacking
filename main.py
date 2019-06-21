import loader
import simulate
import path_vector


def main():
    graph = loader.read()
    for i in range(5):
        print(graph.nodes[str(i)])
    simulate.simulate(graph)
    path_vector.send(graph, 0, 1)
    path_vector.send(graph, 1, 2)
    path_vector.send(graph, 0, 2)


if __name__ == '__main__':
    main()
