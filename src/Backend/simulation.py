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
    k=min(k , len(nodes)-1)
    for node in nodes:
        possible_targets = [n.id for n in nodes if n.id != node.id]  #List of all nodes except the current node
        neighbours = random.sample(possible_targets, k) #Select  k random neighbors

        for target_id in neighbours:
            g.add_edge(node.id, target_id)  #Add edge Between the current node and the selected neighbors

def run_simulation(steps=10, infection_prob=0.3):
    for _ in range(steps):
        new_infected = []

        for node in nodes:
            if node.state == HealthState.INFECTED:
                for neighbor_id in g.neighbors(node.id):
                    neighbor = g.nodes[neighbor_id]["data"]

                    if neighbor.state == HealthState.SUSCEPTIBLE:
                        if random.random() < infection_prob:
                            new_infected.append(neighbor)

        for n in new_infected:
            n.state = HealthState.INFECTED

# run simulation setup
g, nodes = initialize_simulation()
add_edges()
