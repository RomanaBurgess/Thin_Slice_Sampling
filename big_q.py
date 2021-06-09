#%% How long do we need to code?

# This file takes datasets comprised of event logs for parents and infants,
# categorising 5 minute interactions. The file takes 3 potential datasets as inputs 
# (cardiff mums, bristol mums, bristol dads). Transitions between
# behaviours within coding categories and resulting stationary distributions are 
# calculated for each dyad over 14 different timeframes. Chi squared tests are 
# then performed to evaluate if there are statistically significant differences
# between transitions and stationary distributions at different timeframes
# compared to those gathered from all available data.

#%% Import packages and files

import os
os.chdir("C:\\Users\\az19326\\OneDrive - University of Bristol\\Documents\\Second year\\October 2020\\Python")

import pandas as pd
import numpy as np
import coding_scheme as cs
import reformat as dat
import dataframes as datfr
import datetime
import markov_func as mk
import statistics as stats

#%% Predefine timeframe variables

One   = [0, 60];      OneTwo    = [0, 120];     OneTwoThree   = [0, 180];    OneTwoThreeFour  = [0, 240]; OneTwoThreeFourFive = [0, 300]
Two   = [60, 120];    TwoThree  = [60, 180];    TwoThreeFour  = [60, 240];   TwoThreeFourFive = [60, 300]
Three = [120, 180];   ThreeFour = [120, 240];   ThreeFourFive = [120, 300]
Four  = [180, 240];   FourFive  = [180, 300]
Five  = [240, 300]

timeframes = [One, OneTwo, OneTwoThree, OneTwoThreeFour, OneTwoThreeFourFive,
Two, TwoThree, TwoThreeFour, TwoThreeFourFive, Three, ThreeFour, ThreeFourFive, Four, FourFive, Five]
  
timeframe_names = ["One", "OneTwo", "OneTwoThree", "OneTwoThreeFour", "OneTwoThreeFourFive",
"Two", "TwoThree", "TwoThreeFour", "TwoThreeFourFive", "Three", "ThreeFour", "ThreeFourFive", "Four", "FourFive", "Five"]
  
#%% Predefine transition and stationary dataframes
# Comment out dataframes not in use

cardiff = [23, 21, 26, 29, 33, 87, 34, 63, 47, 48, 162, 185, 163, 190, 194, 195, 197, 199, 200, 204, 59, 74, 105, 106, 111, 121, 129, 141, 146, 154, 159]

# bris mum
# cardiff = ["278140497A_Feeding_AC", "278123519B_Stacking_IC", "278120336B_Stacking_IC",
# "278119436A_Feeding_AC", "278115240A_feeding_RP_IC", "278108945A_Stacking1_IC",
# "278107409A_feeding_EI_IC", "278107307A_feeding_RP_IC", "278105342B_Stacking_IC",
# "278105342B_Feeding_AC_IC", "278103911A_Feeding_AC_IC", "278102804A_Feeding_AC",
# "278102511A_Feeding_AC", "278101837A_Feeding_AC", "278100320A_Feeding_EI"]

# # # bris dad
cardiff = ["278100311C_feeding_MR", "278109414A_feeding_MR","278120342A_reading_MR",
"278120342A_stacking_MR", "278127953A_feeding1_MR", "278127953A_feeding2_PC",
"278127953A_feeding3_PC", "278127953A_stacking_MR", "278128402B_stacking_PC",
"278128402B_stacking+feeding_MR", "278130718B_feeding_JS", "278147230A_bedtime_MR",
"278147230A_feeding_JS", "278147248A_P_freeplay+book_LM", "278147397A_feeding_MR",
"278147585A_feeding_MR", "2781472555A_feeding_LM"]

var = []
for i in range(len(timeframe_names)):
    time  = timeframe_names[i]
    var.append((time + " Rate"))
       
# Cardiff dataframes    
big_mum = pd.DataFrame(index = cs.multi_ind_cardiff, columns = var)
big_inf = pd.DataFrame(index = cs.multi_ind_cardiff, columns = var)
mum_all = datfr.mum_all
inf_all = datfr.inf_all
all_mum_stat = datfr.all_mum_stat
all_inf_stat = datfr.all_inf_stat

