import cv2
import face_recognition

def reconocimiento_facial(imagen, nombres_conocidos, encodings_conocidos):
    # Convertir la imagen a RGB (face_recognition trabaja con imágenes en RGB)
    imagen_rgb = cv2.cvtColor(imagen, cv2.COLOR_BGR2RGB)

    # Detectar rostros en la imagen
    rostros = face_recognition.face_locations(imagen_rgb)

    # Si se detectan rostros, intentar reconocer a las personas
    for (top, right, bottom, left) in rostros:
        # Obtener los encodings del rostro detectado
        rostro_encoding = face_recognition.face_encodings(imagen_rgb, [(top, right, bottom, left)])[0]

        # Comparar los encodings con los encodings de las personas conocidas
        coincidencias = face_recognition.compare_faces(encodings_conocidos, rostro_encoding)

        nombre = "Desconocido"

        # Verificar si hay alguna coincidencia con las personas conocidas
        if True in coincidencias:
            indice = coincidencias.index(True)
            nombre = nombres_conocidos[indice]

        # Dibujar un rectángulo y el nombre de la persona en el rostro detectado
        cv2.rectangle(imagen, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(imagen, nombre, (left, top - 20), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 1)

    return imagen

# Cargar las imágenes de las personas conocidas y obtener sus encodings
imagen_yo = face_recognition.load_image_file("/Users/ezequielalvarez/Downloads/THIAGO2.jpeg")

encoding_persona = face_recognition.face_encodings(imagen_yo)[0]

# Lista de encodings y nombres de las personas conocidas
encodings_conocidos = [encoding_persona]
nombres_conocidos = ["yo"]



def reconocimiento_facial_en_video():
    captura = cv2.VideoCapture(0)

    while True:
        ret, frame = captura.read()

        if ret:
            frame_con_reconocimiento = reconocimiento_facial(frame, nombres_conocidos, encodings_conocidos)
            cv2.imshow("Reconocimiento Facial", frame_con_reconocimiento)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    captura.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    reconocimiento_facial_en_video()