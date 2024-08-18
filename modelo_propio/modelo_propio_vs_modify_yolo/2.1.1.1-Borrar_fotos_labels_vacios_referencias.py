import scipy.io
import numpy as np
import os

def eliminar_imagenes_sin_anotaciones(mat_file_path, image_folder_path, nuevo_mat_file_path):
    # Cargar el archivo .mat
    mat_data = scipy.io.loadmat(mat_file_path, squeeze_me=True, struct_as_record=False)

    # Obtener el campo de anotaciones
    release_data = mat_data['RELEASE']
    annolist = release_data.annolist

    # Lista para almacenar los índices de imágenes a eliminar
    indices_a_eliminar = []

    # Recorrer las anotaciones de cada imagen
    for idx, img_annotations in enumerate(annolist):
        eliminar_imagen = True

        if hasattr(img_annotations, 'annorect'):
            annorects = img_annotations.annorect

            # Comprobar si annorect es un solo objeto o una lista de objetos
            if isinstance(annorects, np.ndarray):
                annorects = annorects.tolist()  # Convertir a lista si es un ndarray

            if not isinstance(annorects, list):
                annorects = [annorects]  # Convertir a lista si es un solo objeto

            # Comprobar si alguna anotación de la persona tiene datos válidos
            for rect in annorects:
                # Verificar la existencia de coordenadas del rectángulo de cabeza
                if hasattr(rect, 'x1') and hasattr(rect, 'y1') and hasattr(rect, 'x2') and hasattr(rect, 'y2'):
                    eliminar_imagen = False  # Si alguna persona tiene coordenadas de rectángulo, no eliminar
                    break  # Salir del bucle si encontramos coordenadas válidas

                # Verificar la existencia de puntos de anotación
                if hasattr(rect, 'annopoints') and hasattr(rect.annopoints, 'point'):
                    points = rect.annopoints.point
                    if isinstance(points, np.ndarray):
                        points = points.tolist()  # Convertir a lista si es un ndarray

                    if not isinstance(points, list):
                        points = [points]  # Convertir a lista si es un solo objeto

                    for point in points:
                        if hasattr(point, 'x') and hasattr(point, 'y'):
                            eliminar_imagen = False  # Si alguna persona tiene puntos de anotación, no eliminar
                            break

        if eliminar_imagen:
            # Agregar índice a la lista de eliminación si no hay anotaciones válidas
            indices_a_eliminar.append(idx)
            # Obtener el nombre de la imagen
            image_name = img_annotations.image.name
            # Construir la ruta completa de la imagen
            image_path = os.path.join(image_folder_path, image_name)
            # Comprobar si la imagen existe y eliminarla
            if os.path.exists(image_path):
                print(f"Eliminando imagen: {image_path}")
                os.remove(image_path)

    # Filtrar las anotaciones para excluir las imágenes eliminadas
    nuevo_annolist = [img for i, img in enumerate(annolist) if i not in indices_a_eliminar]

    # Actualizar el campo de anotaciones en los datos de 'RELEASE'
    release_data.annolist = np.array(nuevo_annolist, dtype=object)

    # Guardar el nuevo archivo .mat sin las referencias a las imágenes eliminadas
    scipy.io.savemat(nuevo_mat_file_path, {'RELEASE': release_data})

    print("Proceso completado. Las imágenes sin anotaciones y sus referencias han sido eliminadas.")


# Uso de la función
mat_file_path = './Dataset2_anotations/mpii_human_pose_v1_u12_2/mpii_human_pose_v1_u12_1.mat'  # Ruta al archivo .mat original
image_folder_path = '../../../../human_pose_images_filtrado_1_persona/images'  # Ruta a la carpeta de imágenes
nuevo_mat_file_path = './Dataset2_anotations/mpii_human_pose_v1_u12_2/mpii_human_pose_v1_u12_1FINAL.mat'  # Ruta al nuevo archivo .mat

eliminar_imagenes_sin_anotaciones(mat_file_path, image_folder_path, nuevo_mat_file_path)


# def inspeccionar_datos(mat_file_path, num_muestras=5):
#     # Cargar el archivo .mat
#     mat_data = scipy.io.loadmat(mat_file_path, squeeze_me=True, struct_as_record=False)
#     release_data = mat_data['RELEASE']
#     annolist = release_data.annolist

#     # Inspeccionar las primeras `num_muestras` imágenes
#     for idx, img_annotations in enumerate(annolist[:num_muestras]):
#         print(f"\nImagen índice: {idx}")
#         print(f"Nombre de imagen: {img_annotations.image.name}")
        
#         if hasattr(img_annotations, 'annorect'):
#             annorects = img_annotations.annorect

#             # Comprobar si annorect es un solo objeto o una lista de objetos
#             if isinstance(annorects, np.ndarray):
#                 annorects = annorects.tolist()  # Convertir a lista si es un ndarray

#             if not isinstance(annorects, list):
#                 annorects = [annorects]  # Convertir a lista si es un solo objeto

#             print(f"Cantidad de personas anotadas: {len(annorects)}")
#             for rect in annorects:
#                 if hasattr(rect, 'x1') and hasattr(rect, 'y1'):
#                     print(f"  Coordenadas: x1={rect.x1}, y1={rect.y1}, x2={rect.x2}, y2={rect.y2}")
#                 else:
#                     print("  Sin anotaciones de coordenadas")
#         else:
#             print("Sin anotaciones de personas")

# # Uso de la función
# mat_file_path = './Dataset2_anotations/mpii_human_pose_v1_u12_2/mpii_human_pose_v1_u12_1.mat'  # Ruta al archivo .mat original
# inspeccionar_datos(mat_file_path, num_muestras=10)
