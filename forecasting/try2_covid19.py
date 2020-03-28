# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 22:01:10 2020

@author: rkako
"""

#%% Import Packeges
import os
from get_dataset import Get_DataSet
from vis_utils import bar_plot, timeseries_plot, timeseries_plot_since, growth_plot, land_plot, rate_plot
from get_top_lands import GetTops
from utils import find_start_dates, get_land_since, get_growth, get_mortality_recovery_rates

#%% Set Directories and Pathes"""
current_dir = os.getcwd()
working_dir = current_dir #os.path.join(current_dir, 'gdrive/My Drive/MyCOVID19/forecasting/')
dataset_dir = os.path.join(working_dir, 'COVID-19/csse_covid_19_data/csse_covid_19_time_series/')

print('current_dir: ', current_dir)
print('working_dir: ', working_dir)
print('dataset_dir: ', dataset_dir)

#%% Load Data
get_dataset = Get_DataSet(dataset_dir=dataset_dir)
global_confirmed_df, global_recovered_df, global_deceased_df = get_dataset.load_data()


#%% Some data stats
num_total_lands, num_total_days = global_confirmed_df.shape
print('num_total_lands: {}, num_total_days: {} '.format(num_total_lands, num_total_days))

#%%
num_tops = 20
top_indexes, sum_tops_df, tops_confirmed_df, tops_recovered_df, tops_deceased_df = GetTops().get(global_confirmed_df, global_recovered_df, global_deceased_df, num_tops)

# bar_plot(top_indexes, sum_tops_df)

# timeseries_plot(global_confirmed_df, 'Confirmed Cases')
# timeseries_plot(global_recovered_df, 'Recovered Cases')
# timeseries_plot(global_deceased_df, 'Deceased Cases')

start_dates, durations = find_start_dates(tops_confirmed_df)

# timeseries_plot_since(tops_confirmed_df, 'Confirmed', start_dates, durations)


delta_t = 1
tops_confirmed_growth_df = get_growth(df=tops_confirmed_df, delta_t=delta_t)
tops_recovered_growth_df = get_growth(df=tops_recovered_df, delta_t=delta_t)
tops_deceased_growth_df = get_growth(df=tops_deceased_df, delta_t=delta_t)

# growth_plot(tops_confirmed_growth_df, 'Confirmed', delta_t)
# growth_plot(tops_recovered_growth_df, 'Recovered', delta_t)
# growth_plot(tops_deceased_growth_df, 'Deseased', delta_t)


land = 'Iran'
land_since_df = get_land_since(tops_confirmed_df, tops_recovered_df, 
                               tops_deceased_df, start_dates, durations, land=land)

land_plot(land_since_df, land=land)

# for one country
mortality_rate, recovery_rate = get_mortality_recovery_rates(land_since_df)

rate_plot(mortality_rate, recovery_rate)

# for TopQ countries
# mortality_rate, recovery_rate = get_mortality_recovery_rates()
# rate_plot(mortality_rate, recovery_rate, land='TopQ')



