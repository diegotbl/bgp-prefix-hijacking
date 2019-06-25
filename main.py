import loader
import simulate
import debug


def main():
    graph = loader.read()               # loads graph
    debug.print_nodes(graph)            # DEBUG
    simulate.simulate(graph)            # simulation


if __name__ == '__main__':
    main()
