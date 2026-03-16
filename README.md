## EpiGraph-AI

EpiGraph-AI is a small web app that **simulates infectious spread on a graph** and visualizes the resulting network in the browser. It includes scripts to **generate training data** from simulations and **train an XGBoost regression model**.

## Features

- **Graph-based epidemic simulation** (NetworkX)
- **Interactive visualization UI** (Flask + HTML templates + static JS/CSS)
- **Dataset generation** for supervised learning (`dataset.csv`)
- **Model training** to predict infections after a horizon (`xgboost_model.pkl`)

## Project structure

```text
src/
  Backend/
    app.py              # Flask server + API endpoints
    simulation.py       # core simulation logic
    models.py           # dataclasses/enums used by simulation
    generate_data.py    # generates dataset.csv from simulations
    train_model.py      # trains model and writes xgboost_model.pkl
  Frontend/
    templates/
      index.html
      simulate.html
    static/
      main.js
      style.css
requirements.txt
```

## Requirements

- Python 3.10+ recommended
- Install dependencies:

```bash
pip install -r requirements.txt
```

This installs the web app + simulation dependencies, including `xgboost` for `src/Backend/train_model.py`.

## Run the web app

The Flask app serves:

- `GET /` → home page
- `GET /simulate` → simulation page
- `POST /run_simulation` → runs a simulation and returns graph JSON for the UI

From the repo root:

```bash
python src/Backend/app.py
```

Then open the app in your browser at `http://127.0.0.1:5000/`.

### `/run_simulation` API payload

`POST /run_simulation` expects JSON like:

```json
{
  "nodes": 120,
  "infected": 5,
  "prob": 0.15,
  "steps": 10
}
```

It returns:

- `nodes`: Cytoscape-compatible node list with `id` + `state`
- `edges`: Cytoscape-compatible edge list
- `prediction`: predicted infected count (currently derived from the simulation result)

## Generate dataset and train the model (optional)

The Flask app tries to load the model from **`src/Backend/xgboost_model.pkl`** on startup. To create it:

```bash
cd src/Backend
python generate_data.py
python train_model.py
```

This produces:

- `src/Backend/dataset.csv`
- `src/Backend/xgboost_model.pkl`

## Git-tracked artifacts

By default, this repo’s `.gitignore` ignores:

- `dataset.csv`
- `*.pkl`

So datasets and trained models are meant to be **generated locally**.

## Troubleshooting

- **App crashes on startup with “file not found … xgboost_model.pkl”**
  - Train the model as described above (or place a model at `src/Backend/xgboost_model.pkl`).
- **`ModuleNotFoundError: xgboost` when training**
  - Run `pip install xgboost`.
