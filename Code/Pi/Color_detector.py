import cv2
import numpy as np
import time

# Función para detectar color en una imagen
def detectar_color(frame, lower_bound, upper_bound, color_name, last_detected_time, delay):
    # Convertir la imagen a formato HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Crear una máscara con los límites de color
    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    
    # Encontrar los contornos de las áreas con el color detectado
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    current_time = time.time()
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 500:  # Filtrar contornos pequeños
            x, y, w, h = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, color_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            # Hacer print si ha pasado el tiempo de delay
            if current_time - last_detected_time > delay:
                print(f'Detectado bloque de color {color_name} en la posición: x={x}, y={y}, ancho={w}, alto={h}')
                return current_time
    return last_detected_time

# Capturar video desde la cámara web
cap = cv2.VideoCapture(0)

# Tiempo inicial de detección
last_red_time = time.time()
last_green_time = time.time()

# Definir el delay entre prints (en segundos)
delay = 2.0

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Definir rangos de color con tolerancia reducida para rojo y verde en formato HSV
    lower_red = np.array([159, 50, 70])
    upper_red = np.array([180, 255, 255])
    lower_green = np.array([36, 50, 70])
    upper_green = np.array([89, 155, 155])

    # Detectar colores y actualizar el tiempo de detección
    last_red_time = detectar_color(frame, lower_red, upper_red, "R", last_red_time, delay)
    last_green_time = detectar_color(frame, lower_green, upper_green, "V", last_green_time, delay)

    # Mostrar el frame con los rectángulos de los colores detectados
    cv2.imshow('Detección de Colores', frame)

    # Exit Q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()
