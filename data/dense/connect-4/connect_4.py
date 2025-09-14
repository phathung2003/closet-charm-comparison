import os
import pandas as panda
from typing import List

# Định nghĩa cột (42 ô + class)
COLUMNS = [f"pos{i+1}" for i in range(42)] + ["class"]

def connect_4_dataframe() -> panda.DataFrame:
    # File path
    BASE_DIRECTORY:str = os.path.dirname(os.path.abspath(__file__))
    FILE_PATH:str = os.path.join(BASE_DIRECTORY, "connect-4.data")
    
    # Create Data Frame
    data_frame = panda.read_csv(FILE_PATH, header=None, names=COLUMNS)
    return data_frame