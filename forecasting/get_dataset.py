# -*- coding: utf-8 -*-
"""
Created on Tue Mar 24 21:16:12 2020

@author: rkako
"""
#%%
import os
import pandas as pd
import datetime 

#%%
class Get_DataSet(object):
    def __init__(self, dataset_dir):
        self.dataset_dir = dataset_dir
        
    def load_data(self):
        confirmed_path = os.path.join(self.dataset_dir, 'time_series_covid19_confirmed_global.csv')
        deceased_path = os.path.join(self.dataset_dir, 'time_series_covid19_deaths_global.csv')
        recovered_path = os.path.join(self.dataset_dir, 'time_series_covid19_recovered_global.csv')  
        
        confirmed_df = pd.read_csv(confirmed_path, index_col=False)
        recovered_df = pd.read_csv(recovered_path, index_col=False)
        deceased_df = pd.read_csv(deceased_path, index_col=False)
        
        confirmed_df.drop(columns=['Lat', 'Long', 'Province/State'], inplace=True)
        recovered_df.drop(columns=['Lat', 'Long', 'Province/State'], inplace=True)
        deceased_df.drop(columns=['Lat', 'Long', 'Province/State'], inplace=True)
        
        
        confirmed_df = confirmed_df.groupby(['Country/Region']).sum()
        recovered_df = recovered_df.groupby(['Country/Region']).sum()
        deceased_df = deceased_df.groupby(['Country/Region']).sum()
        
        # Land_confirmed = [country if str(state) == 'nan' else country+' '+str(state) for state, country in zip(confirmed_df['Province/State'], confirmed_df['Country/Region'])]
        # Land_recovered = [country if str(state) == 'nan' else country+' '+str(state) for state, country in zip(recovered_df['Province/State'], recovered_df['Country/Region'])]
        # Land_deceased = [country if str(state) == 'nan' else country+' '+str(state) for state, country in zip(deceased_df['Province/State'], deceased_df['Country/Region'])]

          
        # confirmed_df.index = Land_confirmed
        # recovered_df.index = Land_recovered
        # deceased_df.index = Land_deceased
        
        # confirmed_df.index.name = 'Land'
        # recovered_df.index.name = 'Land'
        # deceased_df.index.name = 'Land'
        
        return confirmed_df, recovered_df, deceased_df