from flask import Flask, render_template
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
TEMPLATE_DIR = BASE_DIR / "Frontend"

app = Flask(__name__, template_folder=str(TEMPLATE_DIR))


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/simulate")
def simulate():
    return render_template("simulate.html")


if __name__ == "__main__":
    app.run(debug=True)
