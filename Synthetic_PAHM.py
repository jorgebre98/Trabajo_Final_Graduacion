# ************************************************************* #
#               Copyright (C) 2022 Jorge Brenes Alfaro.
#               EL5617 Trabajo Final de Graduación.
#               Escuela de Ingeniería Electrónica.
#               Tecnológico de Costa Rica.
# ************************************************************* #
#
#   The presen code is based in H. Kapasi, 2022. "Modeling Non-Linear Dynamic Systems with Neural Networks", 2022. [Online].
#   Available in: https://towardsdatascience.com/modeling-non-linear-dynamic-systems-with-neural-networks-f3761bc92649.
# 
#   La red diseñada es la encargada de reproducir el comportamiento de entrada y salida de un modelado empírico de la planta
# prototipo de péndulo amortiguado a hélice (PAHM).

#   Libraries
import numpy as np
from numpy.linalg import inv
import matplotlib.pyplot as plt
import pandas as pd

#   Function to discrete the PAHM's dynamic.
#   Discretize by backward euler method.
def dinamica_modelo(A,B,C,cond_initial,input_sequence, time_steps,h):
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

def Synthetic_PAHM(filename):
#   Definition of the model in continuous time.
#   A,B,C              - continuous time system matrices 
#   initial_state      - the initial state of the system 
#   time_steps         - the total number of simulation time steps 
#   sampling           - the sampling period for the backward Euler discretization
#   input_seq          - Input sequence

    A = np.matrix([[0, 1],[-17.97, -0.3801]])
    B = np.matrix([[0],[2965]])
    C = np.matrix([[1, 0]])

    data = pd.read_csv(filename)
    input_seq = data.values[:,2]
    tiempo = len(input_seq)
    sampling = 0.02
    initial_state = np.array([[0],[0]])

    # Convert to discrete time the response of the PAHM
    X,Y = dinamica_modelo(A,B,C,initial_state,input_seq,tiempo,sampling)
    plt.subplot(1,2,1)
    plt.plot(input_seq)
    plt.xlabel('Time (ms)')
    plt.title('Input sequence')
    
    plt.subplot(1,2,2)
    plt.plot(Y[0,:])
    plt.xlabel('Tiempo (ms)')
    plt.ylabel('Ángulo')
    plt.title('Step response')
    plt.show()
