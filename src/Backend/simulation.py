import networkx as nx
import random
from models import Node, HealthState

def initialize_simulation(num_nodes):
    g = nx.Graph()
    nodes = []

    for i in range(num_nodes):
        n = Node(
            id=i,
            state=HealthState.SUSCEPTIBLE,
            position=(random.random() * 100, random.random() * 100)
        )
        nodes.append(n)
        g.add_node(n.id, data=n)

    return g, nodes


def add_edges(graph, nodes, k):
    k = min(k, len(nodes) - 1)

    for node in nodes:
        possible_targets = [n.id for n in nodes if n.id != node.id]
        neighbors = random.sample(possible_targets, k)

        for target_id in neighbors:
            graph.add_edge(node.id, target_id)


def run_simulation(graph, nodes, steps, infection_prob):
    for _ in range(steps):
        new_infected = []

        for node in nodes:
            if node.state == HealthState.INFECTED:
                for neighbor_id in graph.neighbors(node.id):
                    neighbor = graph.nodes[neighbor_id]["data"]

                    if neighbor.state == HealthState.SUSCEPTIBLE:
                        if random.random() < infection_prob:
                            new_infected.append(neighbor)

        for n in new_infected:
            n.state = HealthState.INFECTED


def run_full_simulation(num_nodes, k, steps, infection_prob, initial_infected):
    graph, nodes = initialize_simulation(num_nodes)
    add_edges(graph, nodes, k)

    # Infect initial nodes
    for n in random.sample(nodes, initial_infected):
        n.state = HealthState.INFECTED

    run_simulation(graph, nodes, steps, infection_prob)

    infected_after = sum(
        1 for n in nodes if n.state == HealthState.INFECTED
    )

    return graph, nodes, infected_after
