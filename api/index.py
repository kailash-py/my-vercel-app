from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import numpy as np

app = FastAPI()

# Enable CORS for POST requests from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/analytics")
async def analytics(request: Request):
    data = await request.json()
    regions = data.get("regions", [])
    threshold = data.get("threshold_ms", 0)

    # Example telemetry bundle: in real deployment, you’d fetch from DB or API
    telemetry = {
        "amer": {"latencies": [120, 150, 200], "uptimes": [0.99, 0.98, 1.0]},
        "apac": {"latencies": [100, 160, 180], "uptimes": [0.97, 0.95, 0.96]},
        "emea": {"latencies": [140, 170, 190], "uptimes": [0.98, 0.99, 0.97]},
    }

    results = {}
    for region in regions:
        if region in telemetry:
            latencies = telemetry[region]["latencies"]
            uptimes = telemetry[region]["uptimes"]

            avg_latency = float(np.mean(latencies))
            p95_latency = float(np.percentile(latencies, 95))
            avg_uptime = float(np.mean(uptimes))
            breaches = sum(1 for l in latencies if l > threshold)

            results[region] = {
                "avg_latency": avg_latency,
                "p95_latency": p95_latency,
                "avg_uptime": avg_uptime,
                "breaches": breaches,
            }

    return results
