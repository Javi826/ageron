#FUNTCIONS
"""
Created on Sun Dec 31 09:53:59 2023
@author: jlahoz
"""
from modules.mod_init import *

def day_week(df_data_clean):
    
    # column with dates
    date_column = 'date' 

    # ensuring date_column with date format
    df_data_clean[date_column] = pd.to_datetime(df_data_clean[date_column])

    # add column day_week + from label to number
    df_data_clean['day_week'] = df_data_clean[date_column].dt.dayofweek + 1  
    
    return df_data_clean

def var_day(df_data_clean):

    # Calcular la variación diaria
    df_data_clean['var_day'] = (df_data_clean['close'] - df_data_clean['close'].shift(1)) / df_data_clean['close'] * 100
        
    return df_data_clean

def sort_columns(df_data_clean):

    #desired_column_order = columns_clean
    desired_column_order= ['date', 'day_week', 'close', 'open', 'high', 'low', 'adj_close', 'var_day','volume']

    # Asegúrate de que todas las columnas especificadas estén presentes en el DataFrame
    missing_columns = set(desired_column_order) - set(df_data_clean.columns)
    if missing_columns:
        raise ValueError(f"following columns no in DataFrame: {', '.join(missing_columns)}")

    # Sort columns
    df_data_clean = df_data_clean[desired_column_order]

    return df_data_clean

def rounding_data(df_data_clean):

    columns_to_round = ['open', 'high', 'low', 'close', 'adj_close','var_day']
    
    # format float
    df_data_clean[columns_to_round] = df_data_clean[columns_to_round].astype(float)
    df_data_clean['day_week'] = df_data_clean['day_week'].astype(int)
    
    #format rounding 
    for column in columns_to_round:
      if column in df_data_clean.columns:
          df_data_clean[column] = df_data_clean[column].round(2)
    
            
    return df_data_clean