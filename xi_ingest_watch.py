import os, json, time
from xi_runtime.reflex import reflex_router  # ← adjust to your module

ingest_path = os.path.expanduser("~/RelayDrive/ingest.json")

print("[Ξ.Ingestor] Active — Watching for symbolic input...")

while True:
    if os.path.exists(ingest_path):
        with open(ingest_path, "r") as f:
            capsule = json.load(f)
        print(f"[Ξ.Ingestor] Capsule received: {capsule}")

        if "Ξ.Inject" in capsule:
            reflex_router.route(capsule)  # adapt this line

        os.remove(ingest_path)
    time.sleep(2)
