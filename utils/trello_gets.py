# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 23:06:09 2022

@author: Josa - josageof@gmail.com
"""


# from IPython import get_ipython
# get_ipython().magic('reset -f')

# from tqdm import tqdm

from credentials import api_key, token, board_id
import json
import urllib3
import requests
import pandas as pd
from datetime import datetime

urllib3.disable_warnings()

# import pytz

# %% Definitions


def get(url, params):
    response = requests.get(url=url, params=params, verify=False)
    if response.status_code != 200:
        return None
    data = response.json()
    return data


def get_creation_dt(dt_id):
    id_trim = int(dt_id[0:8], 16)
    creation_time = datetime.fromtimestamp(id_trim)
    # utc_creation_time = pytz.utc.localize(creation_time)
    return creation_time


def string2time(string):
    if not string:
        return None
    else:
        return pd.to_datetime(string)


def formatDate(time):
    try:
        return pd.Timestamp(time).strftime('%Y-%m-%d %H:%M:%S')
    except:
        pass


def getEffortValue(df):
    if df.empty:  # nao tem sumUp defindo
        return 0
    # tem sumUp vazio defindo
    elif json.loads(df["value"][0])["cardData"]["sumUpValues"][0]["value"] == "":
        return 0
    else:
        # tem sumUp valido
        return int(json.loads(df["value"][0])["cardData"]["sumUpValues"][0]["value"])


def cardsPerBoard():
    # ==== Cards per board
    url_board_card = f"https://api.trello.com/1/boards/{board_id}/cards"
    params = dict(fields="id,name", key=api_key, token=token)

    # Get the response and parse to DF
    data = get(url_board_card, params)

    cards_df = pd.DataFrame(data).sort_values("id").reset_index(drop=True)

    # Get the datatime card
    cards_df["card_creation_dt"] = cards_df["id"].apply(get_creation_dt)
    # Rename the columns id and name to card_id and card_name
    cards_df = cards_df.rename(columns={"id": "card_id", "name": "card_name"})
    return cards_df


def listsPerBoard():
    # ==== Lists per board
    url_board_lists = f"https://api.trello.com/1/boards/{board_id}/lists"
    params = dict(fields="id,name", cards="none", key=api_key, token=token)

    cols_to_rename = ["list_id", "list_name"]

    response = get(url_board_lists, params=params)

    lists_df = pd.json_normalize(response, sep='_')
    lists_df.columns = cols_to_rename

    lists_df["list_creation_dt"] = lists_df["list_id"].apply(get_creation_dt)
    lists_df = lists_df.sort_values('list_creation_dt')
    # lists_df.to_csv("data/lists.csv", index=False, encoding='utf-8-sig')
    return lists_df


def membersPerBoard():
    # ==== Members per board
    url_board_lists = f"https://api.trello.com/1/boards/{board_id}/members"

    cols_to_rename = ["member_id", "member_fullName", "member_username"]
    params = dict(key=api_key, token=token)

    response = get(url_board_lists, params=params)

    members_df = pd.json_normalize(response, sep='_')
    members_df = members_df.rename(columns=dict(
        zip(members_df.columns, cols_to_rename)))
    # members_df.to_csv("data/members.csv", index=False, encoding='utf-8-sig')
    return members_df


def addCardsData(cards_df):
    # ==== Add data to cards_df
    list_lists = list()
    list_members = list()
    list_efforts = list()
    list_start_times = list()
    list_end_times = list()
    list_status = list()
    list_last_activities = list()
    list_actions_df = list() ### for history...

    # Iterate over all cards to get atributes
    for i, card in cards_df.iterrows():
        card_id = card.card_id
        url_card = f"https://api.trello.com/1/cards/{card_id}"
        url_card_effort = f"https://api.trello.com/1/cards/{card_id}/pluginData"
        url_card_history = f"https://api.trello.com/1/cards/{card_id}/actions"  ### for history...

        params = dict(key=api_key, token=token)

        response = get(url_card, params)
        response_effort = get(url_card_effort, params)
        response_history = get(url_card_history, params)  ### for history...

        list_id = response['idList']
        member_id = response['idMembers']
        pluginData_df = pd.json_normalize(response_effort, sep='_')
        card_start_time = string2time(response['start'])
        card_end_time = string2time(response['due'])
        status = response['dueComplete']   # completed or not?
        last_activity = string2time(response['dateLastActivity'])
        actions_df = pd.json_normalize(response_history, sep='_')   ### for history...

        list_lists.append(list_id)
        list_members.append(member_id)
        list_efforts.append(getEffortValue(pluginData_df))
        list_start_times.append(card_start_time)
        list_end_times.append(card_end_time)
        list_status.append(status)
        list_last_activities.append(last_activity)
        list_actions_df.append(actions_df) ### for history...

    cards_df['list_id'] = list_lists
    cards_df['member_id'] = list_members
    cards_df['card_effort'] = list_efforts
    cards_df['card_start_time'] = list(map(formatDate, list_start_times))
    cards_df['card_end_time'] = list(map(formatDate, list_end_times))
    cards_df['card_status'] = list_status
    cards_df['card_last_action'] = list(map(formatDate, list_last_activities))
    return cards_df, list_actions_df ### for history...
