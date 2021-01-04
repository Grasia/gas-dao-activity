import os
import pandas as pd
import numpy as np
from typing import List

DAOSTAK_SRCS: List[str] = [os.path.join('data', 'daostack_membership.csv'), os.path.join('data', 'daostack_activity.csv')]
DAOHAUS_SRCS: List[str] = [os.path.join('data', 'daohaus_membership.csv'), os.path.join('data', 'daohaus_activity.csv')]


def get_df(src: str) -> pd.DataFrame:
    return pd.read_csv(src, header=0)


def unix_to_date(df: pd.DataFrame) -> pd.DataFrame:
    dff: pd.DataFrame = df
    dff.loc[:, 'date'] = pd.to_datetime(dff.loc[:, 'date'], unit='s').dt.date
    return dff


def date_to_unix(df: pd.DataFrame) -> pd.DataFrame:
    dff: pd.DataFrame = df
    dates = dff['date'].tolist()
    dff.loc[:, 'date'] = pd.DatetimeIndex(dates).astype(np.int64) // 10**9
    return dff


def get_rate(members: pd.DataFrame, activity: pd.DataFrame) -> pd.DataFrame:
    dff: pd.DataFrame = activity
    dff = unix_to_date(dff)
    members = unix_to_date(members)

    first = members['date'].min()
    last = members['date'].max()
    idx = pd.date_range(start=first, end=last, freq='D')
    filler = pd.DataFrame({'date': idx, 'actions': 0})

    dff = dff.append(filler, ignore_index=True)
    dff.loc[:, 'date'] = pd.to_datetime(dff.loc[:, 'date']).dt.date
    dff.drop_duplicates(subset='date', keep='first', inplace=True)
    dff.sort_values('date', inplace=True)

    users = members['members'].tolist()
    actions = dff['actions'].tolist()
    rate: list = []

    for i in range(len(users)):
        rate.append(actions[i] / users[i]) 

    return pd.DataFrame({'date': members['date'].tolist(), 'rateActionsMembers': rate})


if __name__ == '__main__':
    daostack_members: pd.DataFrame = get_df(src=DAOSTAK_SRCS[0])
    daostack_activity: pd.DataFrame = get_df(src=DAOSTAK_SRCS[1])
    daostack_rate: pd.DataFrame = get_rate(members=daostack_members, activity=daostack_activity)
    daostack_rate = date_to_unix(daostack_rate)
    daostack_rate.to_csv(os.path.join('data', 'daostack_activity_membership_rate.csv'), index=False)

    daohaus_members: pd.DataFrame = get_df(src=DAOHAUS_SRCS[0])
    daohaus_activity: pd.DataFrame = get_df(src=DAOHAUS_SRCS[1])
    daohaus_rate: pd.DataFrame = get_rate(members=daohaus_members, activity=daohaus_activity)
    daohaus_rate = date_to_unix(daohaus_rate)
    daohaus_rate.to_csv(os.path.join('data', 'daohaus_activity_membership_rate.csv'), index=False)
