# ************************************************************************************************************************* #
#                                           Copyright (C) 2022 Jorge Brenes Alfaro.
#                                           EL5617 Trabajo Final de Graduación.
#                                           Escuela de Ingeniería Electrónica.
#                                           Tecnológico de Costa Rica.
# *************************************************************************************************************************** #
#
#   This file contains the mimetic neural network (MNN) that uses the empirical mathematical
#   model of the PAHM.
#
#   The data used for training, validation and testing are randomly generated, while their
#   labels (angles) are generated by mathematical model. The angle values are normalized
#   between -1 and 1 for better network performance, the data are prepared in the form of
#   tensor, necessary for the GRU layer. Finally, the network model is developed, training,
#   prediction and evaluation of the model are performed.

#   The presen code is based in H. Kapasi, 2022. "Modeling Non-Linear Dynamic Systems with Neural Networks", 2022. [Online].
#   Available in: https://towardsdatascience.com/modeling-non-linear-dynamic-systems-with-neural-networks-f3761bc92649.


# Libraries to process data
import argparse
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv

#Libraries to create de MNN
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.optimizers import RMSprop, Adam
from tensorflow.keras.layers import Dense, GRU

import wandb
from wandb.keras import WandbCallback

parser = argparse.ArgumentParser(description = 'Mimetic Neural Network for the mathematical model.')
parser.add_argument('--project_name', type = str, default = 'RNAM_', help = 'Name of the run.')
parser.add_argument('--units', type = int, default = 32, help = 'Number of the units for the RNAM.')
parser.add_argument('--epochs', type = int, default = 1000, help = 'Number of epochs for the train.')
parser.add_argument('--batch_size', type = int, default = 1, help = 'Number of batch for the train.')
parser.add_argument('--loss_name', type = str, default = 'loss_',  help = 'RNAM.py')
parser.add_argument('--predict_name', type = str, default = 'Prediction_',  help = 'Name for the figure of the prediction (.png).')
parser.add_argument('--model_name', type = str, default = 'Model_Synth_', help = 'Name for the RNAM model (.h5).')
parser.add_argument('--loss_type', type = str, default = 'mse', help = 'Choose a loss, mse or mae')
parser.add_argument('--load_model', type = str, default = '', help = 'Load a previously trained model (.h5).')
args = parser.parse_args()

#   The parameters are archived in Weights and Biases (W&B), as well as the results of the
#   execution for further evaluation.
wandb.login()

wandb.init(project = "Synthetic PAHM", 
           entity = "mimetic-rna", 
           name = args.project_name,
           resume = 'Allow',
           #notes = 'Prueba básica de la sintetica',
           id = args.project_name)
wandb.config = {
    "epochs": args.epochs,
    "batch_size": args.batch_size,
    "units": args.units,
    "learning_rate":0.001,
}

#   Function to discrete the PAHM's dynamic.
#   Discretize by backward euler method.
def dynamic_model(A,B,C,cond_initial,input_sequence, time_steps,h):
    I = np.identity(A.shape[0])
    Ad = inv(I - h*A)
    Bd = Ad*h*B
    Xd = np.zeros(shape=(A.shape[0],time_steps + 1)) #  Vectors 2 x n / Input in discrete time.
    Yd = np.zeros(shape=(C.shape[0],time_steps + 1)) #  Vectors 1 x n / Output in discrete time.
    
    for i in range(0,time_steps):
        if i==0:
            Xd[:,[i]] = cond_initial
            Yd[:,[i]] = C*cond_initial
            x = Ad*cond_initial + Bd*input_sequence[i]
        else:
            Xd[:,[i]] = x
            Yd[:,[i]] = C*x
            x = Ad*x + Bd*input_sequence[i] # Discrete time representation
            
    Xd[:,[-1]] = x
    Yd[:,[-1]] = C*x
    return Xd, Yd

#   This function is used to normalized values.
def normalizer(angle, action):
    min_val, max_val = -120, 120
    if action == 'norm':
        return (angle - min_val)/(max_val - min_val)
    else:
        return angle*(max_val - min_val)+min_val

#   This function plots training loss vs validation loss. 
def plot_loss (history):
    plt.figure(figsize = (10, 6))
    plt.plot(history.history['loss'], label='Train loss')
    plt.plot(history.history['val_loss'], label='Validation loss')
    plt.title('Model Train vs Validation Loss for GRU network')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(loc='upper right')
    plt.savefig(args.loss_name)

#   This function plots the actual output vs the output predicted by the model. 
def plot_future(prediction, y_test):
    plt.figure(figsize=(10, 6))
    range_future = np.arange(prediction.shape[1])
    plt.plot(range_future, y_test[0,:], label='Test data', color = [1, 0.502, 0])
    plt.plot(range_future, prediction[0,:], label='Prediction',  color = [0.0502, 0.706, 0.949])
    plt.title('Predicted and true output')
    plt.xlabel('Tiempo (ms)')
    plt.ylabel('Ángulo (°)')
    plt.legend(loc='lower right')
    plt.savefig(args.predict_name)
    
#   This function calculates performance metrics for regression problems.    
def evaluate_prediction(predictions, actual):
    errors = predictions - actual
    mse = np.square(errors).mean()
    rmse = np.sqrt(mse)
    mae = np.abs(errors).mean()
    print('GRU:')
    print('Mean Absolute Error: {:.4f}'.format(mae))
    print('Mean Square Error: {:.4f}.'.format(mse))
    print('Root Mean Square Error: {:.4f}'.format(rmse))

