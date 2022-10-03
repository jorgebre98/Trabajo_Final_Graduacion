# # ************************************************************* #
# #               Copyright (C) 2022 Jorge Brenes Alfaro.
# #               EL5617 Trabajo Final de Graduación.
# #               Escuela de Ingeniería Electrónica.
# #               Tecnológico de Costa Rica.
# # ************************************************************* #

#   This file is responsible for generating the mimetic neural network (MNN). First, the data
#   collected from the PAHM is processed, which is reshaped as necessary for the network.
#   Next, the model is developed using recurrent neural networks (RNN), specifically the GRU.

#Libraries to proccess data
import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Libraries to create RNAM
from tensorflow.keras.models import Sequential
from tensorflow.keras.backend import clear_session
from tensorflow.keras.optimizers import RMSprop, Adam
from tensorflow.keras.layers import Dense, Dropout, GRU, TimeDistributed

import warnings
warnings.filterwarnings('ignore')

import wandb
from wandb.keras import WandbCallback

wandb login('52c82ce2e50072d968a0a256c901929128147287')
wandb.init(project="Prueba", 
           entity="mimetic-rna", 
           name='Probando W&B',
           resume='Allow', 
           id='Probando W&B')
wandb.config = {
    "epochs": 500,
    "batch_size": 8,
    "learning_rate":0.001,
    "window": 100
}

#   ******************* Process the Dataset *******************
root = '/Users/jorge/Documents/TEC/TFG/Datos_Recolectados/'

root = '/Users/jorge/Documents/TEC/TFG/Datos_Recolectados/'
Dir = os.listdir(root)
pwm = np.array([])
angle = np.array([])

# Read all the .csv files and make an nx4 array
# Next, separate the pwm value and angle in their respective arrays.
print('******************* Process the Dataset *******************',flush=True)
print('Recolecting Data',flush=True)
for filename in Dir:
    files = pd.read_csv(root+filename)
    pwm = np.append(pwm, np.concatenate((np.zeros(100),files.values[:,2])))
    angle = np.append(angle, np.concatenate((np.zeros(100),files.values[:,3])))

X_train = []
Y_train = []
window = wandb.config['window']

#For each element of training set, we have "window" previous training set elements
print('Accommodating data for the GRU network',flush=True)
for i in range(window,pwm.shape[0]):
    X_train.append(pwm[i-window:i])
    Y_train.append(angle[i])
X_train, Y_train = np.array(X_train), np.array(Y_train) # Input and output arrays

# Separate the values in train, validation and test data/label
train_data, val_data, test_data = [],[],[]
train_label, val_label, test_label = [],[],[]
train_lenght = int(len(X_train)*3/5)
val_lenght = int(len(X_train)*4/5)

# Use 3/5 of the total data set for training 
# and 1/5 for validation and testing.
print('Separating data in training, validation and testing',flush=True)
for i,j in zip(X_train[:train_lenght],Y_train[:train_lenght]):
    train_data.append(i)
    train_label.append(j)

for i,j in zip(X_train[train_lenght:val_lenght],Y_train[train_lenght:val_lenght]):
    val_data.append(i)
    val_label.append(j)
    
for i,j in zip(X_train[val_lenght:],Y_train[val_lenght:]):
    test_data.append(i)
    test_label.append(j)
    
train_data, val_data, test_data = np.array(train_data), np.array(val_data), np.array(test_data)
train_label, val_label, test_label = np.array(train_label), np.array(val_label), np.array(test_label)

print('El total de datos de entrenamiento es: ', len(train_data), flush=True)
print('El total de datos de validación es: ', len(val_data), flush=True)
print('El total de datos de prueba es: ', len(test_data), flush=True)

# Reshape the arrays (n,window,1). Where n is the total amount of data in the array
print('Reshape arrays to tensors',flush=True)
train_data = np.reshape(train_data,(train_data.shape[0],train_data.shape[1],1))
val_data = np.reshape(val_data,(val_data.shape[0],val_data.shape[1],1))
test_data = np.reshape(test_data,(test_data.shape[0],test_data.shape[1],1))
print('******************* Finish *******************',flush=True)

#   ******************* Neural Network *******************
#   Model creation

clear_session()
model = Sequential()
model.add(GRU(64, input_shape=(X_train.shape[1],1),return_sequences=True))
model.add(Dropout(0.35))
model.add(GRU(64, input_shape=(X_train.shape[1],1),return_sequences=True))
model.add(Dropout(0.35))
model.add(TimeDistributed(Dense(1))) # There is no difference between this and model.add(Dense(1))...
model.compile(optimizer=Adam(learning_rate=0.001), loss='mean_squared_error', metrics=['mse','acc'])
model.summary()

#   Model Training
history = model.fit(train_data, train_label,
                    epochs=500, batch_size=8,
                    validation_data = (val_data,val_label),
                    verbose=2,
                    callbacks=[WandbCallback()]
                    )
#   Prediction
testPredict = model.predict(test_data)

#   Model Evaluate
#loss, accuracy = model.evaluate(testX,output_test)

#   Save the model
joblib.dump(model, 'GRU_model.joblib')

#   Plot the predicted and "true" output and plot training and validation losses
loss=history.history['loss']
val_loss=history.history['val_loss']
epochs=range(1,len(loss)+1)
plt.figure()
plt.plot(epochs, loss,'b', label='Training loss')
plt.plot(epochs, val_loss,'r', label='Validation loss')
plt.title('Training and validation losses')
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.xscale('log')
plt.legend()
plt.show()
