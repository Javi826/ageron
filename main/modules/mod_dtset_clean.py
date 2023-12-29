# modules/mod_dtset_clean.py
import pandas as pd
import os
import time
from paths.paths import path_base,folder,archivo,csv_file_path,path_absolut, path_destination, path_save

# Timing
time_start = time.time()

def mod_dtset_clean(df_data):
    
    # restart dataframe jic
    restart_dataframes = True  
    # rstart or define main DataFrame 
    if 'df_data_clean' in locals() and restart_dataframes:del df_data_clean  # delete dataframe if exits
    
    print(f'START MODUL mod_dtset_clean')
    #print(f'Execution start time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_start))}\n')
    
    
    df_data_clean = df_data.copy()
    
    def day_week(df_data_clean):
        
        df_data_clean = df_data.copy()
        # column with dates
        date_column = 'date' 
    
        # ensuring date_column with date format
        df_data_clean[date_column] = pd.to_datetime(df_data_clean[date_column])
    
        # add column day_week + from label to number
        df_data_clean['day_week'] = df_data_clean[date_column].dt.dayofweek + 1  
        
        return df_data_clean

    # update df_date_clean
    df_data_clean = day_week(df_data_clean)
    #print("Step 01 OK: day_week") 

    def var_day(df_data_clean):

        # Calcular la variación diaria
        df_data_clean['var_day'] = (df_data_clean['close'] - df_data_clean['close'].shift(1)) / df_data_clean['close'] * 100
        
        
        return df_data_clean
    # update df_data_clean
    df_data_clean = var_day(df_data_clean)
    
    #print("Step 02 OK: var_day")
    
    def sort_columns(df_data_clean):

        desired_column_order = ['date', 'day_week', 'close', 'open', 'high', 'low', 'adj_close', 'var_day','volume']
    
        # Asegúrate de que todas las columnas especificadas estén presentes en el DataFrame
        missing_columns = set(desired_column_order) - set(df_data_clean.columns)
        if missing_columns:
            raise ValueError(f"Las siguientes columnas no están presentes en el DataFrame: {', '.join(missing_columns)}")
    
        # Sort columns
        df_data_clean = df_data_clean[desired_column_order]

        return df_data_clean
    
    # udpdate df_data_clean
    df_data_clean = sort_columns(df_data_clean)
    
    #print("Step 03 OK: sort_columns")
    
    def rounding_data(df_data_clean):

        columns_to_round = ['open', 'high', 'low', 'close', 'adj_close','var_day']
        
        # format float
        df_data_clean[columns_to_round] = df_data_clean[columns_to_round].astype(float)
        df_data_clean['day_week'] = df_data_clean['day_week'].astype(int)
        
        #format rounding 
        for column in columns_to_round:
          if column in df_data_clean.columns:
              df_data_clean[column] = df_data_clean[column].round(2)
        
        #for column in columns_to_round:
            #if column in df_data_clean.columns:
                #df_data_clean[column] = df_data_clean[column].apply(lambda x: '{:.2f}'.format(x))
        
            
        return df_data_clean
    
    # udpdate df_data_clean
    df_data_clean = rounding_data(df_data_clean)
    
    #print("Step 04 OK: rounding_data") 
    
    # TIMING
    time_end = time.time()
    time_execution = round((time_end - time_start), 1)
    
    # SAVE FILE
    if not os.path.exists(os.path.join(path_base, path_destination)): os.makedirs(os.path.join(path_base, path_destination))
    df_data_clean.to_csv(path_save, index=False)
    
    
    time_end = time.time()
    time_execution = round((time_end - time_start), 1)
    #print(f"DataFrame saved in: {path_save}")
    #print("Time execution:",time_execution)
    #print(f'Execution end time: {time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_end))}')
    print(f'END MODUL mod_dtset_clean\n')
    
    return df_data_clean



