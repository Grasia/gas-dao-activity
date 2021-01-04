import os
import pandas as pd
import numpy as np
from typing import List
from datetime import datetime

PATH: str = os.path.join('data', 'raw')
DAOSTAK_SRCS: List[str] = [os.path.join(PATH, 'daostack_members.csv')]
DAOHAUS_SRCS: List[str] = [os.path.join(PATH, 'daohaus_members.csv'), os.path.join(PATH, 'daohaus_rage_quits.csv')]

def get_df(src: str) -> pd.DataFrame:
    return pd.read_csv(src, header=0)


def clean_df(df: pd.DataFrame, col: str) -> pd.DataFrame:
    dff: pd.DataFrame = df
    dff.loc[:, col] = dff[col]
    dff.rename(columns={col: 'date'}, inplace=True)
    return dff


def sequence_members(df: pd.DataFrame) -> pd.DataFrame:
    dff: pd.DataFrame = df
    dff.loc[:, 'date'] = pd.to_datetime(dff.loc[:, 'date'], unit='s').dt.date
    dff = dff.groupby('date').size().reset_index(name='members')

    # fill gaps
    first = dff['date'].min()
    #last = dff['date'].max()
    last = datetime.strptime('01/12/2020', "%d/%m/%Y") # fill with fix date
    idx = pd.date_range(start=first, end=last, freq='D')
    filler = pd.DataFrame({'date': idx, 'members': 0})

    dff = dff.append(filler, ignore_index=True)
    dff.loc[:, 'date'] = pd.to_datetime(dff.loc[:, 'date']).dt.date
    dff.drop_duplicates(subset='date', keep='first', inplace=True)
    dff.sort_values('date', inplace=True)

    return dff


def transform_date(df: pd.DataFrame) -> pd.DataFrame:
    # to unix timestamp
    dff: pd.DataFrame = df
    dates = dff['date'].tolist()
    dff.loc[:, 'date'] = pd.DatetimeIndex(dates).astype(np.int64) // 10**9
    return dff


def get_total_members(df: pd.DataFrame) -> pd.DataFrame:
    dff: pd.DataFrame = df
    news: List[int] = dff['members'].tolist()
    total: List[int] = [news[0]]

    for i in range(1, len(news)):
        total.append(news[i] + total[i-1])

    dff.loc[:, 'members'] = total

    return dff


def remove_outgoing_members(total: pd.DataFrame, out: pd.DataFrame) -> pd.DataFrame:
    total_: pd.DataFrame = total
    dff: pd.DataFrame = out

    first = total['date'].min()
    last = total['date'].max()
    idx = pd.date_range(start=first, end=last, freq='D')
    filler = pd.DataFrame({'date': idx, 'members': 0})

    dff = dff.append(filler, ignore_index=True)
    dff.loc[:, 'date'] = pd.to_datetime(dff.loc[:, 'date']).dt.date
    dff.drop_duplicates(subset='date', keep='first', inplace=True)
    dff.sort_values('date', inplace=True)

    members = total['members'].tolist()
    out_members = dff['members'].tolist()

    for i in range(len(members)):
        members[i] = members[i] - out_members[i]

    total_.loc[:, 'members'] = members

    return total_


if __name__ == '__main__':
    daostack_members: pd.DataFrame = get_df(src=DAOSTAK_SRCS[0])
    daostack_members = clean_df(df=daostack_members, col='createdAt')
    daostack_members = sequence_members(df=daostack_members)
    daostack_members = get_total_members(df=daostack_members)
    daostack_members = transform_date(df=daostack_members)
    daostack_members.to_csv(os.path.join('data', 'daostack_membership.csv'), index=False)

    daohaus_members: pd.DataFrame = get_df(src=DAOHAUS_SRCS[0])
    daohaus_members = clean_df(df=daohaus_members, col='createdAt')
    daohaus_members = sequence_members(df=daohaus_members)
    daohaus_members = get_total_members(df=daohaus_members)

    daohaus_quits: pd.DataFrame = get_df(src=DAOHAUS_SRCS[1])
    daohaus_quits = clean_df(df=daohaus_quits, col='createdAt')
    daohaus_quits = sequence_members(df=daohaus_quits)
    daohaus_members = remove_outgoing_members(total=daohaus_members, out=daohaus_quits)

    daohaus_members = transform_date(df=daohaus_members)
    daohaus_members.to_csv(os.path.join('data', 'daohaus_membership.csv'), index=False)
