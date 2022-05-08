import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd

path = "/home/balint831/scimod/data/shallow/meas_lr1_s20_d10.csv"

def plot_energy(path, par):
    

    assert isinstance(path,str), "path must be string"
    assert par in [0,1], "Parity is either 0 or 1"
    df = pd.read_csv(path)

    updates = df["update"].max() + 1
    fig = go.Figure()
    
    
    fig = make_subplots(
        rows=2, cols=2,
        specs=[[{"colspan": 2}, None],
                    [{}, {}]],            
            #! row_heights
        subplot_titles=("Energy distribution","Mean energy", "Minimum energy"))


    for update in range( updates ):

        fig.add_trace(
            
            go.Bar( 
                visible = False,
                x = df[ (df["update"] == update) & (df["parity"] == par)  ].groupby("energy").count().index,
                y = df[ (df["update"] == update) & (df["parity"] == par)  ].groupby("energy").count()["Unnamed: 0"],
                showlegend = False
                ), row = 1, col = 1
        )

    fig.add_trace(go.Scatter(
                    visible = True,
                    y = df[ df["parity"] == 0].groupby("update").energy.mean(),
                    x = df[ df["parity"] == 0].groupby("update").energy.mean().index,
                    name = "<E> - parity 0"
                    ), row = 2, col = 1)

    fig.add_trace(go.Scatter(
                    visible = True,
                    y = df[ df["parity"] == 1].groupby("update").energy.mean(),
                    x = df[ df["parity"] == 1].groupby("update").energy.mean().index,
                    name = "<E> - parity 1"
                    ), row = 2, col = 1)

    fig.add_trace(go.Scatter(
                    visible = True,
                    y = df[ df["parity"] == 0].groupby("update").energy.min(),
                    x = df[ df["parity"] == 0].groupby("update").energy.min().index,
                    name = "min(E) - parity 0"
                    ), row = 2, col = 2)

    fig.add_trace(go.Scatter(
                    visible = True,
                    y = df[ df["parity"] == 1].groupby("update").energy.min(),
                    x = df[ df["parity"] == 1].groupby("update").energy.min().index,
                    name = "min(E) - parity 1"
                    ), row = 2, col = 2)


    # ! megváltozhat más parityre
    ylim = df[ (df["update"] == update) & (df["parity"] == par)  ].groupby("energy").count()["Unnamed: 0"].max()
    fig.update_yaxes(range=[0, ylim], row = 1, col = 1)
    fig.update_xaxes(range=[df.energy.min(), df.energy.max()], row = 1, col = 1)

    fig.update_yaxes(title_text = "Count", row = 1, col = 1)
    fig.update_xaxes(title_text = "E", row = 1, col = 1)

    fig.update_xaxes(title_text = "Update", row = 2, col = 1)
    fig.update_yaxes(title_text = "<E>", row = 2, col = 1)

    fig.update_xaxes(title_text = "Update", row = 2, col = 2)
    fig.update_yaxes(title_text = "min(E)", row = 2, col = 2)

    fig.data[0].visible = True

    steps = []
    for i in range( updates ):
        step = dict(
            method="update",
            args=[{"visible": [False] * ( updates + 4)},
                {"title": "Update: " + str(i)}],  # layout attribute
        )
        
        step["args"][0]["visible"][i] = True  # Toggle i'th trace to "visible"
        step["args"][0]["visible"][-2] = True
        step["args"][0]["visible"][-1] = True
        step["args"][0]["visible"][-3] = True
        step["args"][0]["visible"][-4] = True
        
        steps.append(step)


    sliders = [dict(
        active = 0,
        currentvalue={"prefix": "Update: "},
        pad={"t": updates},
        steps=steps
    )]

    fig.update_layout(
        sliders=sliders,
        bargap=0.15
    )

    fig.show()
""" fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="right",
                x=0.7,
                y=1.2,
                showactive=True,
                buttons=list(
                    [
                        dict(
                            label="Parity 0",
                            method="update",
                            args=[{"sliders":}],
                        ),
                        dict(
                            label="Parity 1",
                            method="update",
                            args=[{"y": [df["scoops"], [0] * updates, [0] * updates,[0] * updates,[0] * updates]}],
                        ),
                    ]
                ),
            )
        ]
    )"""

    
