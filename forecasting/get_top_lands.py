# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 00:18:01 2020

@author: rkako
"""
import pandas as pd

class GetTops:
    def __init__(self):
        pass
        
    def get(self, confirmed_df, recovered_df, deceased_df, num_tops):

        sum_confirmed_df = confirmed_df.iloc[:,-1]
        sum_recovered_df = recovered_df.iloc[:,-1]
        sum_deceased_df = deceased_df.iloc[:,-1]
        
        copy_sum_confirmed_df = sum_confirmed_df.copy()
        copy_sum_confirmed_df.sort_values(ascending=False, inplace=True)
        sum_tops_confirmed = copy_sum_confirmed_df.iloc[0:num_tops]
           
        sum_others_confirmed = copy_sum_confirmed_df.iloc[num_tops:]
        
        top_indexes = sum_tops_confirmed.index
        other_indexes = sum_others_confirmed.index
        
        sum_tops_recovered = sum_recovered_df.drop(other_indexes, axis=0)
        
        sum_tops_deceased = sum_deceased_df.drop(other_indexes, axis=0)
        
        sum_tops_df = pd.concat([sum_tops_confirmed, sum_tops_recovered, sum_tops_deceased], axis=1, sort=False)
        sum_tops_df.columns = ['Confirmed', 'Recovered', 'Deceased']
        
        tops_confirmed_df = confirmed_df.loc[top_indexes, :]
        tops_recovered_df = recovered_df.loc[top_indexes, :]
        tops_deceased_df = deceased_df.loc[top_indexes, :]
        
        
        return top_indexes, sum_tops_df, tops_confirmed_df, tops_recovered_df, tops_deceased_df