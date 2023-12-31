#MOD_PIPELINES
"""
Created on Sat Dec 30 21:06:19 2023
@author: jlahoz
"""
import os
from modules.mod_init import *

start_date = "1980-01-01"
endin_date = "1990-12-31"

# Construct the file name based on start_date and endin_date
file_df_data_clean = f"df_data_clean_{start_date}_{endin_date}.csv"
file_path_df_data_clean = os.path.join(path_base, folder_df_data_clean, file_df_data_clean)

# READING file
df_data_clean = pd.read_csv(file_path_df_data_clean, header=None, skiprows=1, names=columns_clean)
print(df_data_clean.head(5))

def filter_data_by_date_range(df, pipe_start_date, pipe_endin_date):
    return df[(df['date'] >= pipe_start_date) & (df['date'] <= pipe_endin_date)]

# PIPELINE Range
pipe_start_date = '1985-01-01'
pipe_endin_date = '1988-12-31'

# filtering data by date
df_clean_filter = filter_data_by_date_range(df_data_clean, pipe_start_date, pipe_endin_date)


#TRAIN AND TEST DATA selection
train_set, test_set = train_test_split(df_clean_filter, test_size=0.2,random_state=42)
strat_train_set, strat_test_set = train_test_split(df_clean_filter, test_size=0.2,stratify= df_clean_filter['day_week'], random_state=42)

print(strat_test_set["day_week"].value_counts() / len(strat_test_set))

#percentage_per_day_clean = (df_clean_filter['day_week'].value_counts(normalize=True) * 100).sort_index()
percentage_per_day_clean = (df_clean_filter['day_week'].value_counts() / len(df_clean_filter))
# Print the results
print("\nPercentage of records by day of the week in df_clean_filter:")
print(percentage_per_day_clean)

#PREPROCESSING
null_imputer = SimpleImputer(strategy="constant", fill_value=None)

raw_pipeline = make_pipeline(
    null_imputer,
    FunctionTransformer(lambda X: X),
    #FunctionTransformer(),
    MinMaxScaler()
)

log_pipeline = make_pipeline(
    null_imputer,
    FunctionTransformer(np.log),
    #StandardScaler()
    MinMaxScaler()
)

preprocessing = ColumnTransformer([
        ("raw", raw_pipeline, ['var_day']),
        ("log", log_pipeline, ['adj_close','open', 'high', 'low', 'volume']),
    ],
    remainder="passthrough")

#PRINT preprocessing
X_preprocessing = preprocessing.fit_transform(df_clean_filter)
print(X_preprocessing)

df_preprocessing=pd.DataFrame(X_preprocessing)

# Guardar el DataFrame df_preprocessing en un archivo Excel
excel_file_path = os.path.join(path_base, folder_functional, "df_preprocessing.xlsx")
df_preprocessing.to_excel(excel_file_path, index=False)
print(f'DataFrame df_preprocessing guardado en: {excel_file_path}')