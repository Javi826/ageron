# modulos/mod_dtset_stdcs.py

import pandas as pd
import os
import time
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from modules.mod_dtset_clean import mod_dtset_clean
from paths.paths import csv_folder, path_base,folder,archivo,path_absolut
import warnings

# IGNORE WARNINGS
warnings.filterwarnings("ignore")


#VISUALIZATION PRINTS
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)

# reading file w/o first row(header)
df_data = pd.read_csv(path_absolut, header=None, skiprows=1, names=['date','open','high','low','close','adj_close','volume'])
df_clean = mod_dtset_clean(df_data)


# numeric columns select
columns_numeric = df_clean.select_dtypes(include=['float', 'int']).columns

# Pearson + Sort ascdending
pearsons = df_clean[columns_numeric].corrwith(df_clean['close'], method='pearson').sort_values(ascending=False)

#print(pearsons)

def filter_data_by_date_range(df, start_date, end_date):
    return df[(df['date'] >= start_date) & (df['date'] <= end_date)]

# choose range
start_date = '2005-01-01'
end_date = '2006-01-02'

# filtering data by date
df_clean = filter_data_by_date_range(df_clean, start_date, end_date)

#print("Primera fila:")
#print(df_clean.head(1))
#print(df_clean.tail(1))

# Conteo de registros entre start_date y end_date
conteo_registros = df_clean.shape[0]

#print(f"El número de registros entre {start_date} y {end_date} es: {conteo_registros}")

#SMA window n days
df_clean['SMA_n'] = df_clean['close'].rolling(window=30).mean()

# differenciation m days
df_clean['diff_tn'] = df_clean['close'].diff(30)

MAE_naive = df_clean['close'].diff(30).mean()
EPAM_naive = (df_clean['close'].diff(30)/df_clean['close']).abs().mean()*100
#print('MAE_naive:', MAE_naive)
#print('EPAM_naive', EPAM_naive)

# Calcula el valor estimado y agrégalo como una nueva columna 'estimated_value'
df_clean['naive_value'] = df_clean['close'] + MAE_naive

# Print only the last 5 values with the columns 'date', 'close', and 'estimated_value'
#print(df_clean[['date', 'close', 'naive_value']].tail(5))


#ARIMA----------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------------------------------------


# Define the values for the parameters p, d, and q you want to try
p_values = [1]
d_values = [0]
q_values = [1]

# Other parameters
seasonal_order = (0, 1, 1, 30)  # You can adjust according to your needs

# Filter and adjust the time series (you can reuse this code)
df_series = df_clean.set_index('date')
df_series = df_series.loc[start_date:end_date]['close'].asfreq('D')

# Loop to try different values of p, d, and q
for p in p_values:
    for d in d_values:
        for q in q_values:
            # Fit the ARIMA model
            model = ARIMA(df_series, order=(p, d, q), seasonal_order=seasonal_order)
            model_fit = model.fit()

            # Get the forecast for the next period
            y_close = model_fit.forecast()
            forecasted_value = y_close[0]

            # Compare the results with the real values
            df_clean_full = mod_dtset_clean(df_data)
            df_clean_full['forecasted_value'] = forecasted_value
            df_clean_full['delta_close-forecasted'] = df_clean_full['close'] - df_clean_full['forecasted_value']
            df_clean_full['%_forecasted'] = (df_clean_full['delta_close-forecasted'] / df_clean_full['close']) * 100

            # Filter records from the date following end_date (including end_date)
            records_post_end_date = df_clean_full[df_clean_full['date'] >= end_date].iloc[1:2]

            # Print the results
            columns_to_print = ['date', 'close', 'forecasted_value', 'delta_close-forecasted', '%_forecasted']
            print(f"\nResults for p={p}, d={d}, q={q}")
            print(records_post_end_date[columns_to_print])
            print(model_fit.summary())


# Graficar la serie temporal con la media móvil y la diferenciación
plt.figure(figsize=(10, 6))
plt.plot(df_clean['date'], df_clean['close'], label='Close Price')
plt.plot(df_clean['date'], df_clean['SMA_n'], label='SMA n days', linestyle='--', color='orange')  # Agrega la media móvil al gráfico
plt.plot(df_clean['date'], df_clean['diff_tn'], label='diff t-n', linestyle=':', color='green')  # Agrega la diferenciación al gráfico
plt.title('Date vs Close Price with SMA and Difference t-n')
plt.xlabel('Date')
plt.ylabel('Values')
plt.legend()
plt.grid(True)
plt.show()


