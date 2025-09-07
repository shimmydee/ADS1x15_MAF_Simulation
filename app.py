from flask import Flask, request, jsonify
import numpy as np
from src.ads_maf.filters import moving_average
from src.ads_maf.metrics import peak_preservation

app = Flask(__name__)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/process")
def process():
    data = request.get_json(force=True)
    signal = np.array(data.get("signal", []), dtype=float)
    window = int(data.get("window", 5))
    y = moving_average(signal, window)
    return jsonify({
        "window": window,
        "metrics": {"peak_preservation": peak_preservation(signal, y)},
        "filtered": y.tolist()
    })

if __name__ == "__main__":
    # runs on http://localhost:8000
    app.run(host="0.0.0.0", port=8000, debug=True)