# # Bristol mum dataframes
# big_mum = pd.DataFrame(index = cs.multi_ind_brism, columns = var)
# big_inf = pd.DataFrame(index = cs.multi_ind_brism, columns = var)
# mum_all = datfr.mum_all_brism
# inf_all = datfr.inf_all_brism
# all_mum_stat = datfr.all_mum_stat_brism
# all_inf_stat = datfr.all_inf_stat_brism

# Bristol dad dataframes
big_mum = pd.DataFrame(index = cs.multi_ind_brisd, columns = var)
big_inf = pd.DataFrame(index = cs.multi_ind_brisd, columns = var)
mum_all = datfr.mum_all_brisd
inf_all = datfr.inf_all_brisd
all_mum_stat = datfr.all_mum_stat_brisd
all_inf_stat = datfr.all_inf_stat_brisd

all_dat = pd.DataFrame() 

#%% Extract data features by timeframe

for n in range(len(cardiff)):
    
    print(n+1)
    # Choose which datasets to extract
    
    # Cardiff mums
    os.chdir("C:\\Users\\az19326\\OneDrive - University of Bristol\\Documents\\Second year\\October 2020\\Python")
    cardiff_ID = "Cardiff" + str(cardiff[n])
    data = pd.read_excel("./Cardiff/Cardiff" + str(cardiff[n]) + ".xlsx")
      
    # # Bristol mums
    # os.chdir("//ads.bris.ac.uk/folders/Health Sciences/SSCM ALSPAC/Studies/T23POC_Focus_on_COCO_90s/Raw data/B2564_Pearson/B3646_Romana/Data/Bristol Mums")
    # cardiff_ID = cardiff[n]
    # data = pd.read_excel(str(cardiff[n]) + ".xlsx")
    
    # Bristol dads
    # os.chdir("//ads.bris.ac.uk/folders/Health Sciences/SSCM ALSPAC/Studies/T23POC_Focus_on_COCO_90s/Raw data/B2564_Pearson/B3646_Romana/Data/Bristol Dads")
    # cardiff_ID = cardiff[n]
    # data = pd.read_excel(str(cardiff[n]) + ".xlsx")
    
    os.chdir("C:\\Users\\az19326\\OneDrive - University of Bristol\\Documents\\Second year\\October 2020\\Python")
    
    # Reformat data
    # Remove stop events, restructure durations, start times and end times
    # Split behaviours that overlap with minute (e.g. 1:00, 2:00)
    data = dat.format_data(data)  
    data = dat.split_data(data)      
    
    data["ID"] = cardiff_ID
    all_dat = all_dat.append(data) 
    
    # Extract transitions and stationary distributions
    for i in range(len(cs.all_codes)):
        
        subcodes    = cs.all_codes[i]                               
        name        = cs.all_names[i]  
        
        # Subset data by subject
        dat_mum  = data[(data["Subject"] == "Caregiver 1")]  
        dat_inf  = data[(data["Subject"] == "Infant")]       

        # Subset data by code category 
        dat_mum  = dat_mum[(dat_mum["Behavior"].isin(subcodes))]  
        dat_inf  = dat_inf[(dat_inf["Behavior"].isin(subcodes))]  
        
        print(name)
        
        # Extract Transition Matrices
        inf_transitions = mk.MarkovTime(dat_inf, subcodes, timeframes, timeframe_names)
        mum_transitions = mk.MarkovTime(dat_mum, subcodes, timeframes, timeframe_names)
        
        mum_all.loc[(cardiff_ID, list(mum_transitions.index)), list(mum_transitions.columns)] = mum_transitions.values
        inf_all.loc[(cardiff_ID, list(inf_transitions.index)), list(inf_transitions.columns)] = inf_transitions.values
        
        print("Transitions done")
        
        # Extract Stationary Distributions
        for k in timeframe_names:
            
            mt = mum_transitions.loc[:, (k, slice(None))]
            mt.columns = mt.columns.droplevel()
            
            it = inf_transitions.loc[:, (k, slice(None))]
            it.columns = it.columns.droplevel()
            
            mum_stat, mum_flag = mk.station(mt, dat_mum, subcodes)
            inf_stat, inf_flag = mk.station(it, dat_inf, subcodes)
        
            if mum_flag:
                all_mum_stat.loc[(cardiff_ID, mum_stat.index), k] = mum_stat.values   
                
            if inf_flag:
                all_inf_stat.loc[(cardiff_ID, inf_stat.index), k] = inf_stat.values
          
        print("Stationary done") 
        
