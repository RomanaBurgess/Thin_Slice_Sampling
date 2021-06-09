import pandas as pd
import coding_scheme as cs

#%%
# Create general mother and infant dataframes
big_mum = pd.Series(dtype = "float64", index = cs.multi_ind)
big_mum = big_mum.to_frame(name = "Sum")            # convert pd.series to pd.dataframe
big_mum['Sum'] = ((0))                              # start as zeros
big_mum['Max duration'] = ((0))                     # add max and min duration
big_mum['Min duration'] = ((0))    
big_mum['Average'] = ((0))                          # average duration column
big_mum["Freq total"] = ((0))
big_mum['Rate per min'] = ((0))
big_mum['Min 1'] = ((0)); big_mum['Min 2'] = ((0)); big_mum['Min 3'] = ((0)); big_mum['Min 4'] = ((0)); big_mum['Min 5'] = ((0))


big_inf = pd.Series(dtype = "float64", index = cs.multi_ind)
big_inf = big_inf.to_frame(name = "Sum")            # convert pd.series to pd.dataframe
big_inf['Sum'] = ((0))                              # start as zeros
big_inf['Max duration'] = ((0))                     # add max and min duration
big_inf['Min duration'] = ((0))    
big_inf['Average'] = ((0))                          # average duration column
big_inf["Freq total"] = ((0))
big_inf['Rate per min'] = ((0))
big_inf['Min 1'] = ((0)); big_inf['Min 2'] = ((0)); big_inf['Min 3'] = ((0)); big_inf['Min 4'] = ((0)); big_inf['Min 5'] = ((0))

#%% Big Cardiff Dataframes

# Create mother and infant dataframes
big_mum_cardiff = pd.Series(dtype = "float64", index = cs.multi_ind_cardiff)
big_mum_cardiff = big_mum_cardiff.to_frame(name = "Sum")            # convert pd.series to pd.dataframe
big_mum_cardiff['Sum'] = ((0))                              # start as zeros
big_mum_cardiff['Max duration'] = ((0))                     # add max and min duration
big_mum_cardiff['Min duration'] = ((0))    
big_mum_cardiff['Average'] = ((0))                          # average duration column
big_mum_cardiff["Freq total"] = ((0))
big_mum_cardiff['Rate per min'] = ((0))
big_mum_cardiff['Min 1'] = ((0)); big_mum_cardiff['Min 2'] = ((0)); big_mum_cardiff['Min 3'] = ((0)); big_mum_cardiff['Min 4'] = ((0)); big_mum_cardiff['Min 5'] = ((0))

big_inf_cardiff = pd.Series(dtype = "float64", index = cs.multi_ind_cardiff)
big_inf_cardiff = big_inf_cardiff.to_frame(name = "Sum")            # convert pd.series to pd.dataframe
big_inf_cardiff['Sum'] = ((0))                              # start as zeros
big_inf_cardiff['Max duration'] = ((0))                     # add max and min duration
big_inf_cardiff['Min duration'] = ((0))    
big_inf_cardiff['Average'] = ((0))                          # average duration column
big_inf_cardiff["Freq total"] = ((0))
big_inf_cardiff['Rate per min'] = ((0))
big_inf_cardiff['Min 1'] = ((0)); big_inf_cardiff['Min 2'] = ((0)); big_inf_cardiff['Min 3'] = ((0)); big_inf_cardiff['Min 4'] = ((0)); big_inf_cardiff['Min 5'] = ((0))

big_mum_cardiff.index.set_names(["Cardiff ID", "Code", "Behaviour"], inplace = True)
big_inf_cardiff.index.set_names(["Cardiff ID", "Code", "Behaviour"], inplace = True)
      
#%%
cardiff = [23, 21, 26, 29, 33, 87, 34, 63, 47, 48, 162, 185, 163, 190, 194, 195, 197, 199, 200, 204, 59, 74, 105, 106, 111, 121, 129, 141, 146, 154, 159]

