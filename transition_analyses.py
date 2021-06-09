#%% Transition matrix analysis.
# Calculates absolute differences between transition matrices over thin slices and fully coded interactions. These absolute differences are plotted in a box plot.
# Chi square analyses are performed on these absolute differences to evaluate significance, outputted as a formatted table "X2".

# Import packages and files
import pandas as pd
import numpy as np
import coding_scheme as cs
from scipy.stats.distributions import chi2

# Define dyad ID numbers
IDs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Box plot analysis
# Load pre-saved transition matrix dataframe (change file name to load infant transitions)
trans = pd.read_excel("./MUM_TRANS.xlsx", index_col=[0,1], header=[0,1])

# Label dataframe index columns
trans.index.set_names(["ID", "Behaviour"], inplace = True)

# Define new dataframes to store absolute differences
tr = pd.DataFrame(index = cs.multi_ind, columns = thin_slice_names)

# Calculate absolute differences between thin slices and full-sessions
# Loop over distinct behavioural groups
for i in range(len(cs.all_codes)):
    
    # Define subcodes
    subcodes = cs.all_codes[i]
    
    # Extract fully-coded transition matrices for specified subcodes
    true = trans.loc[(slice(None), subcodes), ("OneTwoThreeFourFive", subcodes)]
    true[true == 0] = np.nan
    
    # Loop over each slice
    for j in range(len(cs.thin_slice_names)):
    
        # Name of given slice
        T = cs.thin_slice_names[j]
        
        # Subset relevant transitions matrices from large dataframes
        mat = trans.loc[(slice(None), subcodes), (T, subcodes)]

        # Define "difference matrices" (between transitions at T and true transitions)
        diff = pd.DataFrame(abs(mat.values - truevalues), index = mat.index, columns = subcodes)
 
        # Extract mean absolute difference for each behavioural group
        diff = diff.groupby(level = "Behaviour").mean()
      
        # Store differences
        tr.loc[(cs.all_names[i], subcodes), T] = diff.mean(axis=1).values      

# Reorder columns for aesthetic purposes
Tr = tr.reindex(columns= ["One", "Two", "Three", "Four", "Five", "OneTwo", "TwoThree", "ThreeFour", "FourFive", "OneTwoThree", "TwoThreeFour", 
                 "ThreeFourFive", "OneTwoThreeFour", "TwoThreeFourFive"])

# Set index names
Tr.index.set_names(["Code", "Behaviour"], inplace = True)

# Remove codes from analysis with not enough occurrences
remove_codes = [cs.audio, cs.view, cs.alertness_state, cs.encouragement, cs.agitation_soothing, cs.role_reversal,
               cs.physical_imitation, cs.acknowledgment, cs.eating, cs.rough_and_tumble, 
               cs.caregiver_unusual_behaviours, cs.infant_unusual_behaviours]

for i in range(len(remove_codes)):
    codes = remove_codes[i]
    Tr = Tr[~Tr.index.get_level_values("Behaviour").isin(codes)]

# Plot absolute difference box plots
Tr.plot(kind="box", vert = False, figsize = [8,8], xlim = [-0.02, 1.02], fontsize = 13, title = "Distribution of differences of transition matrices from true transition matrices")

#%% Chi squared test for transition matrices
# Note: these analysis require transition FREQUENCIES, not probabilities.

# Drop full-session thin slice
TFN = thin_slice_names.copy(); TF  = thin_slices.copy(); del TF[4]; del TFN[4]

# Predefine dataframes to store chi square values
X2 = pd.DataFrame(index = trans.index.get_level_values("Behaviour").unique(), columns = TFN)

# Calculate chi square values 
# Loop over thin slices
for t in range(len(TFN)):
    
    thin_slice = TFN[t]
    T          = TF[t]
    
    # Loop over behavioural groups
    for n in range(len(cs.all_codes)):
        
        # Define one behavioural group and subcodes 
        code = cs.all_names[n]
        subcodes = cs.all_codes[n]
        
        # Extract averaged full-session transition matrix P
        P = trans.loc[(slice(None), subcodes), ("OneTwoThreeFourFive", subcodes)] 
        P.index.set_names(["ID", "Behaviour"], inplace = True)
        P = P.loc[(P.sum(axis=1) != 0)]           
        P   = P.groupby(level = "Behaviour").mean()
        p_ind    = P.index.get_level_values("Behaviour")
        P = P.loc[p_ind, (slice(None), p_ind)]
        
        if len(p_ind) != 0:
            
            # Extract averaged thin slice transition matrix Q
            Q = pd.DataFrame(0, index = p_ind, columns = p_ind)
            Q_temp = trans.loc[(slice(None), p_ind), (thin_slice, p_ind)]    
            Q_temp = Q_temp.loc[(Q_temp.sum(axis=1) != 0)]
            Q_temp.index.set_names(["ID", "Behaviour"], inplace = True)  
            Q_temp = Q_temp.groupby(level = "Behaviour").mean()
            Q.loc[Q_temp.index, Q_temp.columns.droplevel(0)] = Q_temp.values
            
            P.columns = P.columns.droplevel(0)
            Q = Q.loc[:, P.columns]
            
            # Calculate and store chi square values                
            for i in range(len(p_ind)):
                
                p = P.loc[p_ind[i], :].values
                q = Q.loc[p_ind[i], :].values
    
                # Extract chi square value
                xi = ((q - p)**2)/(p)
                xi[~np.isfinite(xi)] = 0
                
                # Extract associated p-val
                p_val = chi2.sf(np.nansum(xi), len(p_ind)-1)
                
                # Save correctly formatted in a table for write up purposes
                if (p_val <= 0.05) & (p_val > 0.005):
                    X2.loc[p_ind[i], thin_slice] = str(np.round(np.nansum(xi), 2)) + "*" 
                    
                elif (p_val <= 0.005) & (p_val > 0.001):
                    X2.loc[p_ind[i], thin_slice] = str(np.round(np.nansum(xi), 2)) + "**" 
                    
                elif p_val <= 0.001:
                    X2.loc[p_ind[i], thin_slice] = str(np.round(np.nansum(xi), 2)) + "***" 
                    
                else:
                    X2.loc[p_ind[i], thin_slice] = str(np.round(np.nansum(xi), 2))
                                 
            
