import networkx as nx
import random
from models import Node, SimulationConfig, HealthState

g = nx.Graph()
nodes = []

for i in range(100):
    n = Node(
        id=i,
        state=HealthState.SUSCEPTIBLE,
        position=(random.random() * 100, random.random() * 100)
    )
    nodes.append(n)
    g.add_node(n.id, data=n)
