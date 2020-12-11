import os
import statsmodels
from statsmodels.tsa.stattools import kpss
import pandas as pd

SIGNIFICANCE: float = 0.05


if __name__ == '__main__':
    # gas: pd.DataFrame = pd.read_csv(os.path.join('data', 'avg_gas_price.csv'), header=0)
    # series = gas.loc[:, 'Value (Wei)'].values

    #actividad: pd.DataFrame = pd.read_csv(os.path.join('data', 'daostack_activity.csv'), header=0)
    #actividad: pd.DataFrame = pd.read_csv(os.path.join('data', 'daohaus_activity.csv'), header=0)
    actividad: pd.DataFrame = pd.read_csv(os.path.join('data', 'aragon_activity.csv'), header=0)
    series = actividad.loc[:, 'actions'].values

    statistic, p_value, n_lags, critical_values = kpss(series, nlags="auto", regression='c')
    print(f'KPSS Statistic: {statistic}')
    print(f'p-value: {p_value}')
    print(f'num lags: {n_lags}')
    print('Critial Values:')

    for key, value in critical_values.items():
        print(f'   {key} : {value}')

    print(f'Result: The series is {"not " if p_value < SIGNIFICANCE else ""}stationary')