One   = [0, 60];      OneTwo    = [0, 120];     OneTwoThree   = [0, 180];    OneTwoThreeFour  = [0, 240]; OneTwoThreeFourFive = [0, 300]
Two   = [60, 120];    TwoThree  = [60, 180];    TwoThreeFour  = [60, 240];   TwoThreeFourFive = [60, 300]
Three = [120, 180];   ThreeFour = [120, 240];   ThreeFourFive = [120, 300]
Four  = [180, 240];   FourFive  = [180, 300]
Five  = [240, 300]

timeframes = [One, OneTwo, OneTwoThree, OneTwoThreeFour, OneTwoThreeFourFive,
Two, TwoThree, TwoThreeFour, TwoThreeFourFive, Three, ThreeFour, ThreeFourFive, Four, FourFive, Five]
  
timeframe_names = ["One", "OneTwo", "OneTwoThree", "OneTwoThreeFour", "OneTwoThreeFourFive",
"Two", "TwoThree", "TwoThreeFour", "TwoThreeFourFive", "Three", "ThreeFour", "ThreeFourFive", "Four", "FourFive", "Five"]
  
df = pd.DataFrame(index=(cs.multi_ind_cardiff))
subcodes = df.loc["Cardiff23"].index.get_level_values("Behaviour")

#%% CARDIFF:
# All transition matrices

var_tup = []; var_tup2 = []

for i in range(len(timeframe_names)):
    time  = timeframe_names[i]
    for j in range(len(subcodes)):
       var_tup.append((time, subcodes[j]))

for i in range(len(cardiff)):
    c_dat = "Cardiff" + str(cardiff[i])
    for j in range(len(subcodes)):
       var_tup2.append((c_dat, subcodes[j]))
       
mum_all = pd.MultiIndex.from_tuples(var_tup); mum_all2 = pd.MultiIndex.from_tuples(var_tup2)
mum_all = pd.Series(dtype = "float64", index = mum_all); mum_all = mum_all.to_frame()
mum_all = mum_all.reindex(columns = mum_all2, fill_value=0)
mum_all = mum_all.transpose()

inf_all = pd.MultiIndex.from_tuples(var_tup); inf_all2 = pd.MultiIndex.from_tuples(var_tup2)
inf_all = pd.Series(dtype = "float64", index = inf_all); inf_all = inf_all.to_frame()
inf_all = inf_all.reindex(columns = inf_all2, fill_value=0)
inf_all = inf_all.transpose()

# All Stationary distribution
all_mum_stat = pd.MultiIndex.from_tuples(var_tup2)
all_mum_stat = pd.Series(dtype = "float64", index = all_mum_stat)
all_mum_stat = all_mum_stat.to_frame()
all_mum_stat = all_mum_stat.reindex(columns = timeframe_names, fill_value=0)

all_inf_stat = pd.MultiIndex.from_tuples(var_tup2)
all_inf_stat = pd.Series(dtype = "float64", index = all_inf_stat)
all_inf_stat = all_inf_stat.to_frame()
all_inf_stat = all_inf_stat.reindex(columns = timeframe_names, fill_value=0)


#%% BRISTOL MUM: 
#   All transition matrices

brism = ["278140497A_Feeding_AC", "278123519B_Stacking_IC", "278120336B_Stacking_IC",
"278119436A_Feeding_AC", "278115240A_feeding_RP_IC", "278108945A_Stacking1_IC",
"278107409A_feeding_EI_IC", "278107307A_feeding_RP_IC", "278105342B_Stacking_IC",
"278105342B_Feeding_AC_IC", "278103911A_Feeding_AC_IC", "278102804A_Feeding_AC",
"278102511A_Feeding_AC", "278101837A_Feeding_AC", "278100320A_Feeding_EI"]

var_tup = []; var_tup2 = []

for i in range(len(timeframe_names)):
    time  = timeframe_names[i]
    for j in range(len(subcodes)):
       var_tup.append((time, subcodes[j]))

for i in range(len(brism)):
    c_dat = brism[i]
    for j in range(len(subcodes)):
       var_tup2.append((c_dat, subcodes[j]))
       
mum_all_brism = pd.MultiIndex.from_tuples(var_tup); mum_all_brism2 = pd.MultiIndex.from_tuples(var_tup2)
mum_all_brism = pd.Series(dtype = "float64", index = mum_all_brism); mum_all_brism = mum_all_brism.to_frame()
mum_all_brism = mum_all_brism.reindex(columns = mum_all_brism2, fill_value=0)
mum_all_brism = mum_all_brism.transpose()

