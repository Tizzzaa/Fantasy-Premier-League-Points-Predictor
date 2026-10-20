import pandas as pd
import matplotlib.pyplot as plt
df = pd.read_csv("data/processed/2025-26_gw.csv")

a = int(input("Enter a number: ")) # Choose a function

if a == 1:
    df.head()

    df.shape            # (rows, columns)
    df.dtypes           # type of each column
    df.info()           # types plus non-null counts in one view

elif a == 2: #Counting the amount of "double gameweeks"
    counts = df.groupby(["element", "GW"]).size() #Counts the number of double gameweeks and groups them by gw
    counts.value_counts()

    doubles = counts[counts > 1].reset_index().groupby("GW").size()
    print(doubles)

elif a==3: # Shows the distrubution of points accross the whole season
    print(df["total_points"].describe())

    df["total_points"].plot(kind="hist", bins=range(-3, 30), figsize=(8, 4))
    plt.xlabel("Points in a gameweek")
    plt.show()

    print(df["total_points"].value_counts().sort_index().head(10))

elif a == 4: #Calculates how many players have 0 minutes and displays a histogram of the minutes distribution
    zero_min = (df["minutes"] == 0).mean()
    print(f"{zero_min:.1%} of rows have 0 minutes")

    df["minutes"].plot(kind="hist", bins=30, figsize=(8, 4))
    plt.show()

elif a == 5: # Displays the average points when the minutes is not equal to 0
    print(df.groupby(df["minutes"] > 0)["total_points"].mean())

elif a == 6: # Shows the amount of rows which have a Null value grouped by each column
    print(df.isna().sum().sort_values(ascending=False).head(15))

elif a == 7: # Displays any element which comes up multiple times for different names (elements are not consistent across seasons)
    names_per_id = df.groupby("element")["name"].nunique()
    print(names_per_id[names_per_id > 1])

elif a == 8: # Shows the average points per position with a bar chart.
    print(df[df["minutes"]>0].groupby("position")["total_points"].agg(["mean", "median", "count"]))

    df[df["minutes"]>0].groupby("position")["total_points"].mean().plot(kind="bar")
    plt.show()