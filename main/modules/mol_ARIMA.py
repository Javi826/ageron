# -*- coding: utf-8 -*-
"""
Created on Fri Dec 29 14:05:43 2023

@author: jlaho
"""

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