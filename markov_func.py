# File to define Markov Analysis functions for transition matrices and stationary distributions

# Import packages
import pandas as pd
import numpy as np

# Define function to extract transition matrices
# Takes dataframe of interaction data for specific behavioural group, relevant subcodes, thin slice definitions and names as inputs
# Outputs transition matrices calulcated over each thin slice
def MarkovTime(code, subcodes, thin_slices, thin_slice_names):
    
    # Create multi column dataframe to store multiple transition probability matrices
    var_tup = []
    for i in range(len(timeframes)):
        time  = timeframe_names[i]
        for j in range(len(subcodes)):
           var_tup.append((time, subcodes[j]))
    
    DF = pd.MultiIndex.from_tuples(var_tup)
    DF = pd.Series(dtype = "float64", index = DF); DF = DF.to_frame()
    DF = DF.reindex(columns=list(subcodes), fill_value=0)
    DF = DF.transpose()

    # Loop over each thin slice 
    # Calculate transition probability matrix and add to large dataframe   
    for n in range(len(timeframes)):
        
        T = thin_slices[n]
        x_ini = T[0]; x_end = T[1]
        
        codes = code[code.Time_Relative_sf < x_end]       # Subset relevant data
        codes = codes[codes.Time_Relative_sf >= x_ini]    
        df = pd.DataFrame(0, subcodes, subcodes)          # Create empty dataframe
        unique = codes.Behavior.unique()                  # Array of unique behaviours expressed within the data
    
        # Calculate transition frequencies row by row
        for j in range(x_ini, x_end):
            
            if j == x_ini:
                original = codes[codes.Time_Relative_sf == j]
                
                if len(original) > 1:
                    larg = original.Duration_sf.values.argmax()
                    original = original.iloc[larg]
                       
                original = original.Behavior
                
            else:
                original = subsequent
                
            subsequent = codes[codes.Time_Relative_sf < j+1]
            subsequent = subsequent.sort_values(by="Time_Relative_sf").tail(1)
            subsequent = subsequent.Behavior
             
            df.loc[original, subsequent] = df.loc[original, subsequent] + 1
               
        # Convert transition frequencies to probabilities        
        for i in unique:
            df.loc[i,:] = df.loc[i,:]/sum(df.loc[i,:]) 
        
        # Store individual transition matrix in large dataframe of matrices
        name = timeframe_names[n]
        DF.loc[subcodes, name] = df.values
        DF = DF.fillna(0); df = df.fillna(0)

    return DF

# Define function to extract stationary distributions 
# Takes transition matrix for a behavioural group, definition of behavioural group and subcodes as inputs
# Outputs stationary distribution and "flag" if stationary distribution was unable to be calculated
def station(df, code, subcode):
    
    if len(code) != 0:

        # remove zero rows and columns
        good_rows = df.index[df.sum(axis=1)!=0]
        df = df.loc[good_rows, good_rows]
        
        if len(df) != 0:
            
            # calculate eigenvalues and eigenvectors
            eigenvalues, eigenvectors = np.linalg.eig(df.T)
            
            # find eigenvectors that correspond to eigenvalue closest to 1
            evec = eigenvectors[:, np.abs(eigenvalues-1).argmin()]; #evec = evec[:,0]

            stationary = evec / evec.sum()
            stationary = stationary.real    # take real part only, should sum to 1
            
            stationary_distribution = pd.Series(stationary, df.index)
            
            flag = True
            
        else:      
            
            stationary_distribution = 0      
            flag = False
        
    else:       
        stationary_distribution = 0
        flag = False
        
    return stationary_distribution, flag
