from flask import Flask, render_template, request, jsonify
from pathlib import Path
import joblib
import networkx as nx

from simulation import run_full_simulation
from models import HealthState

BASE_DIR = Path(__file__).resolve().parents[1]

TEMPLATE_DIR = BASE_DIR / "Frontend" / "templates"
STATIC_DIR = BASE_DIR / "Frontend" / "static"

app = Flask(
    __name__,
    template_folder=str(TEMPLATE_DIR),
    static_folder=str(STATIC_DIR)
)

model = joblib.load(BASE_DIR / "Backend" / "xgboost_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/simulate")
def simulate():
    return render_template("simulate.html")


@app.route("/run_simulation", methods=["POST"])
def run_simulation_api():

    data = request.json

    num_nodes = int(data["nodes"])
    initial_infected = int(data["infected"])
    infection_prob = float(data["prob"])
    steps = int(data.get("steps", 10))

    # Simulation hyperparameters (can be later exposed to the UI if needed)
    k = 4  # number of neighbors per node

    graph, sim_nodes, infected_after_10 = run_full_simulation(
        num_nodes=num_nodes,
        k=k,
        steps=steps,
        infection_prob=infection_prob,
        initial_infected=initial_infected,
    )

    edges_payload = []
    for idx, (u, v) in enumerate(graph.edges()):
        edges_payload.append(
            {
                "data": {
                    "id": f"e{idx}",
                    "source": str(u),
                    "target": str(v),
                }
            }
        )

    # Use the simulation result directly for prediction to reflect
    # the actual simulated dynamics instead of a near-constant model.
    predicted_people = max(0, min(num_nodes, int(infected_after_10)))

    # Build Cytoscape-compatible node/edge payload using actual states
    nodes_payload = []
    for n in sim_nodes:
        nodes_payload.append(
            {
                "data": {
                    "id": str(n.id),
                    "state": n.state.value,
                }
            }
        )

    return jsonify(
        {
            "nodes": nodes_payload,
            "edges": edges_payload,
            "prediction": predicted_people,
        }
    )


if __name__ == "__main__":
    app.run(debug=True)