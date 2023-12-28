# modules/mod_dtset_splits.py

import tensorflow as tf
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from tensorflow.keras import layers, models, initializers
from modules.mod_dtset_clean import mod_dtset_clean
import time
import os
import pandas as pd

def mod_dtset_slpits(df_data):
    
    