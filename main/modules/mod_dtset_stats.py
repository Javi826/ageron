# modulos/mod_dtset_stdcs.py

import pandas as pd
import os
import time
import matplotlib.pyplot as plt
import warnings
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.model_selection import train_test_split
from modules.mod_dtset_clean import mod_dtset_clean
from paths.paths import csv_folder, path_base,folder,archivo,path_absolut


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
start_date = '2000-01-01'
end_date = '2020-12-31'

# filtering data by date
df_clean = filter_data_by_date_range(df_clean, start_date, end_date)

#print("Primera fila:")
#print(df_clean.head(1))
#print(df_clean.tail(1))

#SUMARY
summary_stats_all = df_clean.describe(include='all')
print(summary_stats_all)

#HISTOGRAM
# Seleccionar columnas de interés
columns_of_interest = ['close', 'var_day', 'volume','day_week']

# Configurar la figura
fig, axes = plt.subplots(nrows=1, ncols=len(columns_of_interest), figsize=(15, 5))

# Generar histogramas para cada columna
for i, column in enumerate(columns_of_interest):
    axes[i].hist(df_clean[column], bins=30, color='skyblue', edgecolor='black')
    axes[i].set_title(f'Histograma de {column}')
    axes[i].set_xlabel(column)
    axes[i].set_ylabel('Frecuencia')

# Ajustar el diseño
plt.tight_layout()
plt.show()

#TRAIN AND TEST DATA

def shuffle_and_split_data(data, test_ratio=0.2):
    np.random.seed(42)  
    shuffled_indices = np.random.permutation(len(data))
    test_set_size = int(len(data) * test_ratio)
    test_indices = shuffled_indices[:test_set_size]
    train_indices = shuffled_indices[test_set_size:]
    train_set = data.iloc[train_indices]
    test_set = data.iloc[test_indices]

    return data.iloc[train_indices], data.iloc[test_indices]

train_set, test_set = shuffle_and_split_data(df_clean)


print("Número de registros en train_set:", len(train_set))
print("Número de registros en test_set:", len(test_set))

train_set, test_set = train_test_split(df_clean, test_size=0.2,random_state=42)

print("Número de registros en train_set:", len(train_set))
print("Número de registros en test_set:", len(test_set))

# Ahora puedes imprimir train_indices
#print(train_set)
#print(train_set)

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




# PLOT
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


