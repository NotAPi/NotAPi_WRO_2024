import cv2
import numpy as np
from picamera2 import Picamera2
import time

# Initialize the Raspberry Pi camera
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"size": (640, 480)}))
picam2.start()

# Allow the camera to warm up
time.sleep(0.1)

while True:
    image_bgr = picam2.capture_array()

    # Swap the red and blue channels
    image = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

    cv2.waitKey(1) 

    altura, anchura = image.shape[:2]  # Obtener las dimensiones de la imagen
    p1_izquierda = (anchura // 3, 0) 
    p2_izquierda = (0, altura)
    p1_derecha = (2 * anchura // 3, 0) 
    p2_derecha = (anchura, altura) 

    hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
    lower_red1 = np.array([115, 100, 100])
    upper_red1 = np.array([160, 255, 255])
    #lower_red2 = np.array([160, 100, 100])
    #upper_red2 = np.array([179, 255, 255])
    lower_green = np.array([20, 100, 50])
    upper_green = np.array([70, 255, 255])

    #mask_red1 = cv2.inRange(hsv_image, lower_red1, upper_red1)xd
    #mask_red2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
    #red_mask = cv2.bitwise_or(mask_red1, mask_red2) 
    red_mask = cv2.inRange(hsv_image, lower_red1, upper_red1)
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

    def draw_centroids_and_contours(mask, image, color, mask2, color2):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours2, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        bloque_cercano = -1
        bloque_centro_x = -1  # Coordenada X del bloque más bajo
        bloque_color = None  # Color del bloque más bajo (para dibujar)
        verde = (0, 255, 0)
        rojo = (0, 0, 255)

        for contour in contours:
            M = cv2.moments(contour)
            if M["m00"] > 200:  # Ajusta este umbral para ignorar ruido area de los bloques
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.drawContours(image, [contour], -1, color, 2)
                cv2.circle(image, (cX, cY), 3, color, -1)
                cv2.putText(image, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                cv2.line(image, (0, cY), (image.shape[1], cY), color, 1)
                cv2.line(image, (cX, 0), (cX, image.shape[0]), color, 1)


                if cY > bloque_cercano:
                    bloque_cercano = cY
                    bloque_centro_x = cX
                    bloque_color = rojo
        
        for contour in contours2:
            M = cv2.moments(contour)
            if M["m00"] > 200:  # Ajusta este umbral para ignorar ruido area de los bloques
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.drawContours(image, [contour], -1, color2, 2)
                cv2.circle(image, (cX, cY), 3, color2, -1)
                cv2.putText(image, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color2, 2)
                cv2.line(image, (0, cY), (image.shape[1], cY), color2, 1)
                cv2.line(image, (cX, 0), (cX, image.shape[0]), color2, 1)


                if cY > bloque_cercano:
                    bloque_cercano = cY
                    bloque_centro_x = cX
                    bloque_color = verde

        if bloque_cercano != -1:
            cv2.line(image, (bloque_centro_x, 0), (bloque_centro_x, image.shape[0]), (255, 0, 255), 2)

            if bloque_color == rojo:
                # Intersección con la línea izquierda
                x_interseccion_izq = p1_izquierda[0] + ((bloque_cercano - p1_izquierda[1]) / (p2_izquierda[1] - p1_izquierda[1])) * (p2_izquierda[0] - p1_izquierda[0]) #calculla 
                objetivo = int(x_interseccion_izq)
            else:
                # Intersección con la línea derecha
                x_interseccion_der = p1_derecha[0] + ((bloque_cercano - p1_derecha[1]) / (p2_derecha[1] - p1_derecha[1])) * (p2_derecha[0] - p1_derecha[0])
                objetivo = int(x_interseccion_der)

            

            cv2.arrowedLine(image, (bloque_centro_x,bloque_cercano), (objetivo, bloque_cercano), bloque_color, thickness=5, line_type=cv2.LINE_8, shift=0, tipLength=0.1)


    draw_centroids_and_contours(red_mask, image, (0, 0, 255), green_mask, (0, 255, 0))
    cv2.line(image, p1_izquierda, p2_izquierda, (0, 255, 255), 2)
    cv2.line(image, p1_derecha, p2_derecha, (0, 255, 255), 2)

    cv2.imshow('Red Mask', red_mask)
    cv2.imshow('Green Mask', green_mask)
    cv2.imshow('original', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()