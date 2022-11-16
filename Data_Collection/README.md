# Recolección de Datos
<p align = justify>
Para la recolección de datos se ocupa programar tanto la Jetson TX2 como el PSoC para dicha acción. La Jetson TX2 consta de 4 módulos para su programación 
distribuidos en los archivos:  Data_collection.py, RepeatedTimer.py y Transmit_Receive.py. Estos módulos son un temporizador, un comunicador, un convertidor
de datos y recolector de datos. En la figura 1 se muestra la interconexión de los módulos.

![Modulos_Jetson](https://user-images.githubusercontent.com/79665536/202050952-f726effe-ac99-4b18-aa46-27967329f2dc.svg)
<p align = center>
Figura 1. Interconexión de los módulos de la Jetson TX2.

<p align = justify>
El archivo Data_collection.py corresponde al recolector de datos, cuya función es recopilar y reinsertar los datos enviados y recibidos vía PSoC hacia y desde
el PAHM. Además, se definen dos tipos de entradas: la \emph{manual}, que, por medio de una interfaz gráfica con un deslizador permite cambiar manualmente el 
valor PWM a transmitir y almacenar para futuras reproducciones. Por otro lado, se tiene la entrada de \emph{reproducción} (\textit{playback}). Este tipo de 
entrada reutiliza la misma entrada de un experimento previo, para de este modo reproducir y así evaluar efecto en la salida producido por factores variantes en 
el tiempo del PAHM ante la misma secuencia de entrada, así como determinar el promedio y la desviación estándar de las respuestas entregadas en repeticiones 
experimentales. Una vez finalizado los experimentos, se ponen a disposición en un archivo .csv con el fin de utilizarlos para el entrenamiento de la RNAM.

<p align = justify>
El PAHM opera con muestreo homogéneo cada $20$\,ms por lo que se necesita que el código se ejecute y dé respuesta en ese lapso de tiempo concreto. Por ello, se 
implementa el archivo RepeatedTimer.py, el cual es necesario para llamar una función cada determinado tiempo, encargada de transmitir y recibir valores en el 
tiempo requerido por el PAHM. 

<p align = justify>
Por último, el archivo Transmit_Receive.py se encarga de transmitir y recibir datos hacia y desde el PSoC. Este utiliza dos funciones: la función \emph{reset()}
que limpia los búferes de entrada y salida para evitar que permanezcan datos residuales de anteriores transmisiones y perjudique la lectura de los datos. Posterior
a ello, la función \emph{Transmit\_Receive()}, la cual se encarga del proceso de transmisión referido a empaquetar el valor PWM en dos \textit{bytes} y transmitirlo 
al PSoC, y el proceso de recepción referido a desempaquetar los cuatro \textit{bytes} recibidos desde el PSoC correspondientes al valor del ángulo medido por el
sensor. Estos dos valores se conservan en un arreglo para la creación del archivo .csv. Dentro de este código también se realiza la conversión de datos 
correspondiente a la desnormalización del valor PWM encapsulada en la función \emph{desnormalizePWM()}.

<p align = justify>
Para el uso de ellos se debe ejecutar el archivo Data_collection.py, el cual ocupará en su llamado el nombre de un archivo de entrada si se desea utilizar el modo reproducción. En caso de ponerlo se utiliza el modo manual. Tambien se le debe indicar el archivo de salida, el cual corresponde al archivo donde se van a almacenar los datos recopilados del PAHM.

<p align = justify>
Ejemplo del llamado: python3 Data_collection.py --input 'Archivo_a_leer.csv' --output 'Archivo_a_escribir.csv'

<p align = justify>
Ahora bien, en cuanto al sistema PSoC, se utiliza el archivo main.c el cual contiene la lógica para que el sistema funcione. Además de ello, dentro del software 
de PSoC creator se debe utilizar:
Un PWM digital, con resolución de 16 bits y un periodo de 250 $\mu$s.
Un decodificador de cuadratura, al cual se le da una resolución de 16 bits y una resolución de contador de 1.
Un bloque UART, con tasa de transmisión de 115200, 1 bytes da datos, no se activa bit de paridad y no se hace uso del control de flujo.
Un temporizador, donde se configura con un periodo de 20 ms.
Una interrupción, un led de ejecución y dos señales de reloj, una de 8 MHz y otra de 1 MHz.

<p align = justify>
Estos bloques se conectan como se muestra en el diagrama de la figura 2

<p align = center>
![Diseno_psoc](https://user-images.githubusercontent.com/79665536/202051062-8f0575b6-d922-4d07-9bad-1208dd9f4dac.svg)
Diagrama de conexión de bloques en el PSoC 5 LP.