inf_all_brism = pd.MultiIndex.from_tuples(var_tup); inf_all_brism2 = pd.MultiIndex.from_tuples(var_tup2)
inf_all_brism = pd.Series(dtype = "float64", index = inf_all_brism); inf_all_brism = inf_all_brism.to_frame()
inf_all_brism = inf_all_brism.reindex(columns = inf_all_brism2, fill_value=0)
inf_all_brism = inf_all_brism.transpose()

# BRISTOL MUM All Stationary distributions
all_mum_stat_brism = pd.MultiIndex.from_tuples(var_tup2)
all_mum_stat_brism = pd.Series(dtype = "float64", index = all_mum_stat_brism)
all_mum_stat_brism = all_mum_stat_brism.to_frame()
all_mum_stat_brism = all_mum_stat_brism.reindex(columns = timeframe_names, fill_value=0)

all_inf_stat_brism = pd.MultiIndex.from_tuples(var_tup2)
all_inf_stat_brism = pd.Series(dtype = "float64", index = all_inf_stat_brism)
all_inf_stat_brism = all_inf_stat_brism.to_frame()
all_inf_stat_brism = all_inf_stat_brism.reindex(columns = timeframe_names, fill_value=0)

#%% BRISTOL DAD: 
# All transition matrices

brisd = ["278100311C_feeding_MR", "278109414A_feeding_MR","278120342A_reading_MR",
"278120342A_stacking_MR", "278127953A_feeding1_MR", "278127953A_feeding2_PC",
"278127953A_feeding3_PC", "278127953A_stacking_MR", "278128402B_stacking_PC",
"278128402B_stacking+feeding_MR", "278130718B_feeding_JS", "278147230A_bedtime_MR",
"278147230A_feeding_JS", "278147248A_P_freeplay+book_LM", "278147397A_feeding_MR",
"278147585A_feeding_MR", "2781472555A_feeding_LM"]

var_tup = []; var_tup2 = []

for i in range(len(timeframe_names)):
    time  = timeframe_names[i]
    for j in range(len(subcodes)):
       var_tup.append((time, subcodes[j]))

for i in range(len(brisd)):
    c_dat = brisd[i]
    for j in range(len(subcodes)):
       var_tup2.append((c_dat, subcodes[j]))
       
mum_all_brisd = pd.MultiIndex.from_tuples(var_tup); mum_all_brisd2 = pd.MultiIndex.from_tuples(var_tup2)
mum_all_brisd = pd.Series(dtype = "float64", index = mum_all_brisd); mum_all_brisd = mum_all_brisd.to_frame()
mum_all_brisd = mum_all_brisd.reindex(columns = mum_all_brisd2, fill_value=0)
mum_all_brisd = mum_all_brisd.transpose()

inf_all_brisd = pd.MultiIndex.from_tuples(var_tup); inf_all_brisd2 = pd.MultiIndex.from_tuples(var_tup2)
inf_all_brisd = pd.Series(dtype = "float64", index = inf_all_brisd); inf_all_brisd = inf_all_brisd.to_frame()
inf_all_brisd = inf_all_brisd.reindex(columns = inf_all_brisd2, fill_value=0)
inf_all_brisd = inf_all_brisd.transpose()

# BRISTOL DAD All Stationary distributions
all_mum_stat_brisd = pd.MultiIndex.from_tuples(var_tup2)
all_mum_stat_brisd = pd.Series(dtype = "float64", index = all_mum_stat_brisd)
all_mum_stat_brisd = all_mum_stat_brisd.to_frame()
all_mum_stat_brisd = all_mum_stat_brisd.reindex(columns = timeframe_names, fill_value=0)

all_inf_stat_brisd = pd.MultiIndex.from_tuples(var_tup2)
all_inf_stat_brisd = pd.Series(dtype = "float64", index = all_inf_stat_brisd)
all_inf_stat_brisd = all_inf_stat_brisd.to_frame()
all_inf_stat_brisd = all_inf_stat_brisd.reindex(columns = timeframe_names, fill_value=0)