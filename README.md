# Diseño e implementación de un controlador basado en aprendizaje reforzado sobre una planta prototipo de control automático

<p align = justify>
Se propone hacer uso del aprendizaje automático para llevar a cabo el control de la planta, mediante redes neuronales artificiales (RNA) ya que estas constituyen una excelente herramienta para el aprendizaje de relaciones complejas a partir de un conjunto de ejemplos. Además, debido a sus capacidades de aproximación, así como su adaptabilidad, las redes neuronales artificiales presentan una importante alternativa en el modelado de sistemas no-lineales [1]. Por ello, se genera un interés del uso de estas mismas para la identificación y comportamiento de un sistema dinámico no lineal desconocido, donde a partir de la salida ante una entrada dada, la red sería capaz de modificar sus parámetros aprendiendo la dinámica de la planta hasta conseguir un sistema fiable [2].
  
<p align = justify>
Una alternativa que se ha vuelto muy popular, teniendo un alto crecimiento en los últimos años, es el aprendizaje reforzado (RL), donde este busca que un agente sea capaz de encontrar la acción correcta de manera autónoma interactuando una cantidad determinada de veces para conocer su entorno, como el agente [3]. Gran parte de este enfoque se ha utilizado para resolver juegos de Atari y sistemas de control, donde el control clásico no es 100\% efectivo debido a que no tienen la capacidad de lidear con problemas y se puede volver muy complejo. Aquí se puede observar la potencia que tiene el introducir el aprendizaje reforzado al control, ya que esta metodología podría ajustar los cambios del sistema al tener que interactuar con las acciones, permitiendo automatizar más el proceso.
  
<p align = justify>
Por lo tanto, se propone mediante utilizar dos redes neuronales artificiales, una que se comporte como el sistema de estudio, que adquiera las características de este y lo aproxime lo mejor posible; y otra que lleve a cabo el control del sistema por medio de aprendizaje reforzado.
  
<p align = justify>
Haciendo provecho del uso de las redes neuronales artificiales (RNA), además de obtener los beneficios de tener un sistema donde se puede experimentar con diversas entradas, sin afectar directamente la planta, evitando el riesgo de que los primeros experimentos son tan violentos en los cambios que pueden dañar la planta. Usando la RNA que mimetiza el comportamiento de la planta se puede usar un reloj más rápido, acelerando los experimentos y eliminando la desventaja de realizarlo en tiempo real, lo que lo vuelve un proceso más lento. Además, permite tener una gran cantidad de muestras de salida que serán de gran utilidad para ejecutar el entrenamiento de la red utilizando el aprendizaje reforzado.
  
<p align = justify>
Presenta un mejor tiempo de desarrollo, ya que con la ayuda de las RNA se puede prescindir de cálculos complejos, así como del planteamiento del modelo que se necesitaría para el control clásico, pues las RNA se puede adaptar a cualquier tipo de estructura sin necesidad de conocer sus características [2].


# Referencias
  <p align = justify>
[1] R. Valverde Gil and D. Gachet Páez, "Identificación de sistemas dinámicos utilizando redes neuronales", Revista Iberoamericana de Automática e Informática Industrial, no. 1697-7912, 2007.
<p align = justify>
[2] S. Torrubia Caravaca, "Redes neuronales multimodelo aplicadas al control de sistemas", Universidad Autónoma de Barcelona, España, 2010.
<p align = justify>
[3] A. Diaz Latorre, "Aprendizaje por refuerzo para control de sistemas dinámicos”, tesis por el título de Ingeniero Mecatrónico, Universidad Autónoma de Occidente, Santiago de Cali, Colombia, 2019.