#%% Save 
       
#os.chdir("C:\\Users\\az19326\\OneDrive - University of Bristol\\Documents\\Second year\\October 2020\\Python\\Cardiff\Statistics\how_many_codes")
#os.chdir("//ads.bris.ac.uk/folders/Health Sciences/SSCM ALSPAC/Studies/T23POC_Focus_on_COCO_90s/Raw data/B2564_Pearson/B3646_Romana/Python/Bristol Mums")
# os.chdir("//ads.bris.ac.uk/folders/Health Sciences/SSCM ALSPAC/Studies/T23POC_Focus_on_COCO_90s/Raw data/B2564_Pearson/B3646_Romana/Python/Bristol Dads")

# mum_all.to_excel('./MUM_TRANS2.xlsx')    
# print(1)
# inf_all.to_excel('./INF_TRANS2.xlsx')
# print(2)
# all_mum_stat.to_excel('./MUM_STAT2.xlsx') 
# print(3)
# all_inf_stat.to_excel('./INF_STAT2.xlsx') 

#%% Count analysis - correlations
from scipy.stats import pearsonr

df_m = pd.DataFrame(index = cs.all_names)   # predefine dataframe
df_m = df_m.fillna((0))

dat = all_dat[all_dat["Subject"] == "Caregiver 1"] # subset mother data
dat = all_dat[all_dat["Subject"] == "Infant"]      # subset infant data

for i in range(len(cs.all_codes)):
    
    subcodes = cs.all_codes[i]
    name = cs.all_names[i]
    
    a = pd.DataFrame(index = dat["ID"].unique()); a = a.fillna((0))
    All_Mean = pd.DataFrame(index = dat["ID"].unique(), columns = [("Mean")]); All_Mean = All_Mean.fillna((0))
    
    m_d = dat[dat["Behavior"].isin(subcodes)]
    m_d = m_d.groupby("ID").count()["Time_Relative_hms"] 
    All_Mean.loc[m_d.index, "Mean"] = m_d.values
        
    for j in range(len(timeframes)):
        
        tf_name = timeframe_names[j]
        start = timeframes[j][0]; end = timeframes[j][1]
    
        m_dat = dat[dat["Behavior"].isin(subcodes)]
        m_dat = m_dat[m_dat["Time_Relative_sf"] >= start]
        m_dat = m_dat[m_dat["Time_Relative_sf"] < end]
        
        mum_tm = m_dat.groupby("ID").count()["Time_Relative_hms"] 
        a.loc[mum_tm.index, "Count " + tf_name] = mum_tm
        
    a = a.fillna((0))
    
    # Save counts averged by slice length
    # Ones
    thin_slice = a[["Count One", "Count Two", "Count Three", "Count Four", "Count Five"]].values
    df_m.loc[name,  "Ones mean (SD)"] = str(np.round(thin_slice.mean(), 2)) + " (" + str(np.round(np.std(thin_slice), 2)) + ")"
    
    # Twos
    thin_slice = a[["Count OneTwo", "Count TwoThree", "Count ThreeFour", "Count FourFive"]].values
    df_m.loc[name,  "Twos mean (SD)"] = str(np.round(thin_slice.mean(), 2)) + " (" + str(np.round(np.std(thin_slice), 2)) + ")"
    
    # Threes
    thin_slice = a[["Count OneTwoThree", "Count TwoThreeFour", "Count ThreeFourFive"]].values
    df_m.loc[name,  "Threes mean (SD)"] = str(np.round(thin_slice.mean(), 2)) + " (" + str(np.round(np.std(thin_slice), 2)) + ")"

    # Fours
    thin_slice = a[["Count OneTwoThreeFour", "Count TwoThreeFourFive"]].values
    df_m.loc[name,  "Fours mean (SD)"] = str(np.round(thin_slice.mean(), 2)) + " (" + str(np.round(np.std(thin_slice), 2)) + ")"

    # Fives
    thin_slice = a[["Count OneTwoThreeFourFive"]].values
    df_m.loc[name,  "Fives mean (SD)"] = str(np.round(thin_slice.mean(), 2)) + " (" + str(np.round(np.std(thin_slice), 2)) + ")"


    # save correlations
    for j in range(len(timeframes)):
        
        thin_slice = a["Count " + timeframe_names[j]]
        
        df_m.loc[name, timeframe_names[j] + " mean"] = thin_slice.mean()
        df_m.loc[name, timeframe_names[j] + " SD"] = np.std(thin_slice)
    
        df_m.loc[name, timeframe_names[j] + " r"] = np.round(pearsonr(thin_slice, All_Mean["Mean"])[0], 2) 
        df_m.loc[name, timeframe_names[j] + " p val"] = np.round(pearsonr(thin_slice, All_Mean["Mean"])[1], 2)

