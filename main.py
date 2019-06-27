import loader
import simulate
import print_checks_and_debug


def main():
    graph = loader.read()                               # loads graph
    print_checks_and_debug.print_nodes(graph)           # DEBUG
    simulate.simulate(graph)                            # simulation


if __name__ == '__main__':
    main()
