# -*- coding: utf-8 -*-
"""Model NLP dengan TensorFlow

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1URYv-Vu9oksM1WlQqX7Qe1nPLg20Z_Ya

Dataset Kaggle : https://www.kaggle.com/datasets/praveengovi/emotions-dataset-for-nlp
"""

import numpy as np
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import accuracy_score
import tensorflow as tf
import pandas as pd
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from sklearn.model_selection import train_test_split

df = pd.read_csv("/content/drive/MyDrive/Dataset/Question_Classification_Dataset.csv")
df = df.drop(columns=['Unnamed: 0', 'Category1', 'Category2'])

df.head()

df = df.drop(df[df['Category0'] == 'ENTITY'].index)
df = df.drop(df[df['Category0'] == 'ABBREVIATION'].index)

model_category = pd.get_dummies(df.Category0)
new_ds         = pd.concat([df,model_category], axis=1)
new_ds         = new_ds.drop(columns='Category0')
new_ds

X_column  = new_ds['Questions'].astype(str)
Y_column  = new_ds[['DESCRIPTION','LOCATION','HUMAN','NUMERIC']]

X_train, X_test, y_train, y_test = train_test_split(X_column,Y_column,test_size=0.2)

getTokenizer = Tokenizer(num_words=5000, oov_token='x')
getTokenizer.fit_on_texts(X_train)
getTokenizer.fit_on_texts(X_test)

A_train      = getTokenizer.texts_to_sequences(X_train)
A_test        = getTokenizer.texts_to_sequences(X_test)

B_train      = pad_sequences(A_train)
B_test       = pad_sequences(A_test)

model_ = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=5000, output_dim=16),
    tf.keras.layers.LSTM(128),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.75),
    tf.keras.layers.Dense(64,activation='relu'),
    tf.keras.layers.Dropout(0.75),
    tf.keras.layers.Dense(4,activation='softmax')
])


model_.compile(loss='categorical_crossentropy',optimizer='adam',metrics=['accuracy'])

class myCallback(tf.keras.callbacks.Callback):
  def on_epoch_end(self,epoch,logs={}):
    if(logs.get('val_accuracy') > 0.9):
      print("\n Akurasi lebih dari 90%")
      self.model.stop_training = True

callbacks = myCallback()

num_of_epochs = 30

history_ = model_.fit(B_train, y_train, epochs=num_of_epochs, callbacks=[callbacks], validation_data=(B_test, y_test), verbose=2)

import matplotlib.pyplot as plt
plt.plot(history_.history['accuracy'])
plt.plot(history_.history['val_accuracy'])
plt.title('Model Akurasi')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train','test'], loc='upper left')
plt.show()

plt.plot(history_.history['loss'])
plt.plot(history_.history['val_loss'])
plt.title('Model Loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train','test'], loc='upper left')
plt.show()