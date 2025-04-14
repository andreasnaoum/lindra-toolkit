import json
import os


def load_json(path: str) -> dict:
    """
    Load a JSON file.
    """
    with open(path, 'r') as f:
        return json.load(f)


def save_json(data: dict, path: str):
    """
    Save a JSON file.
    """
    with open(path, 'w') as f:
        json.dump(data, f)


def load_jsonl(path: str) -> list[dict]:
    """
    Load a JSONL file.
    """
    with open(path, 'r') as f:
        return [json.loads(line) for line in f]


def save_jsonl(data: list[dict], path: str):
    """
    Save a JSONL file.
    """
    with open(path, 'w') as f:
        for item in data:
            f.write(json.dumps(item) + '\n')


def get_path(rel_path: str) -> str:
    """
    Get the path to a file in the project.
    """
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, rel_path)
