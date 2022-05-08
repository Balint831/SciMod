import pandas as pd
import plotly.express as px





path = "/home/balint831/scimod/data/meas_lr0.001_s60_d10.csv.csv"

df = pd.read_csv(path)

df = df[ (df["update"] == 3) & (df["parity"] == 0) ]

fig = px.histogram(df, x = "energy", color = "bitstring", nbins = 30)

fig.show()