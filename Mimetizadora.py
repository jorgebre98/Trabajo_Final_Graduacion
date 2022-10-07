#!/usr/bin/env python
# coding: utf-8

# ## Tecnológico de Costa Rica
# 
# ### Autor: Jorge Andrés Brenes Alfaro
# 
# ## Red mimetizadora
# 
# 

# ## 1. Bibliotecas

# In[1]:


import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.preprocessing import MaxAbsScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.backend import clear_session
from tensorflow.keras.optimizers import RMSprop, Adam
from tensorflow.keras.layers import Dense, Dropout, GRU, TimeDistributed

import warnings
warnings.filterwarnings('ignore')


# ## 2. Dataset 

# In[2]:


def normalizer(angle,action):
    if action == 'norm':
        norm = MaxAbsScaler()
        angle_normalize = norm.fit_transform(angle)
    else:
        angle_normalize = angle.inverse_transform(angle)
    return angle_normalize


# In[3]:


# Separate the values in train, validation and test data/label
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


# In[4]:


def create_dataset (X, Y, look_back = 1):
    Xs, ys = [], []
    
    for i in range(len(X)-look_back):
        v = X[i:i+look_back]
        Xs.append(v)
        #ys.append(X[i+look_back])
        ys.append(Y[i+look_back])
    
    return np.reshape(np.array(Xs),(np.array(Xs).shape[0],np.array(Xs).shape[1],1)), np.reshape(np.array(ys),(-1))


# In[5]:


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

train_data, train_label, val_data, val_label, test_data, test_label = separate_values(pwm, angle)

print('Total train data is: ', len(train_data), flush=True)
print('Total validation data is: ', len(val_data), flush=True)
print('Total testing data is:: ', len(test_data), flush=True)

print('Normalizing Angle Values')
train_label = np.reshape(train_label,(train_label.shape[0],1))
train_target = normalizer(train_label,'norm')

val_label = np.reshape(val_label,(val_label.shape[0],1))
val_target = normalizer(val_label,'norm')

test_label = np.reshape(test_label,(test_label.shape[0],1))
test_target = normalizer(test_label,'norm')

print('Accommodating data for the GRU network',flush=True)
X_train, y_train = create_dataset(train_data, train_target, 4)
X_val, y_val = create_dataset(val_data, val_target, 4)
X_test, y_test = create_dataset(test_data, test_target, 4)

print('\nTrain data shape is: ', X_train.shape, flush=True)
print('Validation data shape is: ', X_val.shape, flush=True)
print('Testing data shape is:: ', X_test.shape, flush=True)
print('Train label shape is: ', y_train.shape, flush=True)
print('Validation label shape is: ', y_val.shape, flush=True)
print('Testing label shape is:: ', y_test.shape, flush=True)
print('******************* Finish *******************',flush=True)


# ## 3. Neural Network

# ### 3.1 Model Creation

# In[6]:


clear_session()

units = 32
model = Sequential()
model.add(GRU (units = units, return_sequences = True, input_shape = [X_train.shape[1], X_train.shape[2]]))
model.add(Dropout(0.2)) 
    # Hidden layer
model.add(GRU(units = units))                 
model.add(Dropout(0.2))
model.add(Dense(units = 1)) 
#Compile model
model.compile(optimizer='adam',loss='mse')
model.summary()


# ### 3.2 Model Training

# In[7]:


history = model.fit(X_train, y_train, 
                    epochs = 4, validation_data = [X_val, y_val],
                    batch_size = 16, verbose = 1)


# In[ ]:


testPredict = model.predict(X_test)


# ### 3.3 Model Evaluate

# In[ ]:


def plot_loss (history, model_name):
    plt.figure(figsize = (10, 6))
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model Train vs Validation Loss for ' + model_name)
    plt.ylabel('Loss')
    plt.xlabel('epoch')
    plt.legend(['Train loss', 'Validation loss'], loc='upper right')

def plot_future(prediction, model_name, y_test):
    
    plt.figure(figsize=(10, 6))
    
    range_future = len(prediction)
    plt.figure()
    plt.plot(np.arange(range_future)[10000:15000], np.array(y_test)[10000:15000], label='Test data')
    plt.figure()
    plt.plot(np.arange(range_future)[10000:15000], np.array(prediction)[10000:15000], 'r',label='Prediction')
    plt.legend(loc='upper left')
    
def evaluate_prediction(predictions, actual, model_name):
    errors = predictions - actual
    mse = np.square(errors).mean()
    rmse = np.sqrt(mse)
    mae = np.abs(errors).mean()

    print(model_name + ':')
    print('Mean Absolute Error: {:.4f}%'.format(mae*100))
    print('Root Mean Square Error: {:.4f}%'.format(rmse*100))
    print('')


# In[ ]:


plot_loss(history,'GRU')


# In[ ]:


plot_future(testPredict,'GRU',y_test)


# In[ ]:


plt.plot(np.reshape(X_test,(-1))[10000:15000])


# In[ ]:


evaluate_prediction(testPredict,y_test,'GRU')