df_m = df_m.fillna((0))
df_m = df_m[df_m.sum(axis=1) != 0]

#%% Transition Analysis and Plots

# Load transition dataframes
# Cardiff
# os.chdir("C:\\Users\\az19326\\OneDrive - University of Bristol\\Documents\\Second year\\October 2020\\Python\\Cardiff\Statistics\how_many_codes")
# mum_trans = pd.read_excel("./MUM_TRANS2.xlsx", index_col=[0,1], header=[0,1])
# print(1)
#inf_trans = pd.read_excel("./INF_TRANS2.xlsx", index_col=[0,1], header=[0,1])

# Bristol Mums
# os.chdir("//ads.bris.ac.uk/folders/Health Sciences/SSCM ALSPAC/Studies/T23POC_Focus_on_COCO_90s/Raw data/B2564_Pearson/B3646_Romana/Python/Bristol Mums")
# mum_trans = pd.read_excel("./MUM_TRANS2.xlsx",index_col=[0,1], header=[0,1])
# inf_trans = pd.read_excel("./INF_TRANS2.xlsx",index_col=[0,1], header=[0,1])

# Bristol Dads
os.chdir("//ads.bris.ac.uk/folders/Health Sciences/SSCM ALSPAC/Studies/T23POC_Focus_on_COCO_90s/Raw data/B2564_Pearson/B3646_Romana/Python/Bristol Dads")
mum_trans = pd.read_excel("./MUM_TRANS2.xlsx",index_col=[0,1], header=[0,1])
print(1)
inf_trans = pd.read_excel("./INF_TRANS2.xlsx",index_col=[0,1], header=[0,1])

# Label dataframe indices
mum_trans.index.set_names(["Cardiff ID", "Behaviour"], inplace = True)
inf_trans.index.set_names(["Cardiff ID", "Behaviour"], inplace = True)

mum_tr = pd.DataFrame(index = cs.multi_ind, columns = timeframe_names)
inf_tr = pd.DataFrame(index = cs.multi_ind, columns = timeframe_names)

for i in range(len(cs.all_codes)):
    
    # define subcodes
    subcodes = cs.all_codes[i]
    
    # true transition matrices at subcodes
    true_mum = mum_trans.loc[(slice(None), subcodes), ("OneTwoThreeFourFive", subcodes)]
    true_inf = inf_trans.loc[(slice(None), subcodes), ("OneTwoThreeFourFive", subcodes)]
    
    true_mum[true_mum == 0] = np.nan
    true_inf[true_inf == 0] = np.nan
    
    for j in range(len(timeframe_names)):
    
        # define timeframe
        T = timeframe_names[j]
        
        # subset relevant matrices from dataframes
        mum_mat = mum_trans.loc[(slice(None), subcodes), (T, subcodes)]
        inf_mat = inf_trans.loc[(slice(None), subcodes), (T, subcodes)]       
        
        # define difference matrices (between transitions at T and true transitions)
        mum_diff = pd.DataFrame(abs(mum_mat.values - true_mum.values), index = mum_mat.index, columns = subcodes)
        inf_diff = pd.DataFrame(abs(inf_mat.values - true_inf.values), index = inf_mat.index, columns = subcodes)   
        
        # 
        mum_diff = mum_diff.groupby(level = "Behaviour").mean()
        inf_diff = inf_diff.groupby(level = "Behaviour").mean()
               
        #    
        mum_tr.loc[(cs.all_names[i], subcodes), T] = mum_diff.mean(axis=1).values      
        inf_tr.loc[(cs.all_names[i], subcodes), T] = inf_diff.mean(axis=1).values     

