import sys


def read() -> str:
    current_path = sys.path[0]
    with open(current_path + "/input.txt", "r") as f:
        return f.read()
