import os
import warnings
import itertools
import numpy as np
import matplotlib.pyplot as plt
from pylab import rcParams
import pandas as pd
from datetime import datetime
from statsmodels.tsa.stattools import acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import statsmodels.api as sm
import matplotlib

FIRST_SLICE_DATE: datetime = datetime.strptime('1/10/2018', '%d/%m/%Y')
SECOND_SLICE_DATE: datetime = datetime.strptime('1/5/2020', '%d/%m/%Y')


def filter_series(df: pd.DataFrame, date_key: str, slice1: datetime, slice2: datetime) -> pd.DataFrame:
    dff: pd.DataFrame = df
    dff.loc[:, date_key] = pd.to_datetime(dff.loc[:, date_key], unit='s')

    dff.loc[:, :] = dff[dff[date_key] >= slice1]
    dff.loc[:, :] = dff[dff[date_key] <= slice2]

    return dff


if __name__ == '__main__':
    df: pd.DataFrame = pd.read_csv(os.path.join('data', 'avg_gas_price.csv'), header=0)
    #activity: pd.DataFrame = pd.read_csv(os.path.join('data', 'daostack_activity.csv'), header=0)
    #activity: pd.DataFrame = pd.read_csv(os.path.join('data', 'daohaus_activity.csv'), header=0)
    #activity: pd.DataFrame = pd.read_csv(os.path.join('data', 'aragon_activity.csv'), header=0)

    df = filter_series(df=df, date_key='UnixTimeStamp', slice1=FIRST_SLICE_DATE, slice2=SECOND_SLICE_DATE)
    df = df.set_index('UnixTimeStamp')
    df = df.dropna()

    # original
    df['Value (Wei)'].plot(figsize = (15, 6))
    plt.show()

    # difference
    # df['diff'] = df['Value (Wei)'] - df['Value (Wei)'].shift(1)
    # df = df.dropna()
    # df['diff'].plot(figsize = (15, 6))
    # plt.show()

    # season difference
    # df['diff_7'] = df['diff'] - df['diff'].shift(7)
    # df = df.dropna()
    # df['diff_7'].plot(figsize = (15, 6))
    # plt.show()

    # rcParams['figure.figsize'] = 18, 8
    # decomposition = sm.tsa.seasonal_decompose(x=df['diff_7'], model='additive')
    # fig = decomposition.plot()
    # plt.show()

    # plot_acf(df['diff_7'])
    # matplotlib.pyplot.show()
    # plot_pacf(df['diff_7'])
    # matplotlib.pyplot.show()