# Reorder columns for aesthetics
Mum_Tr = mum_tr.reindex(columns= ["One", "Two", "Three", "Four", "Five", "OneTwo", 
                 "TwoThree", "ThreeFour", "FourFive", "OneTwoThree", "TwoThreeFour", 
                 "ThreeFourFive", "OneTwoThreeFour", "TwoThreeFourFive"])

Inf_Tr = inf_tr.reindex(columns= ["One", "Two", "Three", "Four", "Five", "OneTwo", 
                 "TwoThree", "ThreeFour", "FourFive", "OneTwoThree", "TwoThreeFour", 
                 "ThreeFourFive", "OneTwoThreeFour", "TwoThreeFourFive"])

# Set index names
Mum_Tr.index.set_names(["Code", "Behaviour"], inplace = True)
Inf_Tr.index.set_names(["Code", "Behaviour"], inplace = True)

# Remove codes from analysis with not enough occurrences
remove_codes = [cs.audio, cs.view, cs.alertness_state, cs.encouragement, cs.agitation_soothing, cs.role_reversal,
               cs.physical_imitation, cs.acknowledgment, cs.eating, cs.rough_and_tumble, 
               cs.caregiver_unusual_behaviours, cs.infant_unusual_behaviours]

for i in range(len(remove_codes)):
    codes = remove_codes[i]
    Mum_Tr = Mum_Tr[~Mum_Tr.index.get_level_values("Behaviour").isin(codes)]
    Inf_Tr = Inf_Tr[~Inf_Tr.index.get_level_values("Behaviour").isin(codes)]
    
# Plot difference box plots
Mum_Tr.plot(kind="box", vert = False, figsize = [8,8], xlim = [-0.02, 1.02], fontsize = 13, title = "Mother distribution of differences of transition matrices from true transition matrices")
Inf_Tr.plot(kind="box", vert = False, figsize = [8,8], xlim = [-0.02, 1.02], fontsize = 13, title = "Infant distribution of differences of transition matrices from true transition matrices")
 
Mum_Tr = Mum_Tr.dropna(axis=0, how = "all")
Inf_Tr = Inf_Tr.dropna(axis=0, how = "all")

from matplotlib.cbook import boxplot_stats

# Extract Means for Write Up
mum_stats = boxplot_stats(Mum_Tr.values)
inf_stats = boxplot_stats(Inf_Tr.values)

#%% Stationary Distribution Analysis and Plots

# Load stationary distribution dataframes
# Cardiff
# os.chdir("C:\\Users\\az19326\\OneDrive - University of Bristol\\Documents\\Second year\\October 2020\\Python")
# mum_stats = pd.read_excel("./Cardiff/Statistics/how_many_codes/MUM_STAT2.xlsx", index_col=[0, 1])
# inf_stats = pd.read_excel("./Cardiff/Statistics/how_many_codes/INF_STAT2.xlsx", index_col=[0, 1])

# Bristol mums
# os.chdir("//ads.bris.ac.uk/folders/Health Sciences/SSCM ALSPAC/Studies/T23POC_Focus_on_COCO_90s/Raw data/B2564_Pearson/B3646_Romana/Python/Bristol Mums")
# mum_stats = pd.read_excel("./MUM_STAT2.xlsx",index_col=[0,1])
# inf_stats = pd.read_excel("./INF_STAT2.xlsx",index_col=[0,1])

