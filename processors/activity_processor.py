import os
import pandas as pd
import numpy as np
from typing import List

PATH: str = os.path.join('data', 'raw')
DAOSTAK_SRCS: List[str] = [os.path.join(PATH, 'daostack_proposals.csv'), os.path.join(PATH, 'daostack_stakes.csv'), os.path.join(PATH, 'daostack_votes.csv')]
DAOHAUS_SRCS: List[str] = [os.path.join(PATH, 'daohaus_proposals.csv'), os.path.join(PATH, 'daohaus_rage_quits.csv'), os.path.join(PATH, 'daohaus_votes.csv')]
ARAGON_SRCS: List[str] = [os.path.join(PATH, 'aragon_casts.csv'), os.path.join(PATH, 'aragon_transactions.csv'), os.path.join(PATH, 'aragon_votes.csv')]

def get_df(srcs: List[str]) -> pd.DataFrame:
    df: pd.DataFrame = pd.DataFrame()

    for src in srcs:
        df = pd.concat([df, pd.read_csv(src, header=0)], axis=0, ignore_index=True)

    return df


def clean_df(df: pd.DataFrame, col: str) -> pd.DataFrame:
    dff: pd.DataFrame = df
    dff.loc[:, col] = dff[col]
    dff.rename(columns={col: 'date'}, inplace=True)
    return dff


def process_activity(df: pd.DataFrame) -> pd.DataFrame:
    dff: pd.DataFrame = df
    dff.loc[:, 'date'] = pd.to_datetime(dff.loc[:, 'date'], unit='s').dt.date
    dff = dff.groupby('date').size().reset_index(name='actions')

    # fill gaps
    first = dff['date'].min()
    last = dff['date'].max()
    idx = pd.date_range(start=first, end=last, freq='D')
    filler = pd.DataFrame({'date': idx, 'actions': 0})

    dff = dff.append(filler, ignore_index=True)
    dff.loc[:, 'date'] = pd.to_datetime(dff.loc[:, 'date']).dt.date
    dff.drop_duplicates(subset='date', keep='first', inplace=True)
    dff.sort_values('date', inplace=True)

    # to unix timestamp
    dates = dff['date'].tolist()
    dff.loc[:, 'date'] = pd.DatetimeIndex(dates).astype(np.int64) // 10**9

    return dff


if __name__ == '__main__':
    daostack: pd.DataFrame = get_df(srcs=DAOSTAK_SRCS)
    daostack = clean_df(df=daostack, col='createdAt')
    daostack = process_activity(df=daostack)
    daostack.to_csv(os.path.join('data', 'daostack_activity.csv'), index=False)

    daohaus: pd.DataFrame = get_df(srcs=DAOHAUS_SRCS)
    daohaus = clean_df(df=daohaus, col='createdAt')
    daohaus = process_activity(df=daohaus)
    daohaus.to_csv(os.path.join('data', 'daohaus_activity.csv'), index=False)

    aragon: pd.DataFrame = get_df(srcs=ARAGON_SRCS)
    # you have to changes aragon.csv date attr name to 'createdAt'
    aragon = clean_df(df=aragon, col='createdAt')
    aragon = process_activity(df=aragon)
    aragon.to_csv(os.path.join('data', 'aragon_activity.csv'), index=False)
