# -*- coding: utf-8 -*-
"""
Created on Sun Aug 14 23:06:09 2022

@author: Josa - josageof@gmail.com

"""

# %% Imports

# from IPython import get_ipython
# get_ipython().magic('reset -f')

import pandas as pd
from datetime import datetime
# import time

from utils.trello_gets import cardsPerBoard, listsPerBoard, membersPerBoard, addCardsData
from config import current_storage_file, history_storage_file


# %% main function
def getTrelloData():

    start_time = datetime.now()

    cards_df = cardsPerBoard()
    lists_df = listsPerBoard()
    members_df = membersPerBoard()
    cards_df, list_actions_df = addCardsData(cards_df) ### history...

    # agrega todas as actions de todos os cards na actions_df
    actions_df = pd.concat(list_actions_df) ### history...

    # remove os cards de soma
    cards_df = cards_df[~cards_df["card_name"].str.contains('|'.join(['soma:']), case=False)]
    actions_df = actions_df[~actions_df["data_card_name"].str.contains('|'.join(['soma:']), case=False)] ### history...

    # insere o list_name baseado no list_id
    cards_df = pd.merge(cards_df, lists_df, on="list_id", how='inner')

    # insere o member_name baseado no member_id
    cards_df = cards_df.explode('member_id')
    cards_df = pd.merge(cards_df, members_df, on="member_id", how='outer')

    # calcula o tempo de esforco em horas
    cards_df["card_elapsed_time"] = (pd.to_datetime(cards_df["card_end_time"]) -
                                     pd.to_datetime(cards_df["card_start_time"])) / pd.Timedelta(hours=1)

    # reposiciona as colunas do card_df
    cards_df = cards_df[[
        'list_id',
        'list_name',
        'list_creation_dt',
        'member_id',
        'member_username',
        'member_fullName',
        'card_id',
        'card_name',
        'card_creation_dt',
        'card_start_time',
        'card_end_time',
        'card_elapsed_time',
        'card_effort',
        'card_last_action',
        'card_status',
    ]]

    # cards_df.sort_values(by=['list_name', 'card_last_action']).to_csv(
    #     "data/cards.csv", index=False, sep=';', encoding='utf-8-sig')
    cards_df.sort_values(by=['list_name', 'card_last_action']).to_pickle(current_storage_file)


    # cria list_id e list_name para o histórico ### history...
    actions_df["list_id"] = actions_df["data_listBefore_id"].astype(str).replace("nan","") + \
                                    actions_df["data_list_id"].astype(str).replace("nan","")
    actions_df["list_name"] = actions_df["data_listBefore_name"].astype(str).replace("nan","") + \
                                    actions_df["data_list_name"].astype(str).replace("nan","")

    # limpa actions inuteis ### history...
    actions_df = actions_df[~actions_df["list_name"].str.contains("----", case=False)]


    # resume as actions no final de cada semana: todo, doing, done ### history...
    actions_df.to_pickle(history_storage_file)


    end_time = datetime.now()
    # print('Duration: {}'.format(end_time - start_time))
    print('Read finish: {}'.format(end_time), "--",
          'Duration: {}'.format(end_time - start_time))


def main():
    while True:
        try:
            getTrelloData()
            # time.sleep(600)
        except:
            pass
        # break


if __name__ == "__main__":
    main()
