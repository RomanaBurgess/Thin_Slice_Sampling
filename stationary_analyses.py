# Import packages and files 
import pandas as pd
import numpy as np
import coding_scheme as cs
import datetime
import statistics as stats
import behaviour_measures as bm
from scipy.stats.distributions import chi2

#%% Stationary Distribution Analysis and Plots
# Load stationary distribution dataframes
stats = pd.read_excel("./MUM_STAT.xlsx", index_col=[0, 1])

# Label dataframe indices
stats.index.set_names(["ID", "Behaviour"], inplace = True)

# Predefine dataframes to save % agreements
st  = pd.DataFrame(columns = cs.thin_slice_names, index = cs.multi_ind)

# Look for significant differences between stationary distributions at timeframe T 
# and "true" stationary distributions

for i in range(len(cs.all_codes)):
    
    # Define subcodes for behavioural group
    subcodes = cs.all_codes[i]
    
    for j in range(len(cs.thin_slice_names)):
    
        # Define thin slice
        T = cs.thin_slice_names[j]
        
        true = stats.loc[(slice(None), subcodes), ("OneTwoThreeFourFive")]

        # Subset relevant matrices from dataframes
        mat = stats.loc[(slice(None), subcodes), (T)]
        
        # Define difference matrices (between SDs at T and true SD)
        stat_diff = pd.DataFrame(abs(mat.values - true.values), index = mat.index)

        # Find indices of values less than tolerance
        stat_diff = stat_diff.groupby(level = "Behaviour").mean()
        
        # Save the % of datasets with difference less than tolerance
        if len(stat_diff) != 0:          
            st.loc[(slice(None), subcodes), T] = stat_diff.values         
        else:
            st.loc[(slice(None), subcodes), T] = 0  
           
# Reformat difference dataframe for box plot   
st = st[st != 0]; 
St = st.reindex(columns= ["One", "Two", "Three", "Four", "Five", "OneTwo", "TwoThree", "ThreeFour", "FourFive", "OneTwoThree", "
                          TwoThreeFour", "ThreeFourFive", "OneTwoThreeFour", "TwoThreeFourFive"])

# Remove codes from analyses with not enough occurrences
remove_codes = [cs.view, cs.alertness_state, cs.encouragement, cs.agitation_soothing, cs.role_reversal,
               cs.physical_imitation, cs.acknowledgment, cs.eating, cs.rough_and_tumble, 
               cs.caregiver_unusual_behaviours, cs.infant_unusual_behaviours]

St.index.set_names(["Behaviour", "Code"], inplace = True)

for i in range(len(remove_codes)):
    codes = remove_codes[i]
    St = St[~St.index.get_level_values("Code").isin(codes)]

# Plot Absolute differences
St.plot(kind="box", vert = False, figsize = [8,8], xlim = [-0.02, 0.42], fontsize = 13, title = "Distribution of differences of stationary distributions from true stationary distributions")

#%% Chi squared test for stationary distributions
# Remove full-session from thin slice arrays
TFN = cs.thin_slice_names.copy(); TF  = cs.thin_slices.copy(); del TF[4]; del TFN[4]

# Pre-define dataframe to store chi square values 
X2_stat = pd.DataFrame(index = cs.all_names, columns = TFN)

# Loop over thin slices
for t in range(len(TFN)):
    
    thin_slice = TFN[t]
    T         = TF[t]
       
    # Loop over behaviorual group
    for n in range(len(cs.all_codes)):
        
        # Define behavioural group and subcodes of interest
        subcodes    = cs.all_codes[n] 
        name        = cs.all_names[n]  
                          
        # Subset data to chosen subject                  
        dat         = bm.all_dat[bm.all_dat["Subject"] == "Caregiver 1"]
        dat         = dat[dat["Behavior"].isin(subcodes)]
        
        # Subset to data within specified thin slice
        dat = dat[dat["Time_Relative_hms"] < datetime.time(minute = int(T[1]/60))]
        dat = dat[dat["Time_Relative_hms"] >= datetime.time(minute = int(T[0]/60))]
        
        if len(dat) != 0:
            
            # Extract full-session stationary distribution "P"
            P = mum_stats.loc[(slice(None), subcodes), "OneTwoThreeFourFive"]  
            P.index.set_names(["Cardiff ID", "Behaviour"], inplace = True)
            P     = P[(P != 0)]
            P_sum = P.groupby(level = "Behaviour").sum().sum() # number of subjects
            P     = P.groupby(level = "Behaviour").apply(lambda x: x.sum()/P_sum)   
                           
            subcodes = P.index
            
            # Extract average stationary distribution for given thin slice "Q"
            Q      = pd.Series(0, index = subcodes)
            Q_temp = mum_stats.loc[(slice(None), subcodes), timeframe]     
            Q_temp.index.set_names(["Cardiff ID", "Behaviour"], inplace = True) 
            
            Q_sum  = Q_temp.groupby(level = "Behaviour").sum().sum() # number of subjects
            Q_temp = Q_temp.groupby(level = "Behaviour").apply(lambda x: x.sum()/Q_sum)
            
            Q.loc[Q_temp.index] = Q_temp.values   
            Q                   = Q.loc[P.index]
                
            # Weight stationary distributions by length of thin slice
            p = P.values*300
            q = Q.values*300
            
            # Compute chi square values
            xi = ((q - p)**2)/(p)
            xi[np.isnan(xi)] = 0    
            xi[~np.isfinite(xi)] = 0
                
            # Extract associated p-val
            p_val = chi2.sf(xi.sum(), len(p)-1)
            
            # Save correctly formatted in a table for write up purposes
            if (p_val <= 0.05) & (p_val > 0.005):
                X2_stat.loc[name, thin_slice] = str(np.round(np.nansum(xi), 2)) + "*" 
                
            elif (p_val <= 0.005) & (p_val > 0.001):
                X2_stat.loc[name, thin_slice] = str(np.round(np.nansum(xi), 2)) + "**" 
                
            elif (p_val <= 0.001):
                X2_stat.loc[name, thin_slice] = str(np.round(np.nansum(xi), 2)) + "***" 
                
            else:
                X2_stat.loc[name, thin_slice] = str(np.round(np.nansum(xi), 2))
            