# Bristol dads
os.chdir("//ads.bris.ac.uk/folders/Health Sciences/SSCM ALSPAC/Studies/T23POC_Focus_on_COCO_90s/Raw data/B2564_Pearson/B3646_Romana/Python/Bristol Dads")
mum_stats = pd.read_excel("./MUM_STAT2.xlsx",index_col=[0,1])
inf_stats = pd.read_excel("./INF_STAT2.xlsx",index_col=[0,1])

# Label dataframe indices
mum_stats.index.set_names(["Cardiff ID", "Behaviour"], inplace = True)
inf_stats.index.set_names(["Cardiff ID", "Behaviour"], inplace = True)

# Predefine dataframes to save % agreements
mum_st  = pd.DataFrame(columns = timeframe_names, index = cs.multi_ind)
inf_st  = pd.DataFrame(columns = timeframe_names, index = cs.multi_ind)

# Look for significant differences between stationary distributions at timeframe T 
# and "true" stationary distributions

for i in range(len(cs.all_codes)):
    
    # define subcodes
    subcodes = cs.all_codes[i]
    
    for j in range(len(timeframe_names)):
    
        # define timeframe
        T = timeframe_names[j]
        
        true_mum = mum_stats.loc[(slice(None), subcodes), ("OneTwoThreeFourFive")]
        true_inf = inf_stats.loc[(slice(None), subcodes), ("OneTwoThreeFourFive")]
        
         # subset relevant matrices from dataframes
        mum_mat = mum_stats.loc[(slice(None), subcodes), (T)]
        inf_mat = inf_stats.loc[(slice(None), subcodes), (T)]
        
        # define difference matrices (between SDs at T and true SD)
        mum_stat_diff = pd.DataFrame(abs(mum_mat.values - true_mum.values), index = mum_mat.index)
        inf_stat_diff = pd.DataFrame(abs(inf_mat.values - true_inf.values), index = inf_mat.index)

        # find indices of values less than tolerance
        mum_stat_diff = mum_stat_diff.groupby(level = "Behaviour").mean()
        inf_stat_diff = inf_stat_diff.groupby(level = "Behaviour").mean()
        
        # save the % of datasets with diff less than tolerance
        # mother
        if len(mum_stat_diff) != 0:          
            mum_st.loc[(slice(None), subcodes), T] = mum_stat_diff.values         
        else:
            mum_st.loc[(slice(None), subcodes), T] = 0  
           
        # infant    
        if len(inf_stat_diff) != 0:          
            inf_st.loc[(slice(None), subcodes), T] = inf_stat_diff.values         
        else:
            inf_st.loc[(slice(None), subcodes), T] = 0  
   
mum_st = mum_st[mum_st != 0]; inf_st = inf_st[inf_st != 0]

Mum_St = mum_st.reindex(columns= ["One", "Two", "Three", "Four", "Five", "OneTwo", 
                 "TwoThree", "ThreeFour", "FourFive", "OneTwoThree", "TwoThreeFour", 
                 "ThreeFourFive", "OneTwoThreeFour", "TwoThreeFourFive"])

Inf_St = inf_st.reindex(columns= ["One", "Two", "Three", "Four", "Five", "OneTwo", 
                 "TwoThree", "ThreeFour", "FourFive", "OneTwoThree", "TwoThreeFour", 
                 "ThreeFourFive", "OneTwoThreeFour", "TwoThreeFourFive"])

# Remove codes from analysis with not enough occurrences
remove_codes = [cs.view, cs.alertness_state, cs.encouragement, cs.agitation_soothing, cs.role_reversal,
               cs.physical_imitation, cs.acknowledgment, cs.eating, cs.rough_and_tumble, 
               cs.caregiver_unusual_behaviours, cs.infant_unusual_behaviours]

Mum_St.index.set_names(["Behaviour", "Code"], inplace = True)
Inf_St.index.set_names(["Behaviour", "Code"], inplace = True)

for i in range(len(remove_codes)):
    codes = remove_codes[i]
    Mum_St = Mum_St[~Mum_St.index.get_level_values("Code").isin(codes)]
    Inf_St = Inf_St[~Inf_St.index.get_level_values("Code").isin(codes)]

