import os
import wandb
import torch
import numpy as np
import pandas as pd
import torch.nn as nn
import matplotlib.pyplot as plt
from wandb.keras import WandbCallback

import warnings
warnings.filterwarnings('ignore')

root = '/content/drive/Othercomputers/Mi portátil/TEC/TFG/Datos_Recolectados/'
Dir = os.listdir(root)
pwm = np.array([])
angle = np.array([])

# Read all the .csv files and make an nx4 array
# Next, separate the pwm value and angle in their respective arrays.
print('******************* Process the Dataset *******************',flush=True)
print('Recolecting Data',flush=True)
for filename in Dir:
    files = pd.read_csv(root + filename)
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

print('Total train data is: ', len(train_data), flush=True)
print('Total validation data is: ', len(val_data), flush=True)
print('Total test data is: ', len(test_data), flush=True)

# Reshape the arrays (n,window,1). Where n is the total amount of data in the array
print('Reshape arrays to tensors',flush=True)
train_data = np.reshape(train_data,(train_data.shape[0],1,train_data.shape[1]))
val_data = np.reshape(val_data,(val_data.shape[0],1,val_data.shape[1]))
test_data = np.reshape(test_data,(test_data.shape[0],1,test_data.shape[1]))
print('******************* Finish *******************',flush=True)


train_data = torch.Tensor(train_data).to(device)
train_label = torch.Tensor(train_label).to(device)
val_data = torch.Tensor(val_data).to(device)
val_label = torch.Tensor(val_label).to(device)
test_data = torch.Tensor(test_data).to(device)
test_label = torch.Tensor(test_label).to(device)

batch = train_data.shape[0]
sequence_lenght = train_data.shape[1]
input_size = train_data.shape[2]

class GRUNetwork(nn.Module):
    def __init__(self, input_size, hidden_size, n_layers, output_dim, drop_prob=0.2):
        super(GRUNetwork, self).__init__()
        self.n_layers = n_layers
        self.hidden_dim = hidden_size
        
        self.gru = nn.GRU(input_size, hidden_size, n_layers, batch_first=True, dropout=drop_prob)
        self.fc = nn.Linear(hidden_size, output_dim)
        #self.relu = nn.ReLU()
        
    def forward(self, x):
        h0 = torch.zeros(self.n_layers,x.size(0),self.hidden_dim).to(device)
        out,_ = self.gru(x,h0)
        out = self.fc(out[:,-1,:])
        #out = self.fc(self.relu(out[:,-1]))
        return out

model = GRUNetwork(input_size, 8, 1, 1, wandb.config['Dropout']).to(device)
loss_function = nn.MSELoss(reduction='mean')
optimizer = torch.optim.Adam(params=model.parameters(), lr=wandb.config['learning_rate'])
hystory = pd.DataFrame()


for epoch in range(1, wandb.config["epochs"] + 1):
    y_train = model(train_data)
    loss = loss_function(input=y_train, target=train_label)
    loss.backward() # Backward propagation. Calculate all the gradients needed to adjust the weights.
    optimizer.step() # Uses gradients to change weight values
    optimizer.zero_grad() # Don't accumulate gradients in epoch iterations.
    
    # Calculate the accuracy without modifying the weights of the neural network
    with torch.no_grad():
        correct = (y_train == train_label).sum()
        accuracy_train = 100*correct/float(len(test_data))
    
    df_temp = pd.DataFrame(data={
        'Epoch': epoch,
        'Loss': round(loss.item(),5),
        'Accuracy': round(accuracy_train.item(),5)},index=[0])



