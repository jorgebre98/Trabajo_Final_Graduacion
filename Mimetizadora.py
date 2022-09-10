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


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GRU, TimeDistributed
from tensorflow.keras.optimizers import RMSprop, Adam

from tensorflow.keras.backend import clear_session

import warnings
warnings.filterwarnings('ignore')


# ## 2. Dataset 

# In[2]:


Dataset = pd.read_excel('Data_Collection.xlsx')  #Se leen los datos del archivo .xlsx
Dataset = Dataset.values # convierten los valores a un array

latencia, pwm_value, angle = [Dataset[:,0]], Dataset[:,1], Dataset[:,2]

# **** DATA ****
train_data = pwm_value[:int(0.8*Dataset.shape[0])] # 80% de los datos
val_data = pwm_value[int(0.8*Dataset.shape[0]):int(0.9*Dataset.shape[0])] # 10% de los datos
test_data = pwm_value[int(0.9*Dataset.shape[0]):] # 10% de los datos

# **** LABELS ****
train_label = angle[:int(0.8*Dataset.shape[0])]
val_label = angle[int(0.8*Dataset.shape[0]):int(0.9*Dataset.shape[0])]
test_label = angle[int(0.9*Dataset.shape[0]):] 

# **** RESHAPE ****
train_data = np.reshape(train_data,(1,train_data.shape[0],1))
val_data = np.reshape(val_data,(1,val_data.shape[0],1))
test_data = np.reshape(test_data,(1,test_data.shape[0],1))

train_label = np.reshape(train_label,(1,train_label.shape[0],1))
val_label = np.reshape(val_label,(1,val_label.shape[0],1))
test_label = np.reshape(test_label,(1,test_label.shape[0],1))

print('El total de datos de entrenamiento es: ', train_data.shape[1])
print('El total de datos de validación es: ', val_data.shape[1])
print('El total de datos de prueba es: ', test_data.shape[1])


# In[3]:


train_data.shape


# ## 3. Neural Network

# ### 3.1 Model Creation

# In[ ]:


clear_session()

model = Sequential()
model.add(GRU(64, input_shape=(train_data.shape[1],train_data.shape[2]),return_sequences=True))
model.add(Dense(1))
#model.add(TimeDistributed(Dense(1)))  #there is no difference between this and model.add(Dense(1))...
model.compile(optimizer=Adam(), loss='mean_squared_error', metrics=['mse'])

model.summary()


# ### 3.2 Model Training

# In[ ]:


history = model.fit(train_data, train_label, 
                  epochs=500, batch_size=1, 
                  validation_data=(val_data,val_label),verbose=2)

model.save('modelo_PAHM', save_format="h5")

# use the test data to predict the model response
#testPredict = model.predict(test_data)


# ### 3.3 Model Evaluate

# In[ ]:




