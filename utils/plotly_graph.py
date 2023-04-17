# -*- coding: utf-8 -*-
"""
Created on Mon Dec 26 18:21:51 2022

@author: josa -- josageof@gmail.com
"""

import plotly.graph_objs as go


template = "plotly_dark"

# %% desempenho durante o ano


def plotGraph1(df_year):

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        name="Backlog",
        x=df_year.index.to_timestamp(),
        y=df_year['effort_todo'],
        text=df_year['effort_todo'],
        stackgroup='one',
        mode='lines',
        # line=dict(shape='spline'),
        textfont_color='white',
    ))
    fig.add_trace(go.Scatter(
        name="Sprint Backlog",
        x=df_year.index.to_timestamp(),
        y=df_year['effort_todo'] + df_year['effort_doing'],
        text=df_year['effort_doing'],
        stackgroup='one',
        mode='lines',
        # line=dict(shape='spline'),
        textfont_color='white',
    ))
    fig.add_trace(go.Scatter(
        name="Sprint Completed",
        x=df_year.index.to_timestamp(),
        y=df_year['effort_todo'] +
        df_year['effort_doing'] + df_year['effort_done'],
        text=df_year['effort_done'],
        stackgroup='one',
        mode='lines',
        # line=dict(shape='spline'),
        textfont_color='white',
    ))

    fig.update_layout(xaxis=dict(dtick="M1"))

    fig.update_layout(legend=dict(x=.85, y=1.3),
                      legend_traceorder="normal")

    # year = pd.to_datetime("today").year

    fig.update_layout({"title": 'Performance in the last 12 months',
                       # "title": f'Desempenho durante o ano de {year}'
                       "xaxis": {"title": "Month"},
                       "yaxis": {"title": "Effort"},
                       "showlegend": True},
                      titlefont=dict(size=24),
                      template=template)

    # fig.write_html('graph1.html')
    return fig


# %% desempenho nas últimas 4 semanas
def plotGraph2(df_month):

    fig = go.Figure(
        data=[go.Bar(
            name="Backlog",
            x=df_month.index.to_timestamp(),
            y=df_month['effort_todo'],
            text=df_month['effort_todo'],
            textfont_color='white',
            marker=dict(
                color='rgba(99, 110, 250, 0.6)',
                line=dict(color='rgba(99, 110, 250, 1.0)', width=2)
            )
        ),
            go.Bar(
            name="Sprint Backlog",
            x=df_month.index.to_timestamp(),
            y=df_month['effort_doing'],
            text=df_month['effort_doing'],
            textfont_color='white',
            marker=dict(
                color='rgba(239, 85, 59, 0.6)',
                line=dict(color='rgba(239, 85, 59, 1.0)', width=2)
            )
        ),
            go.Bar(
            name="Sprint Completed",
            x=df_month.index.to_timestamp(),
            y=df_month['effort_done'],
            text=df_month['effort_done'],
            textfont_color='white',
            marker=dict(
                color='rgba(2, 204, 150, 0.6)',
                line=dict(color='rgba(2, 204, 150, 1.0)', width=2)
            )
        ),
        ])

    # fig.update_layout(xaxis = dict(dtick = "M1"))

    fig.update_layout(legend=dict(x=.8, y=1.3))

    fig.update_layout({"title": 'Performance in the last 4 weeks',
                       "xaxis": {"title": "Week"},
                       "yaxis": {"title": "Effort"},
                       "showlegend": True},
                      titlefont=dict(size=24),
                      template=template)

    # fig.write_html('graph2.html')
    return fig


# %% progresso semanal do time
def plotGraph3(df_member):

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Planned Completed",
        x=df_member['effort_planned_done'],
        y=df_member.index,
        text=df_member['effort_planned_done'],
        orientation='h',
        textfont_color='white',
        marker=dict(
            color='rgba(2, 204, 150, 0.6)',
            line=dict(color='rgba(2, 204, 150, 1.0)', width=2)
        )
    ))
    fig.add_trace(go.Bar(
        name="Extra Completed",
        x=df_member['effort_extra_done'],
        y=df_member.index,
        text=df_member['effort_extra_done'],
        orientation='h',
        textfont_color='white',
        marker=dict(
            color='rgba(253, 157, 7, 0.6)',
            line=dict(color='rgba(253, 157, 7, 1.0)', width=2)
        )
    ))
    fig.add_trace(go.Bar(
    name="Sprint Backlog",
    x=df_member['effort_doing'],
    y=df_member.index,
    text=df_member['effort_doing'],
    orientation='h',
    textfont_color='white',
    marker=dict(
        color='rgba(239, 85, 59, 0.6)',
        line=dict(color='rgba(239, 85, 59, 1.0)', width=2)
        )
    ))

    fig.update_layout(barmode="stack")

    fig.update_layout(legend=dict(x=.8, y=1.3))

    fig.update_layout({"title": 'Weekly team progress',
                       "xaxis": {"title": "Effort"},
                       "yaxis": {"title": "Member"},
                       "showlegend": True},
                      titlefont=dict(size=24),
                      template=template)

    # fig.write_html('graph3.html')
    return fig


# %% esforço total por tipo de tarefa
def plotGraph4(df_task_type):

    fig = go.Figure()
    fig.add_trace(go.Pie(labels=df_task_type.index, values=df_task_type['total'],
                         textinfo='label+percent',
                         insidetextorientation='radial',
                         hole=.4,
                         textfont_color='white',
                         ))

    fig.update_traces(marker=dict(colors=['rgba(2, 204, 150, 0.6)',
                                          'rgba(99, 110, 250, 0.6)',
                                          'rgba(239, 85, 59, 0.6)',
                                          'rgba(171, 99, 250, 0.6)',
                                          'rgba(253, 157, 7, 0.6)'],
                                  line=dict(color=['rgba(2, 204, 150, 1.0)',
                                                   'rgba(99, 110, 250, 1.0)',
                                                   'rgba(239, 85, 59, 1.0)',
                                                   'rgba(171, 99, 250, 1.0)',
                                                   'rgba(253, 157, 7, 1.0)'], width=2)))

    # fig.update_layout(
    #     title=dict(text="Distribuição",
    #                font=dict(size=22,),
    #             xanchor='left',
    #             yanchor='middle',
    #                x=0,
    #                y=.5,
    #                xref='paper',
    #                yref='paper'))

    fig.add_annotation(text="Effort distribution",
                       font=dict(size=24),
                       showarrow=False,
                       textangle=-90,
                       x=-0.05,
                       y=.5,
                       )

    fig.update_layout(
        showlegend=False,
        margin=dict(l=70, r=30, b=30, t=30),
        template=template,
    )

    # fig.write_html('graph4.html')
    return fig
