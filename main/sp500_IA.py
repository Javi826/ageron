# MAIN

import yfinance as yf
import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models, initializers
from modules.mod_dtset_clean import mod_dtset_clean
from paths.paths import csv_folder,path_base,folder,archivo,csv_file_path,path_absolut
import warnings
import time
import os
import pandas as pd

# IGNORE WARNINGS
warnings.filterwarnings("ignore")

# YAHOO Call
symbol = "^GSPC"
start_date = "2000-01-01"
end_date = "2020-12-31"
sp500_data = yf.download(symbol, start=start_date, end=end_date)

# SAVE yahoo file
if not os.path.exists(csv_folder): os.makedirs(csv_folder)
sp500_data.to_csv(csv_file_path)

print(f"The data has been saved to: {csv_file_path}")

# timing
time_start = time.time()
print(f'START MAIN\n')

# READING file
df_data = pd.read_csv(path_absolut, header=None, skiprows=1, names=['date','open','high','low','close','adj_close','volume'])
print("Step 01 OK: reading file")

# call module data cleaning + trans
df_clean = mod_dtset_clean(df_data)


print(f'END MAIN\n')