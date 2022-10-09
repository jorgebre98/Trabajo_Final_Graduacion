# Libraries
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#Libraries to create de RNAM
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, GRU
from tensorflow.keras.optimizers import Adam, RMSprop

import wandb
from wandb.keras import WandbCallback

wandb.login()

wandb.init(project="RNAM Real", 
           entity="mimetic-rna", 
           name='RNAM Real 1',
           resume='Allow', 
           id='RNAM Real 1')
wandb.config = {
    "epochs": 3500,
    "batch_size": 1,
    "units": 32,
    "learning_rate":0.001,
    "Dropout": 0.2
}

def plot_loss (history):
    plt.figure(figsize = (10, 6))
    plt.plot(history.history['loss'], label='Train loss')
    plt.plot(history.history['val_loss'], label='Validation loss')
    plt.title('Model Train vs Validation Loss for GRU network')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(loc='upper right')

def plot_future(prediction, y_test):
    plt.figure(figsize=(10, 6))
    range_future = np.arange(prediction.shape[1])
    plt.plot(range_future, y_test[0,:], label='Test data', color = [1, 0.502, 0])
    plt.plot(range_future, prediction[0,:], label='Prediction',  color = [0.0502, 0.706, 0.949])
    plt.title('Predicted and true output')
    plt.xlabel('Tiempo (ms)')
    plt.ylabel('Ángulo (°)')
    plt.legend(loc='lower right')
    
def evaluate_prediction(predictions, actual):
    errors = predictions - actual
    mse = np.square(errors).mean()
    rmse = np.sqrt(mse)
    mae = np.abs(errors).mean()
    print('GRU:')
    print('Mean Absolute Error: {:.4f}'.format(mae))
    print('Root Mean Square Error: {:.4f}'.format(rmse))

def separate_values(X_train, Y_train):
    train_data, val_data, test_data = [],[],[]
    train_label, val_label, test_label = [],[],[]
    train_lenght = int(len(X_train)*3/5)
    val_lenght = int(len(X_train)*4/5)
    
    # Use 3/5 of the total data set for training
    # and 1/5 for validation and testing.
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
    
    return train_data, train_label, val_data, val_label, test_data, test_label

root = '../Datos_Recolectados/'
Dir = os.listdir(root)
pwm = np.array([])
angle = np.array([])

print('******************* Process the Dataset *******************',flush=True)
print('Recolecting Data',flush=True)
for filename in Dir:
    files = pd.read_csv(root+filename)
    pwm = np.append(pwm, np.concatenate((np.zeros(100),files.values[:,2])))
    angle = np.append(angle, np.concatenate((np.zeros(100),files.values[:,3])))

train_data, train_label, val_data, val_label, test_data, test_label = separate_values(pwm,angle)

# ***************** Create the training data *****************
input_seq_train = train_data # Input sequence for the simulation

train_label = np.reshape(train_label, (1,train_label.shape[0]))
y_train = np.reshape(train_label.T, (1, train_label.T.shape[0], 1)) # Label train data

input_seq_train = np.reshape(input_seq_train,(input_seq_train.shape[0], 1))
tmp_train = np.concatenate((input_seq_train, np.zeros(shape = (input_seq_train.shape[0], 1))), axis=1)
X_train= np.reshape(tmp_train, (1, tmp_train.shape[0], tmp_train.shape[1])) # Train Data

# ***************** Create the training data *****************
input_seq_val = val_data # Input sequence for the simulation

val_label = np.reshape(val_label, (1,val_label.shape[0]))
y_val = np.reshape(val_label.T, (1, val_label.T.shape[0], 1)) # Label train data

input_seq_val = np.reshape(input_seq_val,(input_seq_val.shape[0], 1))
tmp_val = np.concatenate((input_seq_val, np.zeros(shape = (input_seq_val.shape[0], 1))), axis=1)
X_val = np.reshape(tmp_val, (1, tmp_val.shape[0], tmp_val.shape[1])) # Train Data

# ***************** Create the training data *****************
input_seq_test = test_data # Input sequence for the simulation

test_label = np.reshape(test_label, (1,test_label.shape[0]))
y_test = np.reshape(test_label.T, (1, test_label.T.shape[0], 1)) # Label train data

input_seq_test = np.reshape(input_seq_test,(input_seq_test.shape[0], 1))
tmp_test = np.concatenate((input_seq_test, np.zeros(shape=(input_seq_test.shape[0], 1))), axis=1)
X_test = np.reshape(tmp_test, (1, tmp_test.shape[0], tmp_test.shape[1])) # Train Data

print('Total train data is: ', len(train_data), flush=True)
print('Total validation data is: ', len(val_data), flush=True)
print('Total testing data is:: ', len(test_data), flush=True)

print('\nTrain data shape is: ', X_train.shape, flush=True)
print('Validation data shape is: ', X_val.shape, flush=True)
print('Testing data shape is:: ', X_test.shape, flush=True)
print('Train label shape is: ', y_train.shape, flush=True)
print('Validation label shape is: ', y_val.shape, flush=True)
print('Testing label shape is:: ', y_test.shape, flush=True)
print('******************* Finish *******************',flush=True)

# ***************** Neuronal Network *****************
# Model Creation
model=Sequential()
model.add(GRU(units = wandb.config['units'], input_shape=(None, X_train.shape[2]), return_sequences=True))
model.add(Dense(1))
# Compile model
model.compile(optimizer = RMSprop(learning_rate = wandb.config['learning_rate']), 
              loss = 'mean_squared_error', metrics = ['mse'])
model.summary()

history = model.fit(X_train, y_train ,
                    epochs = wandb.config['epochs'], batch_size = wandb.config['batch_size'], 
                    validation_data = (X_val, y_val),
                    verbose = 1, callbacks=[WandbCallback(save_model=False)])
model.save('RNAM_real.h5')


# Model Prediction
testPredict = model.predict(X_test)

# Model Evaluate
plot_loss(history)
plot_future(testPredict,y_test)
evaluate_prediction(testPredict, y_test)

