import os
import pickle
import pandas as pd
import random

# Get app directory
current_dir = os.path.dirname(__file__)  # app/dummy
base_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))
model_dir = os.path.join(base_dir, "app", "models")

# Helper to load a random sample from X_test
def load_random_sample(file_name):
    path = os.path.join(model_dir, file_name)
    if not os.path.exists(path):
        print(f"File not found: {path}")
        return None

    with open(path, "rb") as f:
        X_test = pickle.load(f)

    # Pick a random row
    row = X_test.sample(1).iloc[0]

    # Convert to pure Python dict
    return row.to_dict()

def new_load_random_samples(file_name, n=100):
    path = os.path.join(model_dir, file_name)

    with open(path, "rb") as f:
        X_test = pickle.load(f)

    # sample without replacement if possible
    samples = X_test.sample(n=min(n, len(X_test)))

    # convert each row to dict
    return samples.to_dict(orient="records")
