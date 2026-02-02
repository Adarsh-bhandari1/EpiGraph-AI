import networkx as nx
import random
from models import Node, SimulationConfig, HealthState

g = nx.Graph()
nodes = []

def initialize_simulation(num_nodes=100):
    g.clear()
    nodes.clear()

    for i in range(num_nodes):
        n = Node(
            id=i,
            state=HealthState.SUSCEPTIBLE,
            position=(random.random() * 100, random.random() * 100)
        )
        nodes.append(n)
        g.add_node(n.id, data=n)

    return g, nodes


def add_edges(k=5):
    # each node connected to k RANDOM neighbors
    for node in nodes:
        possible_targets = [n.id for n in nodes if n.id != node.id]
        neighbours = random.sample(possible_targets, k)

        for target_id in neighbours:
            g.add_edge(node.id, target_id)


# run simulation setup
g, nodes = initialize_simulation()
add_edges()
