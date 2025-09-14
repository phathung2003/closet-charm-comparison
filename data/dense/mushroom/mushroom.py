import os
import pandas as panda
from typing import List

COLUMNS: List[str] = [
    "class", "cap-shape", "cap-surface", "cap-color", "bruises?", "odor",
    "gill-attachment", "gill-spacing", "gill-size", "gill-color",
    "stalk-shape", "stalk-root", "stalk-surface-above-ring",
    "stalk-surface-below-ring", "stalk-color-above-ring",
    "stalk-color-below-ring", "veil-type", "veil-color", "ring-number",
    "ring-type", "spore-print-color", "population", "habitat"
]

def mushroom_dataframe() -> panda.DataFrame:
    # File path
    BASE_DIRECTORY:str = os.path.dirname(os.path.abspath(__file__))
    FILE_PATH:str = os.path.join(BASE_DIRECTORY, "agaricus-lepiota.data")
    
    # Create Data Frame
    data_frame = panda.read_csv(FILE_PATH, header=None, names=COLUMNS)
    return data_frame