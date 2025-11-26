import pandas as pd
import os

# Get the directory of the current file (dummyData.py)
current_dir = os.path.dirname(__file__)  # app/dummy

# Go two levels up to khadar-backend
base_dir = os.path.abspath(os.path.join(current_dir, "..", ".."))

disease_df = pd.read_csv(os.path.join(base_dir, "Smart_Farming_Crop_Yield_2024.csv"))
disease_data = disease_df.iloc[0].to_dict()

recommendation_df = pd.read_csv(os.path.join(base_dir, "Crop_recommendation.csv"))
recommendation_data = recommendation_df.iloc[0].to_dict()

yield_df = pd.read_csv(os.path.join(base_dir, "plant_growth_data.csv"))
yield_data = yield_df.iloc[0].to_dict()