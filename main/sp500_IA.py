# MAIN
from modules.mod_init import *
from paths.paths import *
from modules.mod_dtset_clean import mod_dtset_clean
from modules.mod_preprocessing import mod_preprocessing

print(f'START MAIN\n')

# YAHOO Call
symbol = "^GSPC"
global start_date
global endin_date

start_date = "1980-01-01"
endin_date = "2020-12-31"
sp500_data = yf.download(symbol, start=start_date, end=endin_date)

# SAVE yahoo file
sp500_data.to_csv(path_file_csv)
#print(f"The data has been saved to: {path_file_csv}")

#READING yahoo file
df_data = pd.read_csv(path_file_csv, header=None, skiprows=1, names=columns_csv)

#CALL module Datacleaning
df_data_clean = mod_dtset_clean(df_data,start_date,endin_date)
#CALL module Preprocessing
#Range
filter_start_date = '2001-01-01'
filter_endin_date = '2019-12-31'
df_preprocessing = mod_preprocessing(df_data_clean,filter_start_date,filter_endin_date)

print(f'ENDIN MAIN\n')