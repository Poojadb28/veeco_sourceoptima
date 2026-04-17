import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_test_data(filename="testdata.json"):
    

    file_path = os.path.join(BASE_DIR, "testdata", filename)

    # fallback for Jenkins workspace
    if not os.path.exists(file_path):
        file_path = os.path.join(os.getcwd(), "testdata", filename)

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Test data file not found.\nChecked:\n{file_path}"
        )

    with open(file_path, "r") as f:
        return json.load(f)