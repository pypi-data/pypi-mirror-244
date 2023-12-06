import sys
from pathlib import Path


def read(relative="", filename="input.txt") -> str:
    """Reads a file from the same directory as the current file, or with a relative path."""
    file = sys.argv[0] if __name__ == "__main__" else __file__
    current_dir = Path(file).parent
    path = current_dir / relative / filename
    with open(path, 'r') as f:
        return f.read()
