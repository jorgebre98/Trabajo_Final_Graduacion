# Libraries
import numpy as np
import matplotlib.pyplot as plt
from numpy.linalg import inv
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.layers import Dense, GRU, TimeDistributed, Dropout
from Synthetic_PAHM import dynamic_model

import wandb
from wandb.keras import WandbCallback

wandb.login()

wandb.init(project="Synthetic PAHM", 
           entity="mimetic-rna", 
           name='Synthetic PAHM prueba',
           resume='Allow', 
           id='Synthetic PAHM prueba')
wandb.config = {
    "epochs": 3500,
    "batch_size": 8,
    "units": 32,
    "learning_rate":0.001,
    "Dropout": 0.35
}

def plot_loss (history):
    plt.figure(figsize = (10, 6))
    plt.plot(history.history['loss'], label='Train loss')
    plt.plot(history.history['val_loss'], label='Validation loss')
    plt.title('Model Train vs Validation Loss for GRU network')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(loc='upper right')
    plt.savefig('lossGRU.png')

def plot_future(prediction, y_test):
    plt.figure(figsize=(10, 6))
    range_future = np.arange(prediction.shape[1])
    plt.plot(range_future, y_test[0,:], label='Test data', color = [1, 0.502, 0])
    plt.plot(range_future, prediction[0,:,0], label='Prediction',  color = [0.0502, 0.706, 0.949])
    plt.title('Predicted and true output')
    plt.xlabel('Tiempo (ms)')
    plt.ylabel('Ángulo (°)')
    plt.legend(loc='lower right')
    plt.savefig('PredictGRU.png')
    
def evaluate_prediction(predictions, actual):
    errors = predictions - actual
    mse = np.square(errors).mean()
    rmse = np.sqrt(mse)
    mae = np.abs(errors).mean()
    print('GRU:')
    print('Mean Absolute Error: {:.4f}%'.format(mae))
    print('Root Mean Square Error: {:.4f}%'.format(rmse))

#   Definition of the model in continuous time.
A = np.matrix([[0, 1],[-17.97, -0.3801]])
B = np.matrix([[0],[2965]])
C = np.matrix([[1, 0]])

# Number of time samples
time = 2000
sampling = 0.02


# ***************** Create the training data *****************
input_seq_train = np.random.rand(time,1)*0.25 # Input sequence for the simulation
x0_train = np.random.rand(2,1)*0.25 # Initial state for simulation

state, train_label = dynamic_model(A, B, C,
                                    x0_train, input_seq_train, 
                                    time ,sampling) # Simulate the dynamics 

train_label = np.reshape(train_label.T, (1, train_label.T.shape[0], 1)) # Label train data

input_seq_train = np.reshape(input_seq_train,(input_seq_train.shape[0], 1))
tmp_train = np.concatenate((input_seq_train, np.zeros(shape = (input_seq_train.shape[0], 1))), axis=1)
tmp_train = np.concatenate((x0_train.T,tmp_train), axis = 0)
train_data = np.reshape(tmp_train, (1, tmp_train.shape[0], tmp_train.shape[1])) # Train Data

# ***************** Create the validation data *****************
input_seq_val = np.random.rand(time,1)*0.25 # New input sequence
x0_val=np.random.rand(2,1)*0.25

state_val, val_label = dynamic_model(A, B, C,
                                     x0_val, input_seq_val, 
                                     time ,sampling) 

val_label = np.reshape(val_label.T,(1,val_label.T.shape[0],1)) # Label validation data

input_seq_val = np.reshape(input_seq_val,(input_seq_val.shape[0],1))
tmp_val = np.concatenate((input_seq_val, np.zeros(shape = (input_seq_val.shape[0],1))), axis=1)
tmp_val = np.concatenate((x0_val.T,tmp_val), axis = 0)
val_data = np.reshape(tmp_val, (1,tmp_val.shape[0],tmp_val.shape[1])) # Validation Data

# ***************** Create the test data *****************
input_seq_test = np.random.rand(time,1)*0.25
x0_test = np.random.rand(2,1)*0.25

state_test,test_label = dynamic_model(A, B , C,
                                      x0_test, input_seq_test, 
                                      time ,sampling)

output_test = np.reshape(test_label.T,(1,test_label.T.shape[0],1)) # Label test data

input_seq_test = np.reshape(input_seq_test,(input_seq_test.shape[0],1))
tmp_test = np.concatenate((input_seq_test, np.zeros(shape=(input_seq_test.shape[0],1))), axis=1)
tmp_test = np.concatenate((x0_test.T,tmp_test), axis=0)
test_data = np.reshape(tmp_test, (1,tmp_test.shape[0],tmp_test.shape[1])) # Test data

print('Total train data is: ', len(train_data), flush=True)
print('Total validation data is: ', len(val_data), flush=True)
print('Total testing data is:: ', len(test_data), flush=True)
print('\nTrain data shape is: ', train_data.shape, flush=True)
print('Validation data shape is: ', val_data.shape, flush=True)
print('Testing data shape is:: ', test_data.shape, flush=True)
print('Train label shape is: ', train_label.shape, flush=True)
print('Validation label shape is: ', val_label.shape, flush=True)
print('Testing label shape is:: ', test_label.shape, flush=True)

# ***************** Neuronal Network *****************
# Model Creation
model=Sequential()
model.add(GRU(units=wandb.config['units'], input_shape=(train_data.shape[1],train_data.shape[2]),return_sequences=True))
model.add(Dropout(wandb.config['Dropout']))

# Hidden Layer
model.add(GRU(units=wandb.config['units']))
model.add(Dropout(wandb.config['Dropout']))
model.add(Dense(1))

# Compile model
model.compile(optimizer = RMSprop(learning_rate = wandb.config['learning_rate']), 
              loss = 'mean_squared_error', metrics = ['mse'])
model.summary()

history = model.fit(train_data, train_label ,
                    epochs = wandb.config['epochs'], batch_size = wandb.config['batch_size'], 
                    validation_data = (val_data, val_label),
                    verbose = 1, callbacks=[WandbCallback(save_model=False)])
model.save('Synthetic_PAHM.h5')

# Model Prediction
testPredict = model.predict(test_data)

# Model Evaluate
plot_loss(history)
plot_future(testPredict, test_label)
evaluate_prediction(testPredict, test_label)

