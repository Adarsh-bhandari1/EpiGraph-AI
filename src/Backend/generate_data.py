import csv
import random
import networkx as nx

from simulation import initialize_simulation, add_edges, run_simulation
from models import HealthState

OUTPUT_FILE = "dataset.csv"
NUM_RUNS = 300
STEPS_AHEAD = 10


def extract_features(graph, nodes):
    infected_now = sum(
        1 for n in nodes if n.state == HealthState.INFECTED
    )

    return {
        "num_nodes": graph.number_of_nodes(),
        "num_edges": graph.number_of_edges(),
        "infected_now": infected_now,
        "avg_degree": sum(dict(graph.degree()).values()) / graph.number_of_nodes(),
        "clustering_coeff": nx.average_clustering(graph),
    }


with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "num_nodes",
            "num_edges",
            "infected_now",
            "avg_degree",
            "clustering_coeff",
            "infected_after_10",
        ],
    )
    writer.writeheader()

    for _ in range(NUM_RUNS):
        graph, nodes = initialize_simulation(num_nodes=100)
        add_edges(k=5)

        # infect one random node
        random.choice(nodes).state = HealthState.INFECTED

        features = extract_features(graph, nodes)

        run_simulation(steps=STEPS_AHEAD)

        infected_after = sum(
            1 for n in nodes if n.state == HealthState.INFECTED
        )

        features["infected_after_10"] = infected_after
        writer.writerow(features)

print("✅ Dataset generated successfully:", OUTPUT_FILE)