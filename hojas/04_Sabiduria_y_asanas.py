import streamlit as st
from inc.basic import *

st.markdown(HIDE_IMG_FS, unsafe_allow_html=True)

st.title('Sabiduría y Asanas')

st.markdown("Aquí descubrirás los Yoga Sutras, un conjunto de aforismos que forman la base filosófica del yoga, y te guiarán hacia una práctica más consciente y significativa. Además, te ofrecemos una explicación detallada de las asanas (posturas), donde cada postura es desglosada con sus beneficios, alineaciones y variaciones, para que puedas enriquecer tu práctica física y espiritual. Esta sección está diseñada para que tanto principiantes como practicantes avanzados puedan encontrar inspiración y conocimiento en su camino de yoga. :rainbow[Tu camino hacia la iluminación empieza aquí]")

with st.expander("**Los orígenes del Ashtanga**"):
    st.write("La idea de que el Yoga Sutra y el sistema del vinyasa son dos lados de una moneda estuvo muy presente desde el comienzo del linaje contemporáneo del Ashtanga Yoga. K. Pattabhi Jois recibió el método de vinyasa de su maestro T. Krishnamacharya; el maestro de Krishnamacharya, Ramamohan Brahmachary, le ordenó buscar la última copia que quedaba de una Escritura difícil de localizar, el Yoga Korunta, que se creía que había sido compilado por el antiguo vidente Vamana")
    st.image("streamlit_sources/wikimágenes/Krishnamacharya.jpg", caption="Krishnamacharya es el maestro de K. Pattabhi Jois, principal impulsor del Yoga contemporáneo")
    st.write("Según la biografía de Krishnamacharya, el Yoga Korunta, no contenía solamente el sistema de vinyasa, sino también el Yoga Sutra de Patanjali y su comentario, Yoga Bhasya, compilado por el Rishi [sabio] Vyasa. Estos estaban juntos en un volumen. De esto podemos ver que en la antigüedad lo que ahora se considera dos sistemas que comparten el mismo nombre – el Ashtanga Yoga de Patanjali y el Ashtanga Vinyasa del Rishi Vamana – eran de hecho uno.")
    st.image("streamlit_sources/wikimágenes/pattabhi.jpg", caption="Pattabhi Jois fue el creador del Ashtanga yoga moderno y principal impulsor del yoga en occidente a través de sus alumnos.")

with open("streamlit_sources/sutras.md", "r", encoding="utf-8") as sutras_md:
    contenido_md = sutras_md.read()

with st.expander("**Los Sutras de Patanjali**"):
    st.markdown("Los Yoga-sutra son los antiguos textos fundacionales del yoga, escritos por el sabio Patañyali en el siglo III a. C. Pese a ser un conjunto de textos cortos, han tenido una enorme influencia en las creencias y prácticas del yoga a nivel mundial. Estos aforismos son la semilla que de generación en generación se han ido transmitiendo de maestro a aprendiz durante siglos. Ahora, este conocimiento llega a nosotros en plena era de la información y estamos viviendo un auténtico florecimiento del yoga en todo el mundo. e influencia en las creencias y prácticas del yoga Esperamos que estos aforismos refuercen tu práctica.")
    st.image("streamlit_sources/wikimágenes/sutras_papiro.png", caption="Los sutras son textos del siglo III a. C.")
    st.markdown(contenido_md, unsafe_allow_html=True)

with st.expander("**Surya Namaskar A** ***(Saludo al Sol A)***"):
    st.write("El Saludo al Sol es una serie de posturas sincronizadas con la respiración que se realizan en un flujo continuo. Esta práctica tradicionalmente se ofrece como una forma de reverencia al sol, simbolizando la energía y el dinamismo. Es una excelente manera de calentar el cuerpo, mejorar la flexibilidad y preparar la mente para una práctica más profunda de yoga.")
    st.image("streamlit_sources/wikimágenes/Surya Namaskar.png", caption="El saludo al sol (Surya Namaskar en sanscrito) Es una práctica fundamental en muchas tradiciones de yoga y se utiliza tanto como calentamiento al inicio de una clase como una práctica completa en sí misma.", width=None)