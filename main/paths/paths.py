#PATHS

import os

# Directory to store CSV files
csv_folder = r"C:\Users\jlaho\Desktop\ML\ageron\sp500_IA\inputs\historicyh"
path_base = r"C:\Users\jlaho\Desktop\ML\ageron\sp500_IA"
folder = "inputs\historicyh"
archivo = "sp500_data.csv"
csv_file_path = os.path.join(csv_folder, "sp500_data.csv")
path_absolut = os.path.join(path_base, folder, archivo)
path_destination = "inputs\dtset_clean"
path_save = os.path.join(path_base, path_destination, "df_data_clean.csv")




