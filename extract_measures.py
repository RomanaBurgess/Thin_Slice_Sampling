#%% Thin slice sampling in parent-infant interactions.

# Input: This file takes datasets comprised of event logs (.xlsx) for parent and infant interactions, of 5 minute in length.
# Outputs: Frequencies - including mean counts, standard deviations and Pearson correlations - transitions matrices and associated stationary 
# distributions are calculated for each dyad, over the 15 distinct thin slices. These are saved as excel files.
# Note: whilst these files for used for both mother and father data, variables for both parents have been generalised as "mum" for consistency.

# Import packages
import os
import pandas as pd
import numpy as np
import datetime
import statistics as stats
from scipy.stats import pearsonr

# Import additional files
import coding_scheme as cs
import reformat as dat
import dataframes as datfr
import markov_func as mk

#%% Pre-define 15 thin slices
One   = [0, 60];      OneTwo    = [0, 120];     OneTwoThree   = [0, 180];    OneTwoThreeFour  = [0, 240]; OneTwoThreeFourFive = [0, 300]
Two   = [60, 120];    TwoThree  = [60, 180];    TwoThreeFour  = [60, 240];   TwoThreeFourFive = [60, 300]
Three = [120, 180];   ThreeFour = [120, 240];   ThreeFourFive = [120, 300]
Four  = [180, 240];   FourFive  = [180, 300]
Five  = [240, 300]

thin_slices      = [One, OneTwo, OneTwoThree, OneTwoThreeFour, OneTwoThreeFourFive, Two, TwoThree, TwoThreeFour, TwoThreeFourFive, Three, ThreeFour, 
                     ThreeFourFive, Four, FourFive, Five]
thin_slice_names = ["One", "OneTwo", "OneTwoThree", "OneTwoThreeFour", "OneTwoThreeFourFive", "Two", "TwoThree", "TwoThreeFour", "TwoThreeFourFive", 
                    "Three", "ThreeFour", "ThreeFourFive", "Four", "FourFive", "Five"]
  
# Array of data ID numbers, used to access .xlsx files (for confidentiality these have been anonymised)
IDs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Pre-define dataframes to store frequency/transition/stationary distribution data
var = []
for i in range(len(thin_sice_names)):
    time  = thin_slice_names[i]
    var.append((time + " Rate"))
         
big_mum = pd.DataFrame(index = cs.multi_ind, columns = var); big_inf = pd.DataFrame(index = cs.multi_ind, columns = var)
mum_all = datfr.mum_all; inf_all = datfr.inf_all
all_mum_stat = datfr.all_mum_stat; all_inf_stat = datfr.all_inf_stat

# Dataframe used to compound all interaction data
all_dat = pd.DataFrame() 

## Data Extraction
# Extract data features for each dyad, for each thin slice
for n in range(len(IDs)):
   
    # Load data
    dyad_ID = "Dyad" + str(IDs[n])
    data = pd.read_excel("./filepath" + str(IDs[n]) + ".xlsx")
      
    # Reformat data
    # Remove stop events, restructure durations, start times and end times
    # Split behaviours that overlap with minute (e.g. 1:00, 2:00)
    data = dat.format_data(data)  
    data = dat.split_data(data)      
    
    # Add dyadic data to large dataframe
    data["ID"] = dyad_ID
    all_dat = all_dat.append(data) 
    
    # Extract transitions and stationary distributions
    # Loop over behavioural group
    for i in range(len(cs.all_codes)):
        
        subcodes    = cs.all_codes[i]                               
        name        = cs.all_names[i]  
        
        # Subset data by subject
        dat_mum  = data[(data["Subject"] == "Caregiver 1")]  
        dat_inf  = data[(data["Subject"] == "Infant")]       

        # Subset data by code category 
        dat_mum  = dat_mum[(dat_mum["Behavior"].isin(subcodes))]  
        dat_inf  = dat_inf[(dat_inf["Behavior"].isin(subcodes))]  
        
        # Extract Transition Matrices
        # Mother
        mum_transitions = mk.MarkovTime(dat_mum, subcodes, thin_slices, thin_slice_names)
        mum_all.loc[(dyad_ID, list(mum_transitions.index)), list(mum_transitions.columns)] = mum_transitions.values
        
        # Infant
        inf_transitions = mk.MarkovTime(dat_inf, subcodes, thin_slices, thin_slice_names)
        inf_all.loc[(dyad_ID, list(inf_transitions.index)), list(inf_transitions.columns)] = inf_transitions.values
        
        # Extract Stationary Distributions
        for k in thin_slice_names:
          
            # Mother
            mt = mum_transitions.loc[:, (k, slice(None))]
            mt.columns = mt.columns.droplevel()
            
            # Infant
            it = inf_transitions.loc[:, (k, slice(None))]
            it.columns = it.columns.droplevel()
            
            mum_stat, mum_flag = mk.station(mt, dat_mum, subcodes)
            inf_stat, inf_flag = mk.station(it, dat_inf, subcodes)
        
            if mum_flag:
                all_mum_stat.loc[(dyad_ID, mum_stat.index), k] = mum_stat.values   
            if inf_flag:
                all_inf_stat.loc[(dyad_ID, inf_stat.index), k] = inf_stat.values
        
