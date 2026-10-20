import pandas as pd
import matplotlib.pyplot as plt

# Run the notebook from notebooks/, so paths go up one level
df = pd.read_csv("data/processed/2024-25_gw.csv")
df.head()

df.shape            # (rows, columns)
df.dtypes           # type of each column
df.info()           # types plus non-null counts in one view