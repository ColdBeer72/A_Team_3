#### Finalidad del Proyecto

Desarrollar un sistema de procesamiento de imágenes en tiempo real, utilizando la entrada de una webcam, para identificar puntos clave del esqueleto humano. El objetivo es detectar y evaluar la precisión de las posturas de yoga seleccionadas por el usuario, permitiendo incluso la evaluación de secuencias completas.

#### Retos afrontados:

###### 1. Desafío: Precisión en la Identificación de Posturas
**Reto:** Lograr que el sistema interprete con precisión las complejas posturas de yoga, considerando la variabilidad en las posiciones del cuerpo humano.  
**Solución:** Desarrollamos una Máquina de Estados (State Machine) que mapea de manera dinámica las posturas, garantizando un seguimiento preciso y adaptativo en tiempo real. Acompañamos la parte programática de unos cuántos consejos personalizados a cada postura, que recalquen la importancia de ciertas respiraciones, fuerzas aplicadas, etc.

###### 2. Desafío: Procesamiento de Imágenes en Tiempo Real
**Reto:** Asegurar una recepción fluida y sin demoras de las imágenes capturadas por la webcam, tanto en un entorno local como en un entorno de despliegue.  
**Solución:** En el entorno local, utilizamos `cv2` para gestionar el flujo de imágenes en tiempo real, mientras que para el despliegue optamos por `StreamLit WebRtc`, asegurando así una transmisión eficiente y sin latencia.

###### 3. Desafío: Modelado de Keypoints de Alta Precisión
**Reto:** Crear un modelo que identifique los puntos clave del esqueleto con la mayor exactitud posible, superando las limitaciones de los modelos preexistentes.  
**Solución:** Desarrollamos un modelo propio optimizado, diseñado específicamente para las complejidades de las posturas de yoga, permitiendo una detección más precisa y confiable.