#%% Save Transitions and Stationary Distributions
mum_all.to_excel('./MUM_TRANS.xlsx')    
inf_all.to_excel('./INF_TRANS.xlsx')
all_mum_stat.to_excel('./MUM_STAT.xlsx') 
all_inf_stat.to_excel('./INF_STAT.xlsx') 

#%% Calculate frequencies
df = pd.DataFrame(index = cs.all_names; df = df.fillna((0))   # pre-define dataframe to store frequencies

# Subset data by subject - comment out each subject in turn and run analysis for each individually.
dat = all_dat[all_dat["Subject"] == "Caregiver 1"] 
dat = all_dat[all_dat["Subject"] == "Infant"]      

# Extract Frequencies by looping over each behavioural group
for i in range(len(cs.all_codes)):
    
    # Define behavioural group and associated subcodes
    subcodes = cs.all_codes[i]
    name = cs.all_names[i]
    
    a = pd.DataFrame(index = dat["ID"].unique()); a = a.fillna((0))
    All_Mean = pd.DataFrame(index = dat["ID"].unique(), columns = [("Mean")]); All_Mean = All_Mean.fillna((0))
    
    m = dat[dat["Behavior"].isin(subcodes)]
    m = m.groupby("ID").count()["Time_Relative_hms"] 
    All_Mean.loc[m.index, "Mean"] = m.values
        
    # Extract frequencies for each slice
    for j in range(len(thin_slices)):
        
        ts_name = thin_slice_names[j]
        start = thin_slices[j][0]; end = thin_slices[j][1]
    
        # Subset data by slice and subcodes
        dat = dat[dat["Behavior"].isin(subcodes)]
        dat = dat[dat["Time_Relative_sf"] >= start]
        dat = dat[dat["Time_Relative_sf"] < end]
        
        # Count behaviour instances and store in dataframe
        tm = dat.groupby("ID").count()["Time_Relative_hms"] 
        a.loc[tm.index, "Count " + ts_name] = tm
        
    a = a.fillna((0))
    
    # Averge frequencies by slice length 
    # Store means and standard deviations in large dataframe
    dict = {"Ones Mean (SD)": ["Count One", "Count Two", "Count Three", "Count Four", "Count Five"], 
            "Twos Mean (SD)": ["Count OneTwo", "Count TwoThree", "Count ThreeFour", "Count FourFive"],
            "Threes mean (SD)": ["Count OneTwoThree", "Count TwoThreeFour", "Count ThreeFourFive"],
             "Fours mean (SD)": ["Count OneTwoThreeFour", "Count TwoThreeFourFive"],
             "Fives mean (SD)": ["Count OneTwoThreeFourFive"]}
    
    for n in list(dict):
      thin_slice = a[dict[n]].values
      df.loc[name,  n] = str(np.round(thin_slice.mean(), 2)) + " (" + str(np.round(np.std(thin_slice), 2)) + ")"
                  
    # Save mean frequency and standard deviation for each behaviour over each thin slice
    # Save Pearson Correlations between each thin slice and full-session pairing              
    for j in range(len(thin_slices)):
        
        thin_slice = a["Count " + timeframe_names[j]]
        
        df.loc[name, thin_slice_names[j] + " mean"] = thin_slice.mean()        # Save mean frequency for specified slice
        df.loc[name, thin_slice_names[j] + " (SD)"] = np.std(thin_slice)       # Save standard deviation of frequencies for specified slice
    
        df.loc[name, thin_slice_names[j] + " r"] = np.round(pearsonr(thin_slice, All_Mean["Mean"])[0], 2)        # Save Pearson correlation for specified slice
        df.loc[name, thin_slice_names[j] + " p val"] = np.round(pearsonr(thin_slice, All_Mean["Mean"])[1], 2)    # Save associated p-value for specified slice

# Remove entries for behaviours that didn't occur 
df = df.fillna((0)); df = df[df.sum(axis=1) != 0]
      
# Save frequency data and correlations
df.to_excel('./MUM_FREQUENCIES.xlsx') 
df.to_excel('./INF_FREQUENCIES.xlsx') 
            