#   Definition of the model in continuous time.
#   A,B,C               - continuous time system matrices 
#   x0_                   - the initial state of the system 
#   time                 - the total number of simulation time steps 
#   sampling          - the sampling period for the backward Euler discretization
#   input_seq         - Input sequence

A = np.matrix([[0, 1],[-17.97, -0.3801]])
B = np.matrix([[0],[2965]])
C = np.matrix([[1, 0]])
time = 2000
sampling = 0.02

print('******************* Creating the Dataset *******************', flush=True)
# ***************** Create the training data *****************
input_seq_train = np.concatenate((np.zeros(shape=(250,1)),np.random.rand(time,1)*0.25))
x0_train = np.zeros(shape=(2,1)) # Initial state for simulation

state, train_label = dynamic_model(A, B, C,
                                   x0_train, input_seq_train, input_seq_train.shape[0], sampling) # Simulate the dynamics 

train_label = np.reshape(train_label.T, (1, train_label.T.shape[0], 1)) # Label train data

input_seq_train = np.reshape(input_seq_train,(input_seq_train.shape[0], 1))
tmp_train = np.concatenate((input_seq_train, np.zeros(shape = (input_seq_train.shape[0], 1))), axis=1)
tmp_train = np.concatenate((x0_train.T,tmp_train), axis = 0)
train_data = np.reshape(tmp_train, (1, tmp_train.shape[0], tmp_train.shape[1])) # Train Data

# ***************** Create the validation data *****************
time = 400
input_seq_val = np.concatenate((np.zeros(shape=(250,1)),np.random.rand(time,1)*0.25))
x0_val = np.zeros(shape=(2,1))

state_val, val_label = dynamic_model(A, B, C,
                                     x0_val, input_seq_val, 
                                     input_seq_val.shape[0], sampling) 

val_label = np.reshape(val_label.T,(1,val_label.T.shape[0],1)) # Label validation data

input_seq_val = np.reshape(input_seq_val,(input_seq_val.shape[0],1))
tmp_val = np.concatenate((input_seq_val, np.zeros(shape = (input_seq_val.shape[0],1))), axis=1)
tmp_val = np.concatenate((x0_val.T,tmp_val), axis = 0)
val_data = np.reshape(tmp_val, (1,tmp_val.shape[0],tmp_val.shape[1])) # Validation Data

#   ***************** Create the test data *****************
input_seq_test = np.concatenate((np.zeros(shape=(250,1)),np.random.rand(time,1)*0.25))
x0_test = np.zeros(shape=(2,1))

state_test, test_label = dynamic_model(A, B , C,
                                      x0_test, input_seq_test, 
                                      input_seq_test.shape[0], sampling)

test_label = np.reshape(test_label.T,(1,test_label.T.shape[0],1)) # Label test data

input_seq_test = np.reshape(input_seq_test,(input_seq_test.shape[0],1))
tmp_test = np.concatenate((input_seq_test, np.zeros(shape=(input_seq_test.shape[0],1))), axis=1)
tmp_test = np.concatenate((x0_test.T,tmp_test), axis=0)
test_data = np.reshape(tmp_test, (1,tmp_test.shape[0],tmp_test.shape[1])) # Test data

train_label = normalizer(train_label, 'norm')
val_label = normalizer(val_label, 'norm')
test_label = normalizer(test_label, 'norm')

print('Total train data is: ', train_data.shape[1], flush=True)
print('Total validation data is: ', val_data.shape[1], flush=True)
print('Total testing data is:: ', test_data.shape[1], flush=True)
print('\nTrain data shape is: ', train_data.shape, flush=True)
print('Validation data shape is: ', val_data.shape, flush=True)
print('Testing data shape is:: ', test_data.shape, flush=True)
print('Train label shape is: ', train_label.shape, flush=True)
print('Validation label shape is: ', val_label.shape, flush=True)
print('Testing label shape is:: ', test_label.shape, flush=True)

#   ***************** Neuronal Network *****************
#   Model Creation
model = Sequential()
model.add(GRU(units=wandb.config['units'], input_shape=(None,train_data.shape[2]), use_bias=True, return_sequences=True))
#model.add(GRU(units=wandb.config['units'], return_sequences=True))

#   Hidden Layer
model.add(Dense(1))

#   Compile model
if (args.loss_type == 'mae'):
    model.compile(optimizer = 'adam', loss = 'mean_absolute_error', metrics = ['mae'])
else:
    model.compile(optimizer = 'adam', loss = 'mean_squared_error', metrics = ['mse'])
    
model.summary()
if (args.load_model != ''):
    model.load_weights(args.load_model)

#   Train model
history = model.fit(train_data, train_label ,
                    epochs = wandb.config['epochs'], batch_size = wandb.config['batch_size'], 
                    validation_data = (val_data, val_label),
                    verbose = 1, callbacks=[WandbCallback(save_model=False)])
model.save(args.model_name)

#   Model Prediction
testPredict = model.predict(test_data)

#   Desnormalizing Values
testPredict = normalizer(testPredict, '')
test_label = normalizer(test_label, '')

#   Model Evaluate
plot_loss(history)
plot_future(testPredict, test_label)
evaluate_prediction(testPredict, test_label)
