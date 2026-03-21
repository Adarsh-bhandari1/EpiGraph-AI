let cyInstance = null;

async function runSimulation() {
  const nodes = document.getElementById("nodes").value;
  const infected = document.getElementById("infected").value;
  const prob = document.getElementById("prob").value;
  const steps = document.getElementById("steps").value || 10;

  const response = await fetch("/run_simulation", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      nodes: nodes,
      infected: infected,
      prob: prob,
      steps: steps,
    }),
  });

  const data = await response.json();

  drawGraph(data.nodes, data.edges);

  document.getElementById("prediction").innerHTML =
    "Predicted infected after " + steps + " steps: " + data.prediction;
}

function drawGraph(nodes, edges) {
  // Destroy previous graph instance if it exists to avoid overlaps
  if (cyInstance) {
    cyInstance.destroy();
  }

  cyInstance = cytoscape({
    container: document.getElementById("graph"),

    elements: [...nodes, ...edges],

    style: [
      // Base node style (applies to all nodes)
      {
        selector: "node",
        style: {
          label: "data(id)",
          "background-color": "#22c55e",
          color: "white",
          width: 14,
          height: 14,
          "font-size": 6,
        },
      },
      // Specific health states override the base style
      {
        selector: 'node[state="susceptible"]',
        style: {
          "background-color": "#22c55e", // green for susceptible
        },
      },
      {
        selector: 'node[state="infected"]',
        style: {
          "background-color": "#ef4444", // red for infected
        },
      },
      {
        selector: 'node[state="recovered"]',
        style: {
          "background-color": "#eab308", // yellow for recovered
        },
      },
      {
        selector: "edge",
        style: {
          "line-color": "#64748b",
          width: 2,
        },
      },
    ],

    layout: {
      name: "cose",
      nodeRepulsion: 8000,
      idealEdgeLength: 80,
      padding: 20,
    },
  });
}

function resetSimulation() {
  // Clear input fields
  document.getElementById("nodes").value = "";
  document.getElementById("infected").value = "";
  document.getElementById("prob").value = "";
  document.getElementById("steps").value = "";

  // Clear prediction text
  const predictionEl = document.getElementById("prediction");
  if (predictionEl) {
    predictionEl.innerHTML = "";
  }

  // Clear graph visualization
  if (cyInstance) {
    cyInstance.destroy();
    cyInstance = null;
  }
  const graphEl = document.getElementById("graph");
  if (graphEl) {
    graphEl.innerHTML = "";
  }
}
