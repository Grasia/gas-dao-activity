import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime


def to_datetime(tup):
    x, y = tup
    return datetime.strptime(f'{x}/{y}/2000', '%d/%m/%Y')


if __name__ == '__main__':
    gas: pd.DataFrame = pd.read_csv(os.path.join('data', 'avg_gas_price.csv'), header=0)
    #activity: pd.DataFrame = pd.read_csv(os.path.join('data', 'daostack_activity.csv'), header=0)
    #activity: pd.DataFrame = pd.read_csv(os.path.join('data', 'daohaus_activity.csv'), header=0)
    #activity: pd.DataFrame = pd.read_csv(os.path.join('data', 'daostack_activity_membership_rate.csv'), header=0)

    gas.loc[:, 'UnixTimeStamp'] = pd.to_datetime(gas.loc[:, 'UnixTimeStamp'], unit='s')

    gas1 = gas.copy()

    gas1.loc[:,:] = gas1[gas1['UnixTimeStamp'] >= datetime.strptime('1/1/2019', '%d/%m/%Y')]
    gas1.loc[:,:] = gas1[gas1['UnixTimeStamp'] < datetime.strptime('1/1/2020', '%d/%m/%Y')]
    gas1.dropna(inplace=True)
    gas1.reset_index(inplace=True)

    gas1['day'] = gas1['UnixTimeStamp'].dt.day
    gas1['month'] = gas1['UnixTimeStamp'].dt.month

    gas1['date'] = list(map(to_datetime, zip(gas1['day'], gas1['month'])))


    gas2 = gas.copy()

    gas2.loc[:,:] = gas2[gas2['UnixTimeStamp'] >= datetime.strptime('1/1/2020', '%d/%m/%Y')]
    gas2.loc[:,:] = gas2[gas2['UnixTimeStamp'] < datetime.strptime('1/1/2021', '%d/%m/%Y')]
    gas2.dropna(inplace=True)
    gas2.reset_index(inplace=True)

    gas2['day'] = gas2['UnixTimeStamp'].dt.day
    gas2['month'] = gas2['UnixTimeStamp'].dt.month

    gas2['date'] = list(map(to_datetime, zip(gas2['day'], gas2['month'])))

    #activity.loc[:, 'date'] = pd.to_datetime(activity.loc[:, 'date'], unit='s').dt.date

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=gas1['date'].tolist(), y=gas1['Value (Wei)'].tolist(), name="2019")
    )

    fig.add_trace(
        go.Scatter(x=gas2['date'].tolist(), y=gas2['Value (Wei)'].tolist(), name="2020")
    )

    # fig.add_trace(
    #     go.Scatter(x=activity['date'].tolist(), y=activity['rateActionsMembers'].tolist(), name="Number of actions"),
    #     secondary_y=True,
    # )

    # Add figure title
    fig.update_layout(
        #title_text="Avg gas price in Gwei",
        legend={'orientation': 'h', 'x': 0, 'y': 1.1, 'font': {'size': 28}},
        xaxis={
            'tickformat': "%B",
            'ticks': 'outside',
            'ticklen': 5,
            'tickwidth': 2,
            'showline': True, 
            'linewidth': 2, 
            'linecolor': 'black',
            'showgrid': True,
            'gridwidth': 0.5,
            'gridcolor': '#B0BEC5',
            'tickfont': {'size': 28},
        },
        yaxis={
            'showgrid': True,
            'gridwidth': 0.5,
            'gridcolor': '#B0BEC5',
            'ticks': 'outside',
            'ticklen': 5,
            'tickwidth': 2,
            'showline': True, 
            'linewidth': 2, 
            'linecolor': 'black',
            'tickfont': {'size': 28},
        },
        plot_bgcolor="white",

    )

    fig.show()
