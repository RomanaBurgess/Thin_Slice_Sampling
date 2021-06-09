# File used to reformat the .xlsx data to be more accessible

# Import packages
import datetime
import numpy as np
import pandas as pd

# Define function to generally format the data
def format_data(data):
    
    # Create copy of the imported data to avoid errors
    data_copy = data.copy(); del(data)

    # Remove "State Stop" rows (unnessary feature of Observer XT event log output)
    data_copy = data_copy[~(data_copy["Event_Type"] == "State stop")]

    # Extract microseconds from Time_Relative_sf
    decimals = data_copy["Time_Relative_sf"] - data_copy["Time_Relative_sf"].apply(np.floor)
    int_mics = np.multiply(decimals, 1000000).astype("int")
    
    # Add microseconds to Time_Relative_hms in datetime format
    for i in range(len(data_copy)):
        
        ii = data_copy.index[i]
        time0 = data_copy.loc[ii, "Time_Relative_hms"]
        
        data_copy.loc[ii, "Time_Relative_hms"] = datetime.datetime(
                    1, 1, 1,
                    hour = time0.hour,
                    minute = time0.minute,
                    second = time0.second,
                    microsecond = int_mics.loc[ii]
                )
        
    # Calculate End Time to replace State Stop rows
    # Separate duration into sec and microsec
    decimals = data_copy["Duration_sf"] - data_copy["Duration_sf"].apply(np.floor)
    micro = np.multiply(decimals, 1000000).astype("int")
    all_sec = data_copy["Duration_sf"].apply(np.floor).astype("int")
    mins = all_sec.apply(lambda a: a // 60); secs = all_sec.apply(lambda a: a % 60)
    
    # Add duration in correct format
    for i in range(len(data_copy)):
        ii = data_copy.index[i]
        data_copy.loc[ii, "Duration_sf"] = datetime.timedelta(
             minutes = int(mins.loc[ii]), 
             seconds = int(secs.loc[ii]), 
             microseconds = int(micro.loc[ii])
        )
         
    # Add End Time column 
    data_copy["Time_End"] = (data_copy.iloc[:, 0] + data_copy.iloc[:, 2]).apply(lambda a: a.time())     
    data_copy["Time_Relative_hms"] = data_copy["Time_Relative_hms"].apply(lambda a: a.time())
    
    return data_copy

# Define function to "split" data where time period of a behaviour overalaps with minute mark
# This is important for extracting the transition data
def split_data(data):
    
    # Extract all behaviour start and end times
    starts = data.Time_Relative_hms.apply(lambda a: a.minute)
    ends   = data.Time_End.apply(lambda a: a.minute)
    
    # Identify datapoints which overlap with 1.00, 2.00 etc.
    # Label as "keep" or "split"
    d_split = data[ends > starts]
    d_keep  = data[ends == starts]
    
    df = pd.DataFrame(d_keep)
    
    # Split data overlapping minute mark into 2 (or more) separate data entries
    for i in range(len(d_split)):
            
            start  = d_split.iloc[i, :].Time_Relative_hms
            end    = d_split.iloc[i, :].Time_End
            n_mins = end.minute - start.minute
            A      = pd.DataFrame(columns = ["Start", "End"], index = range(n_mins+1))
            rows   = pd.DataFrame(columns = d_split.columns)
         
            for j in range(n_mins+1):
                
                st = datetime.time(minute = (start.minute + j))
                et = datetime.time(minute = (start.minute + j+1))
                
                A.loc[j, "Start"] = st; A.loc[j, "End"]   = et
                
                rows = rows.append(d_split.iloc[i, :])
            
            A.loc[0, "Start"]      = start
            A.loc[len(A)-1, "End"] = end
            
            # Store the split data by start and end time
            rows["Time_Relative_hms"] = A.loc[:, "Start"].values
            rows["Time_End"] = A.loc[:, "End"].values
             
            A = pd.DataFrame(index = range(len(rows)), columns = ["Duration", "Start"])
            
            # Reformat new data entries
            # Add duration_sf and time_relative_sf in correct format
            for i in range(len(rows)):
                
                A.iloc[i, :]["Duration"] = datetime.timedelta(
                     minutes      = int(rows.iloc[i]["Time_End"].minute - rows.iloc[i]["Time_Relative_hms"].minute), 
                     seconds      = int(rows.iloc[i]["Time_End"].second - rows.iloc[i]["Time_Relative_hms"].second), 
                     microseconds = int(rows.iloc[i]["Time_End"].microsecond - rows.iloc[i]["Time_Relative_hms"].microsecond)
                     )
                
                A.iloc[i, :]["Start"] = datetime.timedelta(
                     minutes      = int(rows.iloc[i]["Time_Relative_hms"].minute), 
                     seconds      = int(rows.iloc[i]["Time_Relative_hms"].second), 
                     microseconds = int(rows.iloc[i]["Time_Relative_hms"].microsecond)
                     )
            
            rows["Duration_sf"]       = A.loc[:, "Duration"].values
            rows["Time_Relative_sf"]  = A.loc[:, "Start"].apply(lambda a: a.total_seconds()).values
    
            df = df.append(rows)
            
    return df
