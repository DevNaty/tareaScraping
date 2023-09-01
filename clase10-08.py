import cv2
def detectar_rostros(frame):
    # Cargar el clasificador de cascada para la detección de rostros
    cascada_rostros = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # Convertir el frame a escala de grises (requerimiento del clasificador)
    frame_gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Detectar rostros en el frame
    rostros = cascada_rostros.detectMultiScale(frame_gris, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    # Dibujar rectángulos alrededor de los rostros detectados
    for (x, y, w, h) in rostros:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    return frame
def capturar_y_mostrar():
    # Inicializar la captura de video desde la cámara
    captura = cv2.VideoCapture(0)
    while True:
        # Leer el frame desde la cámara
        ret, frame = captura.read()
        # Si la lectura del frame es exitosa, realizar la detección de rostros
        if ret:
            frame_con_rostros = detectar_rostros(frame)
            # Mostrar el frame con los rostros detectados
            cv2.imshow("Detección de Rostros", frame_con_rostros)
        # Salir del bucle si se presiona la tecla 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    # Liberar la captura de video y cerrar las ventanas
    captura.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    capturar_y_mostrar()







