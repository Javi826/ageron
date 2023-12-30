#MODULE SUMMARY STATS
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
start_date = '2001-01-01'
end_date = '2014-12-31'

# filtering data by date
df_clean_filter = filter_data_by_date_range(df_data_clean, start_date, end_date)

#print("Primera fila:")
#print(df_clean_filter.head(1))
#print(df_clean_filter.tail(1))

df_clean_filter['date'] = pd.to_datetime(df_clean_filter['date'])
#df_clean_filter['date'] = df_clean_filter['date'].dt.strftime('%Y-%m-%d')
#df_clean_filter['year'] = df_clean_filter['date'].dt.strftime('%Y')

# PLOT
plt.figure(figsize=(10, 6))
plt.plot(df_clean_filter['date'], df_clean_filter['close'], label='Close Price')
plt.title('Year vs Close Price with SMA and Difference t-n')
plt.xlabel('Year')
plt.ylabel('Values')
plt.legend()
plt.grid(True)
plt.show()

#SUMARY
summary_stats_all = df_clean_filter.describe(include='all')
print(summary_stats_all)

#HISTOGRAM
# Select columns
columns_of_interest = ['close', 'var_day', 'volume','day_week','high','low','adj_close']

# plot
fig, axes = plt.subplots(nrows=1, ncols=len(columns_of_interest), figsize=(15, 5))

# Columns
for i, column in enumerate(columns_of_interest):
    axes[i].hist(df_clean_filter[column], bins=30, color='skyblue', edgecolor='black')
    axes[i].set_title(f'Histogram de {column}')
    axes[i].set_xlabel(column)
    axes[i].set_ylabel('frequency')

# design
plt.tight_layout()
plt.show()


#PEARSONS
# numeric columns select
columns_numeric = df_clean_filter.select_dtypes(include=['float', 'int']).columns

# Pearson + Sort ascdending
pearsons = df_clean_filter[columns_numeric].corrwith(df_data_clean['close'], method='pearson').sort_values(ascending=False)

print(pearsons)