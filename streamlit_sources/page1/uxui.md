#### Especificaciones del Proyecto: Adaptación de la Interfaz de Usuario

Para el proyecto, hemos puesto un especial énfasis en tener una **Interfaz de Usuario** basada en los conceptos de:
    - simplicidad
    - no sobrecarga
    - división de tareas

Siempre, y por supuesto, dentro de las limitaciones que impone el uso de StreamLit. Así, en vez de programar un menú en el lateral, hemos preferido dividir las diferentes secciones en páginas `[st.page]`, y modelar diferentes `librerías` propias de forma que nos permitiera trabajar simultáneamente a todos los miembros del proyecto cuando fuera necesario y equilibrar en la medida de lo posible que la UI ofrezca una UX tremendamente sencilla, evitando alardes de diseño.

Tal es así, que incluso se podrían lanzar en streamlit las páginas por separado, que con cambiar el nombre de la carpeta `hojas` por `pages`, el menú de la izquierda se recrearía automáticamente. No lo hicimos así simplemente por nuestra intención de gestionar todo personalmente.

##### Estilo Gráfico

1. **Themming**: Se utiliza el themming básico de Streamlit, utilizando una paleta de colores titulada "**La Delicadeza**", sacada del libro ["Psicología del color. Cómo actúan los colores sobre los sentimientos y la razón"](https://editorialgg.com/psicologia-del-color-libro.html) de Eva Heller.
2. **CSS**: Hemos limitado lo más posible este tipo de personalización, y organizativamente, lo tenemos en una única variable definida en `inc/input.py`.
