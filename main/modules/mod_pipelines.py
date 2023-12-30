#MOD_PIPELINES
"""
Created on Sat Dec 30 21:06:19 2023
@author: jlahoz
"""

from modules.mod_init import *

# READING file w/o first row(header)
df_data_clean = pd.read_csv(path_df_data_clean, header=None, skiprows=1, names=columns_clean)
print(df_data_clean.head(5))

def filter_data_by_date_range(df, start_date, end_date):
    return df[(df['date'] >= start_date) & (df['date'] <= end_date)]

# choose range
start_date = '2003-01-01'
end_date = '2015-12-31'

# filtering data by date
df_clean_filter = filter_data_by_date_range(df_data_clean, start_date, end_date)

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

# SAVE in excel
df_preprocessing.to_excel(folder_functional,file_preprocessing, index=False)