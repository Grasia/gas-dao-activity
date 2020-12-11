import os
import statsmodels
from statsmodels.tsa.stattools import adfuller
import pandas as pd

SIGNIFICANCE: float = .05


if __name__ == '__main__':
    #gas: pd.DataFrame = pd.read_csv(os.path.join('data', 'avg_gas_price.csv'), header=0)
    #series = gas.loc[:, 'Value (Wei)'].values

    #actividad: pd.DataFrame = pd.read_csv(os.path.join('data', 'daostack_activity.csv'), header=0)
    #actividad: pd.DataFrame = pd.read_csv(os.path.join('data', 'daohaus_activity.csv'), header=0)
    actividad: pd.DataFrame = pd.read_csv(os.path.join('data', 'aragon_activity.csv'), header=0)
    series = actividad.loc[:, 'actions'].values

    adf_test = adfuller(series, autolag='AIC')
    p_value = adf_test[1]
    stationary: bool = p_value < SIGNIFICANCE

    dfResults = pd.Series(adf_test[0:4], index=['ADF Test Statistic','P-Value','# Lags Used','# Observations Used'])
    #Add Critical Values
    for key,value in adf_test[4].items():
        dfResults[f'Critical Value ({key})'] = value

    print('Augmented Dickey-Fuller Test Results:')
    print(dfResults)
    print(f"Is the time series stationary? {stationary}")
