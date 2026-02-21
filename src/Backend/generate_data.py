import csv
import random
import networkx as nx

from simulation import initialize_simulation, add_edges, run_simulation
from models import HealthState

OUTPUT_FILE = "dataset.csv"
NUM_RUNS = 3000
STEPS_AHEAD = 10
INFECTION_PROB = 0.1
K_MIN, K_MAX = 2, 6
AVERAGE_RUNS = 5


def extract_features(graph, nodes):
    infected_now = sum(
        1 for n in nodes if n.state == HealthState.INFECTED
    )

    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()

    avg_degree = sum(dict(graph.degree()).values()) / num_nodes
    clustering = nx.average_clustering(graph)
    density = nx.density(graph)
    infected_ratio = infected_now / num_nodes

    return {
        "num_nodes": num_nodes,
        "num_edges": num_edges,
        "infected_now": infected_now,
        "infected_ratio": infected_ratio,
        "avg_degree": avg_degree,
        "clustering_coeff": clustering,
        "density": density,
    }


with open(OUTPUT_FILE, "w", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=[
            "num_nodes",
            "num_edges",
            "infected_now",
            "infected_ratio",
            "avg_degree",
            "clustering_coeff",
            "density",
            "infected_after_10",
        ],
    )
    writer.writeheader()

    for _ in range(NUM_RUNS):
        num_nodes = random.randint(50, 200)
        k = random.randint(K_MIN, K_MAX)
        initial_infected = random.randint(1, max(1, num_nodes // 10))

        total_infected = 0

        # 🔥 We extract features only once from first clean setup
        graph, nodes = initialize_simulation(num_nodes)
        add_edges(graph, nodes, k)

        for n in random.sample(nodes, initial_infected):
            n.state = HealthState.INFECTED

        # ✅ Extract features BEFORE simulation
        features = extract_features(graph, nodes)

        # Now average simulation outcomes
        for _ in range(AVERAGE_RUNS):
            # Reinitialize for each stochastic run
            graph_run, nodes_run = initialize_simulation(num_nodes)
            add_edges(graph_run, nodes_run, k)

            for n in random.sample(nodes_run, initial_infected):
                n.state = HealthState.INFECTED

            run_simulation(
                graph_run,
                nodes_run,
                STEPS_AHEAD,
                INFECTION_PROB
            )

            infected_after = sum(
                1 for n in nodes_run if n.state == HealthState.INFECTED
            )

            total_infected += infected_after

        infected_avg = total_infected / AVERAGE_RUNS
        features["infected_after_10"] = infected_avg

        writer.writerow(features)

print("Dataset generated successfully.")
