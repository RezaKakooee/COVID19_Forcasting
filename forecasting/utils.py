# -*- coding: utf-8 -*-
"""
Created on Sat Mar 28 03:34:01 2020

@author: rkako
"""
import numpy as np
import pandas as pd
from pandas_profiling import ProfileReport

if pd_profiler:
  profile_confirmed = ProfileReport(global_confirmed_df)
  profile_recovered = ProfileReport(global_recovered_df)
  profile_deceased = ProfileReport(global_deceased_df)
  profile_confirmed.to_file(outputfile=os.path.join(working_dir, "Profiling for Global Confirmed Cases.html"))
  profile_recovered.to_file(outputfile=os.path.join(working_dir, "Profiling for Global Recovered Cases.html"))
  profile_deceased.to_file(outputfile=os.path.join(working_dir, "Profiling for Global Deceased Cases.html"))



def get_land_since(tops_confirmed_df, tops_recovered_df, 
                   tops_deceased_df, start_dates, durations, land='Iran', delta_t):
    
  land_confirmed_since_df = tops_confirmed_df.loc[land,:].loc[start_dates[land]:]
  land_recovered_since_df = tops_recovered_df.loc[land,:].loc[start_dates[land]:]
  land_deceased_since_df = tops_deceased_df.loc[land,:].loc[start_dates[land]:]
  
  date_cols = tops_confirmed_df.loc[:, start_dates[land]:].columns
  num_days = durations[land]+1
  growth_list_C = []
  growth_list_R = []
  growth_list_D = []
  for i in range(0, num_days-delta_t, delta_t):
    growth_list_C.append(land_confirmed_since_df[date_cols[i+delta_t]] - land_confirmed_since_df[date_cols[i]])
    growth_list_R.append(land_recovered_since_df[date_cols[i+delta_t]] - land_recovered_since_df[date_cols[i]])
    growth_list_D.append(land_deceased_since_df[date_cols[i+delta_t]] -  land_deceased_since_df[date_cols[i]])
  
  begining_gap_growth = len(growth_list_C)
  list_temp = list(np.zeros(num_days-begining_gap_growth))
  
  growth_list_C = np.insert(np.array(growth_list_C), 0, list_temp)
  growth_list_R = np.insert(np.array(growth_list_R), 0, list_temp)
  growth_list_D = np.insert(np.array(growth_list_D), 0, list_temp)
 
  
  land_since_df = pd.DataFrame({'Confirmed': land_confirmed_since_df.values,
                                'Recovered': land_recovered_since_df.values,
                                'Deceased': land_deceased_since_df.values,
                                'Confirmed Growth': growth_list_C,
                                'Recovered Growth': growth_list_R,
                                'Deceased Growth': growth_list_D,}, 
                                 index = np.arange(num_days))
  
  return land_since_df

def find_start_dates(confirmed):
  # very_start_date = confirmed.columns[0]
  very_end_date = confirmed.columns[-1]
  lands = confirmed.index
  start_dates = {}
  for land in lands:
    df1 = confirmed.loc[confirmed.index==land].iloc[0,1:]!=0
    start_dates.update({land: df1.index[df1==True].tolist()[0]})

  durations = {}
  for key in start_dates.keys():
      sd = start_dates[key]
      d1 = datetime.strptime(sd, '%m/%d/%y').date()
      d2 = datetime.strptime(very_end_date, '%m/%d/%y').date()
      delta = d2 - d1
      durations.update({key: delta.days})
      
  return start_dates, durations

def get_growth(df, delta_t=1):
  land_names=df.index
  date_cols = df.columns
  num_days= len(date_cols)

  growth_list = []
  for i in range(0, num_days-delta_t, delta_t):
    growth_list.append(df[date_cols[i+delta_t]].values - df[date_cols[i]].values)
  growth_arr = np.array(growth_list)

  new_date_cols = [date_cols[0]+'-'+date_cols[i] for i in range(1, num_days-delta_t, delta_t)]
  growth_df = pd.DataFrame(columns=new_date_cols, index=land_names)

  for i, ncol in enumerate(new_date_cols):
    growth_df[ncol] = growth_arr[i,:]
  # speed_df.insert(0, 'Land', land_names.values)

  return growth_df


def get_mortality_recovery_rates(confirmed1, deceased1, recovered1):
  mortality_rate = pd.DataFrame(deceased1.iloc[:,1:].values / confirmed1.iloc[:,1:].values, columns=confirmed1.columns[1:])
  recovery_rate = pd.DataFrame(recovered1.iloc[:,1:].values / confirmed1.iloc[:,1:].values , columns=confirmed1.columns[1:])

  return mortality_rate, recovery_rate