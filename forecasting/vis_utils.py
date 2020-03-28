# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#%%
import numpy as np
import pandas as pd
from plotly.offline import plot
import plotly.graph_objects as go
from plotly.subplots import make_subplots

#%%
def bar_plot(top_indexes, sum_tops_df):
    fig = go.Figure(data=[go.Bar(name='Confirmed', x=sum_tops_df['Confirmed'], y=top_indexes, orientation='h', marker_color='royalblue'),
                          go.Bar(name='Recovered', x=sum_tops_df['Recovered'], y=top_indexes, orientation='h', marker_color='Green'),
                          go.Bar(name='Deceased', x=sum_tops_df['Deceased'], y=top_indexes, orientation='h', marker_color='firebrick')])
    
    # Change the bar mode
    fig.update_layout(barmode='group')
    fig.show()
    plot(fig)


#%%
def timeseries_plot(df, title, start_date='1/22/20'):
  # df = tops_confirmed_df
  # title = 'Confirmed'
  lands = df.index
  num_lands = len(lands)
  fig = go.Figure()
  for i in range(num_lands):
    xdata = df.columns
    df_land = df.iloc[i,:]
    ydata = df_land[start_date:]
    fig.add_trace(go.Scatter(
                    x=xdata,
                    y=ydata,
                    name=df.index[i],
                    opacity=0.8))
  fig.update_layout(
      title={
          'text': title,
          'y':0.9,
          'x':0.5,
          'xanchor': 'center',
          'yanchor': 'top'},
           xaxis_title="Date",
           yaxis_title="The number of {} cases".format(title))
  fig.show()
  plot(fig)

def timeseries_plot_since(df, title, start_dates, durations):
  # df = tops_confirmed_df
  # title = 'Confirmed'
  lands = df.index
  fig = go.Figure()
  for ind in df.index:
    xdata = np.arange(0, durations[ind])#df_cince.columns
    df_cince = df.loc[:, start_dates[ind]:]
    ydata = df_cince.loc[ind, start_dates[ind]:].values
    fig.add_trace(go.Scatter(
                    x=xdata,
                    y=ydata,
                    name=ind,
                    opacity=0.8))
  fig.update_layout(
      title={
          'text': title + ' cases',
          'y':0.9,
          'x':0.5,
          'xanchor': 'center',
          'yanchor': 'top'},
      xaxis_title="Number days passed since the first case tested positive",
      yaxis_title="The number of {} cases".format(title))
      
  fig.show()
  plot(fig)


#%%
def growth_plot(df, title, delta_t):
  # df = tops_confirmed_speed
  # title = 'Confirmed'
  lands = df.index
  num_lands = len(lands)
  fig = go.Figure()
  for i in range(num_lands):
    df_land = df.iloc[i,:]
    fig.add_trace(go.Scatter(
                    x=df.columns,
                    y=df_land.values,
                    name=df.index[i],
                    opacity=0.8))
  fig.update_layout(
      title={
          'text': "Growth of {} cases".format(title),
          'y':0.9,
          'x':0.5,
          'xanchor': 'center',
          'yanchor': 'top'},
          xaxis_title="Every {} days".format(delta_t),
          yaxis_title="The number of {} cases".format(title))
  fig.show()
  plot(fig)


def growth_plot_since(df, title, delta_t):
  # df = tops_confirmed_speed
  # title = 'Confirmed'
  lands = df.index
  num_lands = len(lands)
  fig = go.Figure()
  for i in range(num_lands):
    df_land = df.iloc[i,:]
    fig.add_trace(go.Scatter(
                    x=df.columns,
                    y=df_land.values,
                    name=df.index[i],
                    opacity=0.8))
  fig.update_layout(
      title={
          'text': "Growth of {} cases".format(title),
          'y':0.9,
          'x':0.5,
          'xanchor': 'center',
          'yanchor': 'top'},
          xaxis_title="Every {} days".format(delta_t),
          yaxis_title="The number of {} cases".format(title))
  fig.show()
  plot(fig)
  
