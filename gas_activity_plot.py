import os
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots


if __name__ == '__main__':
    gas: pd.DataFrame = pd.read_csv(os.path.join('data', 'avg_gas_price.csv'), header=0)
    #activity: pd.DataFrame = pd.read_csv(os.path.join('data', 'daostack_activity.csv'), header=0)
    #activity: pd.DataFrame = pd.read_csv(os.path.join('data', 'daohaus_activity.csv'), header=0)
    activity: pd.DataFrame = pd.read_csv(os.path.join('data', 'aragon_activity.csv'), header=0)

    gas.loc[:, 'UnixTimeStamp'] = pd.to_datetime(gas.loc[:, 'UnixTimeStamp'], unit='s').dt.date
    activity.loc[:, 'date'] = pd.to_datetime(activity.loc[:, 'date'], unit='s').dt.date

    # Create figure with secondary y-axis
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add traces
    fig.add_trace(
        go.Scatter(x=gas['UnixTimeStamp'].tolist(), y=gas['Value (Wei)'].tolist(), name="Avg gas price (Wei)"),
        secondary_y=False,
    )

    fig.add_trace(
        go.Scatter(x=activity['date'].tolist(), y=activity['actions'].tolist(), name="Number of actions"),
        secondary_y=True,
    )

    # Add figure title
    fig.update_layout(
        title_text="Gas price vs DAOs actions",
        legend={'orientation': 'h', 'x': 0, 'y': 1.2}
    )

    fig.show()
