import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tensorflow.keras.models import Sequential
from tensorflow.keras.backend import clear_session
from tensorflow.keras.optimizers import RMSprop, Adam
from tensorflow.keras.layers import Dense, Dropout, GRU, TimeDistributed



# ## 2. Dataset 
print('Process Data',flush=True)
Dir = os.listdir('/home/nvidia/Documents/TFG Jorge Brenes/Datos')
Data_Collect = np.array([[0,0,0,0]])
for filename in Dir:
    files = pd.read_csv('/home/nvidia/Documents/TFG Jorge Brenes/Datos/'+filename)
    Data_Collect = np.append(Data_Collect, files.values, axis=0)

train_data = np.array([])
val_data = np.array([])
train_label = np.array([])
val_label = np.array([])
cont=0

while(cont < Data_Collect[:,2].shape[0]):
    if cont < round(Data_Collect[:,2].shape[0]*0.75):
        train_data = np.append(train_data, Data_Collect[:,2][cont])
        train_label = np.append(train_label, Data_Collect[:,3][cont])
    else:
        val_data = np.append(val_data, Data_Collect[:,3][cont])
        val_label = np.append(val_label, Data_Collect[:,3][cont])
    cont+=1

train_data = np.reshape(train_data,(1,train_data.shape[0],1))
train_label = np.reshape(train_label,(1,train_label.shape[0],1))

val_data = np.reshape(val_data,(1,val_data.shape[0],1))
val_label = np.reshape(val_data,(1,val_label.shape[0],1))

print('Finish',flush=True)

# ## 3. Neural Network

# ### 3.1 Model Creation

# In[ ]:


clear_session()

model = Sequential()
model.add(GRU(64, input_shape=(train_data.shape[1],1),return_sequences=True))
model.add(Dropout(0.35))
model.add(TimeDistributed(Dense(1)))  #there is no difference between this and model.add(Dense(1))...
model.compile(optimizer=Adam(), loss='mean_squared_error', metrics=['mse','acc'])

model.summary()


# ### 3.2 Model Training

print('Training',flush=True)
history = model.fit(train_data, train_label,
                    epochs=500, batch_size=8,
                    validation_data = (val_data,val_label),
                    verbose=2)

#testPredict = model.predict(test_data)


# ### 3.3 Model Evaluate

#loss, accuracy = model.evaluate(testX,output_test)

joblib.dump(model, 'GRU_model.joblib')


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

