import os

from keras.models import Sequential
from keras.layers import Embedding, Bidirectional, LSTM, Dense
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping
from keras.models import load_model

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split

def preprocess(names_df, train=True):
    names_df['name'] = names_df['name'].str.lower()

    names_df['name'] = [list(name) for name in names_df['name']]

    name_length = 50
    names_df['name'] = [
        (name + [' ']*name_length)[:name_length] 
        for name in names_df['name']
    ]

    names_df['name'] = [
        [
            max(0.0, ord(char)-96.0) 
            for char in name
        ]
        for name in names_df['name']
    ]
    
    if train:
        names_df['gender'] = [
            0.0 if gender=='F' else 1.0 
            for gender in names_df['gender']
        ]
    
    return names_df

model = load_model('boyorgirl-100.h5')

# Input names
names = ['Joe', 'Karen', 'Jeff', 'Catherine']

# Convert to dataframe
pred_df = pd.DataFrame({'name': names})

# Preprocess
pred_df = preprocess(pred_df, train=False)

# Predictions
result = model.predict(np.asarray(
    pred_df['name'].values.tolist())).squeeze(axis=1)

pred_df['Boy or Girl?'] = [
    'Boy' if logit > 0.5 else 'Girl' for logit in result
]

pred_df['Probability'] = [
    logit if logit > 0.5 else 1.0 - logit for logit in result
]

# Format the output
pred_df['name'] = names
pred_df.rename(columns={'name': 'Name'}, inplace=True)
pred_df['Probability'] = pred_df['Probability'].round(2)
pred_df.drop_duplicates(inplace=True)

print(pred_df.head())