#%%
def land_plot(confirmed, deceased, recovered, confirmed_speed, deceased_speed, recovered_speed,
              confirmed_mean, deceased_mean, recovered_mean, confirmed_speed_mean, deceased_speed_mean, recovered_speed_mean,
              land='Iran'):
  
  fig = make_subplots(rows=2, cols=1)
  fig.add_trace(go.Scatter(x=confirmed.columns[1:],
                           y=confirmed.iloc[:,1:].values[0],
                           name='Confirmed', opacity=0.8, mode='lines', line = dict(color='royalblue')), row=1, col=1)
  
  fig.add_trace(go.Scatter(x=deceased.columns[1:],
                           y=deceased.iloc[:,1:].values[0],
                           name='Deceased', opacity=0.8, mode='lines', line = dict(color='firebrick')), row=1, col=1)

  fig.add_trace(go.Scatter(x=recovered.columns[1:],
                           y=recovered.iloc[:,1:].values[0],
                           name='Recovered', opacity=0.8, mode='lines', line = dict(color='green')), row=1, col=1)

  fig.add_trace(go.Scatter(x=confirmed_speed.columns[1:],
                           y=confirmed_speed.iloc[:,1:].values[0],
                           name='Confirmed Speed', opacity=0.8, mode='lines', line = dict(color='royalblue')), row=2, col=1)
  
  fig.add_trace(go.Scatter(x=deceased_speed.columns[1:],
                           y=deceased_speed.iloc[:,1:].values[0],
                           name='Deceased Speed', opacity=0.8, mode='lines', line = dict(color='firebrick')), row=2, col=1)
  
  fig.add_trace(go.Scatter(x=recovered_speed.columns[1:],
                           y=recovered_speed.iloc[:,1:].values[0],
                           name='Recovered Speed', opacity=0.8, mode='lines', line = dict(color='green')), row=2, col=1)
  

  #### Mean
  dates = confirmed.columns[1:]
  num_days = len(dates)
  confirmed_mean_vec = confirmed_mean*np.ones(num_days)
  deceased_mean_vec = deceased_mean*np.ones(num_days)
  recovered_mean_vec = recovered_mean*np.ones(num_days)
  confirmed_speed_mean_vec = confirmed_speed_mean*np.ones(num_days)
  deceased_speed_mean_vec = deceased_speed_mean*np.ones(num_days)
  recovered_speed_mean_vec = recovered_speed_mean*np.ones(num_days)

  fig.add_trace(go.Scatter(x=confirmed.columns[1:],
                           y=confirmed_mean_vec,
                           name='Confirmed Mean', opacity=0.8, line = dict(color='royalblue', dash='dash')), row=1, col=1)
  
  fig.add_trace(go.Scatter(x=deceased.columns[1:],
                           y=deceased_mean_vec,
                           name='Deceased Mean', opacity=0.8, line = dict(color='firebrick', dash='dash')), row=1, col=1)

  fig.add_trace(go.Scatter(x=recovered.columns[1:],
                           y=recovered_mean_vec,
                           name='Recovered Meam', opacity=0.8, line = dict(color='green', dash='dash')), row=1, col=1)
  
  fig.add_trace(go.Scatter(x=confirmed_speed.columns[1:],
                           y=confirmed_speed_mean_vec,
                           name='Confirmed Speed Mean', opacity=0.8, line = dict(color='royalblue', dash='dash')), row=2, col=1)
  
  fig.add_trace(go.Scatter(x=deceased_speed.columns[1:],
                           y=deceased_speed_mean_vec,
                           name='Deceased Speed Mean', opacity=0.8, line = dict(color='firebrick', dash='dash')), row=2, col=1)

  fig.add_trace(go.Scatter(x=recovered_speed.columns[1:],
                           y=recovered_speed_mean_vec,
                           name='Recovered Speed Meam', opacity=0.8, line = dict(color='green', dash='dash')), row=2, col=1)
  
  fig.update_layout(title={'text': land, 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'})
  fig.show()


#%%
  
def rate_plot(mortality_rate, recovery_rate, land='Iran'):
  fig = go.Figure()
  fig.add_trace(go.Scatter(x=mortality_rate.columns[1:],
                           y=mortality_rate.iloc[:,1:].values[0],
                           name='Mortality Rate', opacity=0.8, mode='lines', 
                           line = dict(color='firebrick')))
  
  fig.add_trace(go.Scatter(x=recovery_rate.columns[1:],
                           y=recovery_rate.iloc[:,1:].values[0],
                           name='Recovery Rate', opacity=0.8, mode='lines', 
                           line = dict(color='green')))
  fig.update_layout(title={'text': 'Mortality and Recovery Rates in {}'.format(land), 'y':0.9, 'x':0.5, 'xanchor': 'center', 'yanchor': 'top'})
  fig.show()