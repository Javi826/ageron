#MODULE SUMMARY STATS
"""
Created on Sat Dec 30 21:06:19 2023
@author: jlahoz
"""
from modules.mod_init import *
from paths.paths import *
from main.sp500_IA import start_date, endin_date
from functions.def_functions import *

# Construct the file name based on start_date and endin_date
file_df_data_clean = f"df_data_clean_{start_date}_{endin_date}.csv"
file_path_df_data_clean = os.path.join(path_base, folder_df_data_clean, file_df_data_clean)

# READING file
df_data_clean = pd.read_csv(file_path_df_data_clean, header=None, skiprows=1, names=columns_clean)
print(df_data_clean.head(5))

# STATS Range
filter_start_date = '2000-01-01'
filter_endin_date = '2020-12-31'

# filtering data by date
df_clean_filter = filter_data_by_date_range(df_data_clean, filter_start_date, filter_endin_date)

df_clean_filter['date'] = pd.to_datetime(df_clean_filter['date'])
#df_clean_filter['date'] = df_clean_filter['date'].dt.strftime('%Y-%m-%d')
#df_clean_filter['year'] = df_clean_filter['date'].dt.strftime('%Y')

#PLOT
df_plots(df_clean_filter['date'],df_clean_filter['close'],'date','close','lines')
print(df_clean_filter['date'])
#SUMARY
summary_stats_all = df_clean_filter.describe(include='all')
print(summary_stats_all)

#HISTOGRAMS
columns_of_interest = ['day_week','close','open','high', 'low','adj_close','var_day', 'volume']
plots_histograms(df_clean_filter, columns_of_interest)

#PEARSONS
# numeric columns select
columns_numeric = df_clean_filter.select_dtypes(include=['float', 'int']).columns

# Pearson + Sort ascdending
pearsons = df_clean_filter[columns_numeric].corrwith(df_data_clean['close'], method='pearson').sort_values(ascending=False)

print(pearsons)