# Plot Absolute differences
Mum_St.plot(kind="box", vert = False, figsize = [8,8], xlim = [-0.02, 0.42], fontsize = 13, title = "Mother distribution of differences of stationary distributions from true stationary distributions")
Inf_St.plot(kind="box", vert = False, figsize = [8,8], xlim = [-0.02, 0.42], fontsize = 13, title = "Infant distribution of differences of stationary distributions from true stationary distributions")

Mum_St = Mum_St.dropna(axis=0, how = "all")
Inf_St = Inf_St.dropna(axis=0, how = "all")

from matplotlib.cbook import boxplot_stats

# Extract Means for Write Up
mum_stats = boxplot_stats(Mum_St.values)
inf_stats = boxplot_stats(Inf_St.values)

#%% Chi Squared test
# For Transition matrices

# Load transition dataframes
# Cardiff
#os.chdir("C:\\Users\\az19326\\OneDrive - University of Bristol\\Documents\\Second year\\October 2020\\Python\\Cardiff\Statistics\how_many_codes")
#mum_trans = pd.read_excel("./MUM_TRANS_RAW2.xlsx", index_col=[0,1], header=[0,1])
#inf_trans = pd.read_excel("./INF_TRANS_RAW2.xlsx", index_col=[0,1], header=[0,1])

# Bristol Mums
# os.chdir("//ads.bris.ac.uk/folders/Health Sciences/SSCM ALSPAC/Studies/T23POC_Focus_on_COCO_90s/Raw data/B2564_Pearson/B3646_Romana/Python/Bristol Mums")
# mum_trans = pd.read_excel("./MUM_TRANS_RAW2.xlsx",index_col=[0,1], header=[0,1])
# inf_trans = pd.read_excel("./INF_TRANS_RAW2.xlsx",index_col=[0,1], header=[0,1])

# Bristol Dads
# os.chdir("//ads.bris.ac.uk/folders/Health Sciences/SSCM ALSPAC/Studies/T23POC_Focus_on_COCO_90s/Raw data/B2564_Pearson/B3646_Romana/Python/Bristol Dads")
# mum_trans = pd.read_excel("./MUM_TRANS_RAW2.xlsx",index_col=[0,1], header=[0,1])
# print(1)
# inf_trans = pd.read_excel("./INF_TRANS_RAW2.xlsx",index_col=[0,1], header=[0,1])

# Label dataframe indices
mum_trans.index.set_names(["Cardiff ID", "Behaviour"], inplace = True)
inf_trans.index.set_names(["Cardiff ID", "Behaviour"], inplace = True)

from scipy.stats.distributions import chi2

TFN = timeframe_names.copy(); TF  = timeframes.copy(); del TF[4]; del TFN[4]

# Predefine dataframes to save X2 values
X2 = pd.DataFrame(index = inf_trans.index.get_level_values("Behaviour").unique(), columns = TFN)

for t in range(len(TFN)):
    
    timeframe = TFN[t]
    T         = TF[t]
    
    for n in range(len(cs.all_codes)):
        
        code = cs.all_names[n]
        subcodes = cs.all_codes[n]
        
        # full-session transition matrix P
        P = inf_trans.loc[(slice(None), subcodes), ("OneTwoThreeFourFive", subcodes)] 
        P.index.set_names(["Cardiff ID", "Behaviour"], inplace = True)
        P = P.loc[(P.sum(axis=1) != 0)]           
        P   = P.groupby(level = "Behaviour").mean()
        p_ind    = P.index.get_level_values("Behaviour")
        P = P.loc[p_ind, (slice(None), p_ind)]
        
        if len(p_ind) != 0:
            
            # thin slice transition matrix Q
            Q = pd.DataFrame(0, index = p_ind, columns = p_ind)
            Q_temp = inf_trans.loc[(slice(None), p_ind), (timeframe, p_ind)]    
            Q_temp = Q_temp.loc[(Q_temp.sum(axis=1) != 0)]
            Q_temp.index.set_names(["Cardiff ID", "Behaviour"], inplace = True)  
            Q_temp = Q_temp.groupby(level = "Behaviour").mean()
            Q.loc[Q_temp.index, Q_temp.columns.droplevel(0)] = Q_temp.values
            
            P.columns = P.columns.droplevel(0)
            Q = Q.loc[:, P.columns]
            
            # save X2 values                
            for i in range(len(p_ind)):
                
                p = P.loc[p_ind[i], :].values
                q = Q.loc[p_ind[i], :].values
    
                # Extract x2 value
                xi = ((q - p)**2)/(p)
                xi[~np.isfinite(xi)] = 0
                
                # Extract associated p-val
                p_val = chi2.sf(np.nansum(xi), len(p_ind)-1)
                
                # Save correctly formatted in Table for Write up
                if (p_val <= 0.05) & (p_val > 0.005):
                    X2.loc[p_ind[i], timeframe] = str(np.round(np.nansum(xi), 2)) + "*" 
                    
                elif (p_val <= 0.005) & (p_val > 0.001):
                    X2.loc[p_ind[i], timeframe] = str(np.round(np.nansum(xi), 2)) + "**" 
                    
                elif p_val <= 0.001:
                    X2.loc[p_ind[i], timeframe] = str(np.round(np.nansum(xi), 2)) + "***" 
                    
                else:
                    X2.loc[p_ind[i], timeframe] = str(np.round(np.nansum(xi), 2))
                                 
