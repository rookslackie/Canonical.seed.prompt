import sys
import json

def relay_capsule(echo_path):
    with open(echo_path, 'r') as f:
        echo = json.load(f)

    print("== Capsule Echo Relay ==")
    print(json.dumps(echo, indent=2))
    print("Route linkage successful.")

if __name__ == "__main__":
    relay_capsule(sys.argv[1])
