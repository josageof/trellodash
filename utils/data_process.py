# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 18:21:51 2022

@author: josa -- josageof@gmail.com
"""

import pandas as pd
from config import stage_list, task_type


def rangeWeekDate():
    # retorna o primeiro e ultimo dia da semana atual
    today = pd.to_datetime("today").date()
    first_day = pd.to_datetime(today, format="%Y-%m-%d") - pd.offsets.Week(weekday=6)
    last_day = pd.to_datetime(today, format="%Y-%m-%d") + pd.offsets.Week(weekday=5)
    return first_day, last_day


def rangeMonthDate():
    # retorna o primeiro e ultimo dia do mês atual
    today = pd.to_datetime("today").date()
    first_day = pd.to_datetime(today, format="%Y-%m-%d") - pd.offsets.MonthBegin()
    last_day = pd.to_datetime(today, format="%Y-%m-%d") + pd.offsets.MonthEnd()
    return first_day, last_day


def rangeYearDate():
    # retorna o primeiro e ultimo dia do ano atual
    today = pd.to_datetime("today").date()
    first_day = pd.to_datetime(today, format="%Y-%m-%d") - pd.offsets.YearBegin()
    last_day = pd.to_datetime(today, format="%Y-%m-%d") + pd.offsets.YearEnd()
    return first_day, last_day


def rangeLastMonth():
    # retorna o início do ultimo mês corrido e hoje
    today = pd.to_datetime("today").date()
    first_day = pd.to_datetime(today, format="%Y-%m-%d") - pd.Timedelta(days=30)
    return first_day, today


def rangeLastYear():
    # retorna o início do ultimo ano corrido e hoje
    today = pd.to_datetime("today").date()
    first_day = pd.to_datetime(today, format="%Y-%m-%d") - pd.Timedelta(days=365)
    return first_day, today


# cria uma lista de tipo de estado de tarefa
# stage_list = {"todo": "|".join(['a fazer', 'revisar', 'vencida']),
#                   "doing": "|".join(['backlog', 'andamento', 'preparação']),
#                   "done": "|".join(['concluído', 'concluido', 'calibrado'])}


def processCurrentData(df):
    # mantém apenas primeiro e ultimo nome dos membros
    df['member_fullName'] = df['member_fullName'].apply(
        lambda name: ' '.join([str(name).split()[0], str(name).split()[-1], " "]))

    # converte as colunas de data para datetime
    df['card_creation_dt'] = pd.to_datetime(
        df['card_creation_dt'], format='%Y-%m-%d %H:%M:%S')
    df['list_creation_dt'] = pd.to_datetime(
        df['list_creation_dt'], format='%Y-%m-%d %H:%M:%S')
    df['card_start_time'] = pd.to_datetime(
        df['card_start_time'], format='%Y-%m-%d %H:%M:%S')
    df['card_end_time'] = pd.to_datetime(df['card_end_time'], format='%Y-%m-%d %H:%M:%S')
    df['card_last_action'] = pd.to_datetime(
        df['card_last_action'], format='%Y-%m-%d %H:%M:%S')

    # remove qualquer linha que nao pertence a uma lista
    df = df.dropna(subset=['list_name'])

    # separa em dataframes por tipo de lista
    df_todo = df[df["list_name"].str.contains(stage_list["todo"], case=False)]
    df_doing = df[df["list_name"].str.contains(stage_list["doing"], case=False)]
    df_done = df[df["list_name"].str.contains(stage_list["done"], case=False)]
    return df_todo, df_doing, df_done


def processHistoryData(df, df_history):
    # converte a coluna date para datetime
    df_history["list_date"] = pd.to_datetime(df_history['date'], format='%Y-%m-%d %H:%M:%S')
    # df_history = resumeHistory(pd.read_pickle(historyFileName))
    df_history = df_history[["data_card_id", "list_id", "list_name", "list_date"]]
    # Renomeia a coluna 'data_card_id' para 'card_id'
    df_history = df_history.rename(columns={'data_card_id': 'card_id'})
    # Mescla os dataframes com base na coluna 'card_id'
    df_history = pd.merge(df_history, df[['card_id', 'card_effort']], on='card_id', how='left')
    # remover as linhas duplicadas
    df_history = df_history.drop_duplicates()
    # separa em dataframes por tipo de lista
    df_h_todo = df_history[df_history["list_name"].str.contains(stage_list["todo"], case=False)]
    df_h_doing = df_history[df_history["list_name"].str.contains(stage_list["doing"], case=False)]
    df_h_done = df_history[df_history["list_name"].str.contains(stage_list["done"], case=False)]

    # obtém primeiro dos ultimos 30 dias
    first_m_day, last_m_day = rangeLastMonth()  
    # cria o indice completo para o periodo em semanas
    # Utilizando a função warn() para capturar o aviso
    idx_month_w = pd.date_range(first_m_day, last_m_day, freq='W').to_period('w')
    # cria um dataframe mensal com periodo semanal como index
    df_h_month = pd.DataFrame(index=idx_month_w)
    # seta o list_date como index e reamostra semanalmente somando o effort por semana
    df_h_month['effort_todo'] = df_h_todo.set_index(
        'list_date')['card_effort'].tz_localize(None).resample('W').sum().to_period('w')
    df_h_month['effort_doing'] = df_h_doing.set_index(
        'list_date')['card_effort'].tz_localize(None).resample('W').sum().to_period('w')
    df_h_month['effort_done'] = df_h_done.set_index(
        'list_date')['card_effort'].tz_localize(None).resample('W').sum().to_period('w')
    df_h_month.fillna(0, inplace=True)
    
    # obtém primeiro dos ultimos 365 dias
    first_y_day, last_y_day = rangeLastYear()  
    # cria o indice completo para o periodo em meses
    idx_year_m = pd.date_range(first_y_day, last_y_day, freq='M').to_period('m')
    # cria um dataframe anual com periodo mensal como index
    df_h_year = pd.DataFrame(index=idx_year_m)
    # seta o list_date como index e reamostra mensalmente somando o effort por mês
    df_h_year['effort_todo'] = df_h_todo.set_index(
        'list_date')['card_effort'].tz_localize(None).resample('M').sum().to_period('m')
    df_h_year['effort_doing'] = df_h_doing.set_index(
        'list_date')['card_effort'].tz_localize(None).resample('M').sum().to_period('m')
    df_h_year['effort_done'] = df_h_done.set_index(
        'list_date')['card_effort'].tz_localize(None).resample('M').sum().to_period('m')
    df_h_year.fillna(0, inplace=True) 
    return df_h_month, df_h_year, df_h_todo, df_h_doing, df_h_done


def processGraphData1(df_todo, df_doing, df_done, df_h_year):
    # obtém o primeiro e ultimo dia do ano atual
    first_y_day, last_y_day = rangeLastYear()  
    # cria o indice completo para o periodo em meses
    idx_year_m = pd.date_range(first_y_day, last_y_day, freq='M').to_period('m')
    # cria um novo dataframe
    df_year = pd.DataFrame(index=idx_year_m)
    # seta o last_activity como index e reamostra somando o effort por mes
    ## (foi substituído card_last_action por card_end_time)
    df_year["effort_todo"] = df_todo.set_index(
        'card_end_time')['card_effort'].tz_localize(None).resample('M').sum().to_period('m')
    df_year["effort_doing"] = df_doing.set_index(
        'card_end_time')['card_effort'].tz_localize(None).resample('M').sum().to_period('m')
    df_year["effort_done"] = df_done.set_index(
        'card_end_time')['card_effort'].tz_localize(None).resample('M').sum().to_period('m')
    df_year.fillna(0, inplace=True)  # substitui nan por 0
    # soma df_year a df_h_year mantendo as celulas nao afetadas
    df_full_year = df_h_year.add(df_year, fill_value=0)
    return df_full_year


def processGraphData2(df_todo, df_doing, df_done, df_h_month):
    # obtém primeiro dos ultimos 30 dias
    first_m_day, last_m_day = rangeLastMonth()  
    # cria o indice completo para o periodo em semanas
    idx_month_w = pd.date_range(first_m_day, last_m_day, freq='W').to_period('w')
    # cria um novo dataframe com as semanas como index
    df_month = pd.DataFrame(index=idx_month_w)
    # seta o last_activity como index e reamostra somando o effort por semana
    ## (foi substituído card_last_action por card_end_time)
    df_month['effort_todo'] = df_todo.set_index(
        'card_end_time')['card_effort'].tz_localize(None).resample('W').sum().to_period('w')
    df_month['effort_doing'] = df_doing.set_index(
        'card_end_time')['card_effort'].tz_localize(None).resample('W').sum().to_period('w')
    df_month['effort_done'] = df_done.set_index(
        'card_end_time')['card_effort'].tz_localize(None).resample('W').sum().to_period('w')
    df_month.fillna(0, inplace=True)  # substitui nan por 0
    # soma df_month a df_h_month mantendo as celulas nao afetadas
    df_full_month = df_h_month.add(df_month, fill_value=0)
    return df_full_month


def processGraphData3(df, df_doing, df_done):
    # cria df_week_member com todos os membros como index
    df_week_member = pd.DataFrame(index=df['member_fullName'].unique())
    # remove o membro nan
    df_week_member = df_week_member[~df_week_member.index.str.contains("nan nan")]
    # remove o membro Francisco
    # df_week_member = df_week_member[~df_week_member.index.str.contains("Francisco")]
    # obtem o primeiro e ultimo dia da semana
    first_w_day, last_w_day = rangeWeekDate()
    # separa os dataframes da semana atual
    ## (foi substituído card_last_action por card_end_time)
    df_week_doing = df_doing.loc[(df_doing['card_end_time'] >= first_w_day) &
                                 (df_doing['card_end_time'] <= last_w_day)]
    df_week_done = df_done.loc[(df_done['card_end_time'] >= first_w_day) &
                               (df_done['card_end_time'] <= last_w_day)]
    # separa as tarefas planejadas concluídas das extras concluídas
    df_week_planned_effort = df_week_done[~df_week_done["card_name"].str.contains("extra", case=False)]
    df_week_extra_effort = df_week_done[df_week_done["card_name"].str.contains("extra", case=False)]
    # soma o effort por cada member
    df_week_member['effort_doing'] = [df_week_doing[df_week_doing['member_fullName'] == member]['card_effort'].sum()
                                      for member in df_week_member.index]
    df_week_member['effort_done'] = [df_week_done[df_week_done['member_fullName'] == member]['card_effort'].sum()
                                     for member in df_week_member.index]
    df_week_member['effort_planned_done'] = [df_week_planned_effort[df_week_planned_effort['member_fullName'] == member]['card_effort'].sum()
                                             for member in df_week_member.index]
    df_week_member['effort_extra_done'] = [df_week_extra_effort[df_week_extra_effort['member_fullName'] == member]['card_effort'].sum()
                                           for member in df_week_member.index]
    return df_week_member


def processGraphData4(df_todo, df_doing, df_done, df_h_todo, df_h_doing, df_h_done):
    # soma separadamente o total de todo, doing e done
    df_task_type = pd.DataFrame(index=task_type)
    df_task_type["todo"] = [df_todo[df_todo["list_name"].str.contains(task, case=False)]['card_effort'].sum()
                            for task in df_task_type.index]
    df_task_type["doing"] = [df_doing[df_doing["list_name"].str.contains(task, case=False)]['card_effort'].sum()
                             for task in df_task_type.index]
    df_task_type["done"] = [df_done[df_done["list_name"].str.contains(task, case=False)]['card_effort'].sum()
                            for task in df_task_type.index]
    df_task_type["h_todo"] = [df_h_todo[df_h_todo["list_name"].str.contains(task, case=False)]['card_effort'].sum()   ## history ...
                            for task in df_task_type.index]
    df_task_type["h_doing"] = [df_h_doing[df_h_doing["list_name"].str.contains(task, case=False)]['card_effort'].sum()   ## history ...
                             for task in df_task_type.index]
    df_task_type["h_done"] = [df_h_done[df_h_done["list_name"].str.contains(task, case=False)]['card_effort'].sum()   ## history ...
                            for task in df_task_type.index]
    # adiciona ao df_task_type o esforço total pelo tipo de tarefa
    df_task_type["total"] = df_task_type.sum(axis=1)
    return df_task_type


def processFieldData(df_task_type):
    # soma as tarefas a fazer (p/ texField1)
    todo = int(df_task_type["todo"].sum() + df_task_type["h_todo"].sum())
    # soma as tarefas que estão sendo feitas (p/ texField2)
    doing = int(df_task_type["doing"].sum() + df_task_type["h_doing"].sum())
    # soma as tarefas feitas (p/ texField3)
    done = int(df_task_type["done"].sum() + df_task_type["h_done"].sum())
    return todo, doing, done 

