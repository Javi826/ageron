#PATHS
"""
Created on Sat Dec 30 21:06:19 2023
@author: jlahoz
"""

import os

# Directory to store CSV files
path_base = r"C:\Users\javier\Desktop\ML\ageron"

file_df_data = "sp500_data.csv"
folder_csv = "inputs\historicyh"
path_file_csv = os.path.join(path_base,folder_csv,file_df_data)

file_df_data_clean = "df_data_clean.csv"
folder_df_data_clean = "inputs\dtset_clean"
path_df_data_clean = os.path.join(path_base,folder_df_data_clean, file_df_data_clean)

file_summary_stats = 'df_summary_stats'
folder_summary_stats = "outputs\\summary_stats"
path_summary_stats= os.path.join(path_base,folder_summary_stats, file_summary_stats)

file_preprocessing = 'df_preprocessing.xlsx'
folder_preprocessing = "outputs\\preprocessing"
path_preprocessing = os.path.join(path_base,folder_preprocessing, file_preprocessing)






