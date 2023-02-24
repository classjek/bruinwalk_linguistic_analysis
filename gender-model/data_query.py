from google.cloud import bigquery
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

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../../priv/gender-model-006f0132749e.json"

client = bigquery.Client()

query = f"""
    SELECT name, gender
    FROM `bigquery-public-data.usa_names.usa_1910_current` 
    LIMIT 1000
"""

query_job = client.query(query)
df = query_job.to_dataframe()

print(df.head(5))

######PREPROCESSING DATA##########
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

processed_df = preprocess(df)
print(processed_df.head())

######LSTM MODEL##########
def lstm_model(num_alphabets=27, name_length=50, embedding_dim=256):
    model = Sequential([
        Embedding(num_alphabets, embedding_dim, input_length=name_length),
        Bidirectional(LSTM(units=128, recurrent_dropout=0.2, dropout=0.2)),
        Dense(1, activation="sigmoid")
    ])

    model.compile(loss='binary_crossentropy',
                  optimizer=Adam(learning_rate=0.001),
                  metrics=['accuracy'])

    return model

#######TRAIN MODEL###########
model = lstm_model(num_alphabets=27, name_length=50, embedding_dim=256)

X = np.asarray(processed_df['name'].values.tolist())
y = np.asarray(processed_df['gender'].values.tolist())

X_train, X_test, y_train, y_test = train_test_split(X,
                                                    y,
                                                    test_size=0.2,
                                                    random_state=0)

callbacks = [
    EarlyStopping(monitor='val_accuracy',
                  min_delta=1e-3,
                  patience=5,
                  mode='max',
                  restore_best_weights=True,
                  verbose=1),
]

history = model.fit(x=X_train,
                    y=y_train,
                    batch_size=64,
                    epochs=50,
                    validation_data=(X_test, y_test),
                    callbacks=callbacks)

model.save('boyorgirl.h5')

# plt.plot(history.history['accuracy'], label='train', resize=False)
# plt.plot(history.history['val_accuracy'], label='val', resize=False)
# plt.xlabel('Epochs')
# plt.ylabel('Accuracy')
# plt.legend()


########MAIN###########
pred_model = load_model('boyorgirl.h5')

# Input names
names = ['Joe', 'Biden', 'Kamala', 'Harris']

# Convert to dataframe
pred_df = pd.DataFrame({'name': names})

# Preprocess
pred_df = preprocess(pred_df, train=False)

# Predictions
result = pred_model.predict(np.asarray(
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