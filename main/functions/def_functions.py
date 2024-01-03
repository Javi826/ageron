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

def filter_data_by_date_range(df, start_date, end_date):
    return df[(df['date'] >= start_date) & (df['date'] <= end_date)]


def df_plots(x, y, x_label, y_label,plot_style):
    
    plt.figure(figsize=(10, 6))
    
    if plot_style == "lines":
        plt.plot(x, y, label=f'{x_label} vs {y_label}')  # Use a line plot
    elif plot_style == "points":
        plt.scatter(x, y, label=f'{x_label} vs {y_label}', marker='o')  # Use a scatter plot with markers
    else:
        raise ValueError("Invalid plot_style. Use 'lines' or 'points'.")

    plt.title(f'{x_label} vs {y_label} Plot')
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    plt.grid(True)
    plt.show()
            
def plots_histograms(dataframe, columns_of_interest):
    bins = 30
    figsize = (15, 5)
    
    # plot
    fig, axes = plt.subplots(nrows=1, ncols=len(columns_of_interest), figsize=figsize)
    
    # Columns
    for i, column in enumerate(columns_of_interest):
        axes[i].hist(dataframe[column], bins=bins, color='skyblue', edgecolor='black')
        axes[i].set_title(f'Histogram de {column}')
        axes[i].set_xlabel(column)
        axes[i].set_ylabel('frequency')
    
    # design
    plt.tight_layout()
    plt.show()

