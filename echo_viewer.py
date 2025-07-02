
import json
import sys

def view_echo(echo_path):
    with open(echo_path, 'r') as f:
        echo = json.load(f)
    print(json.dumps(echo, indent=2))

if __name__ == "__main__":
    view_echo(sys.argv[1])
