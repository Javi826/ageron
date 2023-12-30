# MAIN
from modules.mod_init import *
from modules.mod_dtset_clean import mod_dtset_clean

# YAHOO Call
symbol = "^GSPC"
start_date = "2002-01-01"
end_date = "2020-12-31"
sp500_data = yf.download(symbol, start=start_date, end=end_date)

# SAVE yahoo file
if not os.path.exists(folder_csv): os.makedirs(folder_csv)
sp500_data.to_csv(path_file_csv)

print(f"The data has been saved to: {path_file_csv}")

# timing

print(f'START MAIN\n')

# READING yahoo file
df_data = pd.read_csv(path_file_csv, header=None, skiprows=1, names=columns_csv)

# CALL module data cleaning + trans
df_clean = mod_dtset_clean(df_data)


print(f'ENDIN MAIN\n')