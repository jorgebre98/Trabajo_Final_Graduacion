# Diseño e implementación de un controlador utilizando aprendizaje reforzado sobre una planta prototipo de control automático

<p align = justify>
  En el presente repositorio se lleva a cabo el trabajo final de graduación (TFG) donde se desarrolla un controlador para la planta de péndulo amortiguado a hélice (PAHM) utilizando aprendizaje reforzado.
  
<p align = justify>
  Para llevar a cabo esto se hace uso de dos redes neuronales artificiales (RNA). La RNA se encarga de mimetizar el comportamiento del sistema de estudio con el fin de experimentar con diversas entradas sin afectar directamente la planta, se puede usar un reloj más rápido que el tiempo real, entre otros. La segunda RNA lleva a cabo el controlador de la planta, el cual utilizará aprendizaje reforzado, cuya metodología busca que un agente sea capaz de encontrar la acción correcta de manera autónoma, explorando un espacio desconocido y determinando la acción mediante prueba y error.
  
<p align = justify>
  A continuación, se realiza una breve explicación del código utilizado. En la carpeta documentación, como su nombre lo indica, se está la documentación llevada a cabo en el transcurso del TFG.

<p align = justify>
  En el archivo comunicación_UART.py se realiza la comunicación de la tarjeta NVIDIA Jetson TX 2 a la PSoC por medio del protocolo UART. Donde …
  
<p align = justify>
  En el archivo red_mimetizadora.py …
  
<p align = justify>
  Por último, en el archivo controlador_RL.py se encuentra …
