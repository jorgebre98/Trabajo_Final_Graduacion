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
print('*************** Process Data *************** ',flush=True)
Dir = os.listdir('/home/nvidia/Documents/TFG Jorge Brenes/Datos_Recolectados')
Data_Collect = np.array([[0,0,0,0]])
for filename in Dir:
    file = pd.read_csv('/home/nvidia/Documents/TFG Jorge Brenes/Datos_Recolectados/'+filename)
    Data_Collect = np.append(Data_Collect, file.values,axis=0)

train_data = np.array([])
train_label = np.array([])

val_data = np.array([])
val_label = np.array([])

test_data = np.array([])
test_label = np.array([])

train_lenght = int(len(Data_Collect)*3/5)
val_lenght = int(len(Data_Collect)*4/5)

for i in Data_Collect[:train_lenght,2:]:
    train_data = np.append(train_data, i[0])
    train_label = np.append(train_label, i[1])

for j in Data_Collect[train_lenght:val_lenght,2:]:
    val_data = np.append(val_data, i[0])
    val_label = np.append(val_label, i[1])
    
for j in Data_Collect[val_lenght:,2:]:
    test_data = np.append(test_data, i[0])
    test_label = np.append(test_label, i[1])
    
print('El total de datos de entrenamiento es: ', len(train_data))
print('El total de datos de validación es: ', len(val_data))
print('El total de datos de prueba es: ', len(test_data))

train_data = np.reshape(train_data,(train_data.shape[0],1))
tmp_train = np.concatenate((train_data, np.zeros(shape=(train_data.shape[0],1))), axis=1)
train_x = np.reshape(tmp_train, (1,tmp_train.shape[0],tmp_train.shape[1]))
train_label = np.reshape(train_label,(1,train_label.shape[0],1))

val_data = np.reshape(val_data,(val_data.shape[0],1))
tmp_val = np.concatenate((val_data, np.zeros(shape=(val_data.shape[0],1))), axis=1)
val_x = np.reshape(tmp_val, (1,tmp_val.shape[0],tmp_val.shape[1]))
val_label = np.reshape(val_data,(1,val_label.shape[0],1))

test_data = np.reshape(test_data,(test_data.shape[0],1))
tmp_test = np.concatenate((test_data, np.zeros(shape=(test_data.shape[0],1))), axis=1)
test_x = np.reshape(tmp_test, (1,tmp_test.shape[0],tmp_test.shape[1]))
test_label = np.reshape(test_data,(1,test_label.shape[0],1))

print('*************** Finish ***************  ',flush=True)

# ## 3. Neural Network
# ### 3.1 Model Creation
clear_session()

model = Sequential()
model.add(GRU(64, input_shape=(train_x.shape[1],train_x.shape[2]),return_sequences=True))
model.add(Dropout(0.35))
model.add(TimeDistributed(Dense(1)))  #there is no difference between this and model.add(Dense(1))...
model.compile(optimizer=Adam(), loss='mean_squared_error', metrics=['mse','acc'])

model.summary()

# ### 3.2 Model Training
print('Training',flush=True)
history = model.fit(train_x, train_label,
                    epochs=500, batch_size=8,
                    validation_data = (val_x,val_label),
                    verbose=2)


testPredict = model.predict(test_x)


# ### 3.3 Model Evaluate

loss, accuracy = model.evaluate(test_x,test_label)

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

