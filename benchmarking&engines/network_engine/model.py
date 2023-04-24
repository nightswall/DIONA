import os
import tensorflow as tf
from tensorflow import keras

class Model():
  def create_model(__self__, input_dim, checkpoint_path):
    model = tf.keras.models.Sequential()
    model.add(tf.keras.layers.Dense(
              50, 
              input_dim = input_dim, 
              kernel_initializer = 'normal', 
              activation = 'relu'))
    model.add(tf.keras.layers.Dense(
              30, 
              input_dim = input_dim, 
              kernel_initializer = 'normal', 
              activation = 'relu'))
    model.add(tf.keras.layers.Dense(
              20, 
              kernel_initializer = 'normal'))
    model.add(tf.keras.layers.Dense(
              6,
              activation = 'softmax'))
    model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    # Code below will help us to quit training when decrease in
    # validation loss happens more than 5 times. Model is either
    # overfitting or underfitting in this case. So, continueing the
    # training is pointless.
    monitor = tf.keras.callbacks.EarlyStopping(
              monitor = 'val_loss',
              min_delta = 1e-3,
              patience = 5,
              verbose = 1,
              mode = 'auto')
    # Code below will help us to save trained models and use them afterwards.
    checkpoint_dir = os.path.dirname(checkpoint_path)
    checkpoint = tf.keras.callbacks.ModelCheckpoint(
                filepath = checkpoint_path,
                save_weights_only = True,
                verbose = 2)
    return model, [monitor, checkpoint];

  def load_model(__self__, model, checkpoint_path):
    model.load_weights(checkpoint_path)
    return model
