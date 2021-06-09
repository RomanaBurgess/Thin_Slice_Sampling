# Import packages and additional files
import pandas as pd
import coding_scheme as cs
      
# Define dyad ID numbers
IDS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Define thin slices
One   = [0, 60];      OneTwo    = [0, 120];     OneTwoThree   = [0, 180];    OneTwoThreeFour  = [0, 240]; OneTwoThreeFourFive = [0, 300]
Two   = [60, 120];    TwoThree  = [60, 180];    TwoThreeFour  = [60, 240];   TwoThreeFourFive = [60, 300]
Three = [120, 180];   ThreeFour = [120, 240];   ThreeFourFive = [120, 300]
Four  = [180, 240];   FourFive  = [180, 300]
Five  = [240, 300]

thin_slices = [One, OneTwo, OneTwoThree, OneTwoThreeFour, OneTwoThreeFourFive,
Two, TwoThree, TwoThreeFour, TwoThreeFourFive, Three, ThreeFour, ThreeFourFive, Four, FourFive, Five]
  
thin_slice_names = ["One", "OneTwo", "OneTwoThree", "OneTwoThreeFour", "OneTwoThreeFourFive",
"Two", "TwoThree", "TwoThreeFour", "TwoThreeFourFive", "Three", "ThreeFour", "ThreeFourFive", "Four", "FourFive", "Five"]
  
# Extract list of all individual codes
df = pd.DataFrame(index=(cs.multi_ind_cardiff))
subcodes = df.loc["dyad1"].index.get_level_values("Behaviour")

# Pre define dataframe indices
var_tup = []; var_tup2 = []

for i in range(len(tthin_slice_names)):
    time  = thin_slice_names[i]
    for j in range(len(subcodes)):
       var_tup.append((time, subcodes[j]))

for i in range(len(IDs)):
    c_dat = "dyad" + str(IDs[i])
    for j in range(len(subcodes)):
       var_tup2.append((c_dat, subcodes[j]))
      
# Create dataframe to store mum (parent) transition matrices    
mum_all = pd.MultiIndex.from_tuples(var_tup); mum_all2 = pd.MultiIndex.from_tuples(var_tup2)
mum_all = pd.Series(dtype = "float64", index = mum_all); mum_all = mum_all.to_frame()
mum_all = mum_all.reindex(columns = mum_all2, fill_value=0)
mum_all = mum_all.transpose()

# Create dataframe to store infant transition matrices  
inf_all = pd.MultiIndex.from_tuples(var_tup); inf_all2 = pd.MultiIndex.from_tuples(var_tup2)
inf_all = pd.Series(dtype = "float64", index = inf_all); inf_all = inf_all.to_frame()
inf_all = inf_all.reindex(columns = inf_all2, fill_value=0)
inf_all = inf_all.transpose()

# Create dataframe to store mum (parent) stationary distributions
all_mum_stat = pd.MultiIndex.from_tuples(var_tup2)
all_mum_stat = pd.Series(dtype = "float64", index = all_mum_stat)
all_mum_stat = all_mum_stat.to_frame()
all_mum_stat = all_mum_stat.reindex(columns = timeframe_names, fill_value=0)

# Create dataframe to store infant stationary distributions  
all_inf_stat = pd.MultiIndex.from_tuples(var_tup2)
all_inf_stat = pd.Series(dtype = "float64", index = all_inf_stat)
all_inf_stat = all_inf_stat.to_frame()
all_inf_stat = all_inf_stat.reindex(columns = timeframe_names, fill_value=0)
