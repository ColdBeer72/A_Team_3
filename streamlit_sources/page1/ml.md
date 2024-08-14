## Creación de modelo propio para detectar puntos clave en postura corporal

Hemos querido investigar cual es el proceso para crear un modelo de detección de puntos clave **desde cero**,
lo cual tiene sus retos y tecnologías independientes.

- Proceso a seguir
    1. Conseguir o crear un dataset de imagenes variadas sobre personas en diferentes posturas:
        1. Anotar en cada foto los puntos que queremos que nuestro modelo detecte con herramientas de anotacion para conjuntos de datos como Labelme.
        2. Dejar las anotaciones en el formato deseado, en este caso un array en el que deben de ir anotados todos los puntos coprorales (visibles o no) junto al path de cada imagen en un archivo Json.
    2. Entrenar un modelo **Deep Learning** con aumentado de datos en lotes para poder hacer **más con menos**:
        1. Creamos método aumentado de datos por probabilidad gracias a la biblioteca imgaug, asi de cada imagen anotada podremos sacar algunas más con una modificación tal cual que los keypoints de la original se modifiquen con el mismo sentido para que sigan teniendo el sitio correcto.
        2. Entrenamos modelo en lotes, asi no tenemos que almacenar ni procesar en local todas las imagenes generadas en el aumentado.
    3. Configurar y guardar modelo para que su salida sea compatible con el State Machine de Yolo
---

- Problemas encontrados
    1. Creación de un Dataset con una cantidad de imágenes aceptable sobre la temática de la aplicación. 
    2. Si se opta por usar un dataset existente, los datasets de muestra que se han usado para este cometido en internet estan compuestos de 5.000, 12.000 o incluso 24.000 imágenes, por lo tanto requiere de un proceso de mayor tiempo y personas para el etiquetado manual. Por lo tanto los resultados del modelo necesitan de más entrenamiento para empezar a concebir o aprender la postura humana.
