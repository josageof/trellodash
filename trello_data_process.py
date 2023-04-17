# -*- coding: utf-8 -*-
"""
Created on Sat Dec 17 09:03:38 2022

@author: Josa - josageof@gmail.com
"""

import pandas as pd
import pickle as pkl

from config import current_storage_file, history_storage_file
from config import processed_storage_file
from utils.data_process import processCurrentData, processHistoryData
from utils.data_process import processGraphData1, processGraphData2, processGraphData3, processGraphData4
from utils.data_process import processFieldData


def processTrelloData():

    # Lê os dados importados do card atual
    df = pd.read_pickle(current_storage_file)
    
    # Lê os dados importados dos cards arquivados
    df_history = pd.read_pickle(history_storage_file)   ## history...
    
            
    # resume os dados atuais (cards no quadro)
    df_todo, df_doing, df_done = processCurrentData(df)
    
    # resume os dados do histórico (cards arquivados)
    df_h_month, df_h_year, df_h_todo, df_h_doing, df_h_done = processHistoryData(df, df_history)   ## history ...
    
    
    # ==== resume os 3 dataframes para o ano corrente                          (p/ plotGraph1)
    df_year = processGraphData1(df_todo, df_doing, df_done, df_h_year)
    
    # ==== resume os 3 dataframes para os ultimos 30 dias                      (p/ plotGraph2)
    df_month = processGraphData2(df_todo, df_doing, df_done, df_h_month)
    
    # ==== resume o progresso semanal de cada member                           (p/ plotGraph3)
    df_week_member = processGraphData3(df, df_doing, df_done)
    
    # ==== resume os tipos de tarefas e a condição atual                       (p/ plotGraph4)
    df_task_type  = processGraphData4(df_todo, df_doing, df_done, df_h_todo, df_h_doing, df_h_done)
    
    # ==== resume o total de todo, doing e done                                (p/ texField)
    todo, doing, done = processFieldData(df_task_type)
    
    ## armazena todos os dados processados no dicionario data
    data = {}
    data['df_todo'] = df_todo
    data['df_doing'] = df_doing
    data['df_done'] = df_done
    data['df_h_month'] = df_h_month
    data['df_h_year'] = df_h_year
    data['df_h_todo'] = df_h_todo
    data['df_h_doing'] = df_h_doing
    data['df_h_done'] = df_h_done
    data['df_year'] = df_year
    data['df_month'] = df_month
    data['df_week_member'] = df_week_member
    data['df_task_type'] = df_task_type
    data['todo'] = todo
    data['doing'] = doing
    data['done'] = done
    
    return data


if __name__ == "__main__":
    # Salve o dicionário em um arquivo .pkl
    with open(processed_storage_file, 'wb') as f:
        pkl.dump(processTrelloData(), f)
