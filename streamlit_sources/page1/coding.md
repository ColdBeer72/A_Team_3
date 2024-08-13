#### Codificación, Libro de Estilo

Ha sido **objetivo número uno** el mantener una organización y una codificación lo más limpias posibles, fácil de leer y comprender y organizada por necesidades. Reciclando y reusando, en la medida de lo posible, todas las utilidades y/o valores que se pudiera.

##### Organización

- **hojas**: Ahí están los ficheros Python para Streamlit que definen las páginas del proyecto.
- **inc**: En este lugar definimos las **librerías propias** en Python que utilizamos en el proyecto:
    - **basic** es la librería que define configuraciones y funciones básicas relacionadas con la interfaz de usuario o páginas de streamlit
    - **config** es el fichero donde definimos variables globales, para su fácil configuración
    - otros, librerías de clases y funciones específicas para manejo de vídeo e IA
- **streamlit_sources**: Aquí disponemos todo el material de apoyo (tanto gráfico como de texto/markdown) que utilizamos en las páginas, de forma que limitamos al máximo el uso de *"textos"* en el código. Internamente, se subidivide en carpetas en función de la página a la que afecta.