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

disease_data = load_random_sample("disease_X_test.pkl")
recommendation_data = load_random_sample("reco_X_test.pkl")
yield_data = load_random_sample("yield_X_test.pkl")