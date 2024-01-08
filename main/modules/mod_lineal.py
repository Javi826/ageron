# -*- coding: utf-8 -*-
"""
Created on Sun Jan  7 10:03:49 2024
@author: javier
"""
from modules.mod_init import *
from functions.def_functions import *
from paths.paths import *
from columns.columns import *

# READING file
df_preprocessing = pd.read_excel(path_preprocessing, header=None, skiprows=1, names=columns_preprocessing)
#print(df_preprocessing.head(5))

# Lista de valores de n
#n_values = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]
n_values = [1, 2, 3]
mse_values = []  # Almacenar MSE para cada valor de n

for n in n_values:
    for col in ['pipe_open', 'pipe_high', 'pipe_low', 'pipe_var_day', 'pipe_volume']:
        for i in range(1, n + 1):
            df_preprocessing[f'{col}_lag_{i}'] = df_preprocessing[col].shift(i)

    # Eliminar filas con valores nulos resultantes de los desplazamientos
    df_preprocessing = df_preprocessing.dropna()

    # SELECT x & y
    predictors = [f'{col}_lag_{i}' for col in ['pipe_open', 'pipe_high', 'pipe_low', 'pipe_var_day', 'pipe_volume'] for i in range(1, n + 1)]
    x = df_preprocessing[predictors]
    y = df_preprocessing['close']

    # SPLIT data
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    # INIT & FIT Model
    model = LinearRegression()
    model.fit(x_train, y_train)
    y_pred = model.predict(x_test)
    mse = mean_squared_error(y_test, y_pred)

    # Almacenar MSE para cada valor de n
    mse_values.append(mse)

    # Imprimir el MSE para cada valor de n
    #print(f'Mean Squared Error for n={n}: {mse}')

# Ordenar las listas de n y mse por el valor de mse
sorted_data = sorted(zip(n_values, mse_values), key=lambda x: x[1], reverse=False)
n_values_sorted, mse_values_sorted = zip(*sorted_data)


# Imprimir los MSE ordenados de mayor a menor
print('\nMean Squared Error (MSE) Ordered from Highest to Lowest:')
for n, mse in sorted_data:
    print(f'n={n}: {mse}')

    # Imprimir y_pred, y_test, la fecha correspondiente y la diferencia
    print('\nResults for n={n}:')
    
    for index, (pred_value, actual_value) in enumerate(zip(y_pred, y_test.values)):
        date = df_preprocessing.iloc[x_test.index[index]]['date']
        print(f'Date: {date}, Predicted Value: {pred_value}, Actual Value: {actual_value}, Difference: {pred_value - actual_value}')