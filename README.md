# Diseño e implementación de un sistema que simule el comportamiento dinámico de una planta prototipo de control automático utilizando redes neuronales artificiales

<p align = justify>
  El presente proyecto busca simular mediantes redes neuronales artificiales el comportamiento dinámico de un péndulo amortiguado a hélice (PAHM). Para el desarrollo de la red neuronal artificial mimetizadora (RNAM) se requiere la conexión de la planta, quien posee un sistema embebido PSoC 5 LP, con un sistema embebido NVIDIA Jetson TX2. Para la comunicación de los sistemas se hace uso del protocolo UART. El sistema principal es la Jetson TX2 quien transmite el valor requerido para movilizar el motor codificado en PWM y recibe el ángulo del péndulo. Estos datos son almacenados para el entrenamiento de la RNAM. Los archivos pertenecientes a dicha comunicación se encuentran en /Data_Collection.
  
  Se desarrolla una planta sintética que corresponde al modelado matemático de la PAHM, determinado empíricamente con un porcentaje de aproximación del 84.99\%. Donde la ecuación lineal que describe el comportamiento dinámico de la PAHM es:
  
  $H(s) = \frac{\theta(s)}{V(s)} = \frac{2965}{s^2 +0.4151s+ 17.97}$
  
  Para el desarrollo de la RNAM se realiza un preprocesamiento de los datos y se emplea una arquitectura neuronal con una o dos capas GRU y una capa densa a su salida. En su entrenamiento se varía los hiperparámetros de neuronas y \textit{batch size}, cuyo resultado refleja que los valores óptimos son 32 y 16 respectivamente. Además de ello, se preentrenan los modelos y se prueba la eficacia de utilizar una o dos capas GRU.
  
  
  Se implementa una RNAM con el modelo sintético para evaluar su capacidad para aprender el comportamiento de la planta PAHM, cuya respuesta es satisfactoria con un error absoluto medio de $0,01175^{\circ}$ en sus predicciones. Paralelamente, se determina que el uso de una capa GRU es el adecuado para aprender el comportamiento del modelo, ya que el uso de dos capas GRU disminuye el error en $0.0531^{\circ}$. 
  
  
  Por otro lado, se implementa la RNAM con datos de la planta PAHM, cuyos resultados también son satisfactorios prediciendo con un error absoluto medio de $1,0875^{\circ}$. Donde a diferencia de la RNAM sintética, el uso de dos capas GRU resulta eficaz, reduciendo el error en  $2,817^{\circ}$.
  
  
  Por lo tanto, la RNAM tiene la capacidad de simular el comportamiento dinámico de la planta PAHM. En cuanto a su comparación con el modelo sintético, este presenta un error absoluto promedio de $17,5177^{\circ}$ con respecto a la respuesta real de la PAHM, por lo que se puede concluir que la aplicación de la RNAM aproxima de mejor forma que el modelo matemático determinado.