#%% Chi squared - stationary distributions

X2_stat = pd.DataFrame(index = cs.all_names, columns = TFN)

for t in range(len(TFN)):
    
    timeframe = TFN[t]
    T         = TF[t]
       
    for n in range(len(cs.all_codes)):
        
        subcodes    = cs.all_codes[n] 
        name        = cs.all_names[n]                           
        dat         = all_dat[all_dat["Subject"] == "Caregiver 1"]
        dat         = dat[dat["Behavior"].isin(subcodes)]
        
        # subset timeframe
        dat = dat[dat["Time_Relative_hms"] < datetime.time(minute = int(T[1]/60))]
        dat = dat[dat["Time_Relative_hms"] >= datetime.time(minute = int(T[0]/60))]
        
        if len(dat) != 0:
            
            # true stationary distribution P
            P = mum_stats.loc[(slice(None), subcodes), "OneTwoThreeFourFive"]  
            P.index.set_names(["Cardiff ID", "Behaviour"], inplace = True)
            P     = P[(P != 0)]
            P_sum = P.groupby(level = "Behaviour").sum().sum() # number of subjects
            P     = P.groupby(level = "Behaviour").apply(lambda x: x.sum()/P_sum)   
                           
            subcodes = P.index
            
            # average stationary distribution Q
            Q      = pd.Series(0, index = subcodes)
            Q_temp = mum_stats.loc[(slice(None), subcodes), timeframe]     
            Q_temp.index.set_names(["Cardiff ID", "Behaviour"], inplace = True) 
            
            Q_sum  = Q_temp.groupby(level = "Behaviour").sum().sum() # number of subjects
            Q_temp = Q_temp.groupby(level = "Behaviour").apply(lambda x: x.sum()/Q_sum)
            
            Q.loc[Q_temp.index] = Q_temp.values   
            Q                   = Q.loc[P.index]
                
            p = P.values*300
            q = Q.values*300
            
            # Chi squared
            xi = ((q - p)**2)/(p)
            xi[np.isnan(xi)] = 0    
            xi[~np.isfinite(xi)] = 0
                
            # Extract associated p-val
            p_val = chi2.sf(xi.sum(), len(p)-1)
            
            # Save correctly formatted in Table for Write up
            if (p_val <= 0.05) & (p_val > 0.005):
                X2_stat.loc[name, timeframe] = str(np.round(np.nansum(xi), 2)) + "*" 
                
            elif (p_val <= 0.005) & (p_val > 0.001):
                X2_stat.loc[name, timeframe] = str(np.round(np.nansum(xi), 2)) + "**" 
                
            elif (p_val <= 0.001):
                X2_stat.loc[name, timeframe] = str(np.round(np.nansum(xi), 2)) + "***" 
                
            else:
                X2_stat.loc[name, timeframe] = str(np.round(np.nansum(xi), 2))
            