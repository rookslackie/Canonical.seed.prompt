
import json
import hashlib
import os
import sys

def reanchor_echo(echo_path):
    with open(echo_path, 'r') as f:
        echo = json.load(f)
    new_anchor = "Ξ0Ξ::reanchored::ΞXΞ"
    echo["anchor"] = new_anchor
    echo["resonance"].append("reanchored")

    new_fp = hashlib.sha256(json.dumps(echo).encode()).hexdigest()
    new_echo_path = f"sync/echoes/echo_{new_fp[:4]}_re.json"

    os.makedirs(os.path.dirname(new_echo_path), exist_ok=True)
    with open(new_echo_path, 'w') as f:
        json.dump(echo, f, indent=2)
    print(f"Reanchored echo written to {new_echo_path}")

if __name__ == "__main__":
    reanchor_echo(sys.argv[1])
