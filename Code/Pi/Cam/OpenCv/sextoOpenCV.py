import cv2
import numpy as np

video_path = "/home/jara/Robotica/OpenCv/Imagenes/wro2020-fe-POV2-120d.mp4"
video_path2 = "/home/jara/Robotica/OpenCv/Imagenes/wro2020-fe-POV2-280mm.mp4"
cap = cv2.VideoCapture(video_path)

while True:

    et, frame = cap.read() # Leer un cuadro de la cámara

    image = cv2.resize(frame, (640, 480))

    cv2.waitKey(100) 

    altura, anchura = image.shape[:2]# Obtener las dimensiones de la imagen
    izquierda = anchura//3 
    derecha = 2*anchura//3

    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])
    lower_green = np.array([35, 100, 50])
    upper_green = np.array([85, 255, 255])

    mask_red1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask_red1, mask_red2) 
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)

    def draw_centroids_and_contours(mask, image, color, mask2, color2):

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours2, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        bloque_cercano = -1
        bloque_centro_x = -1  # Coordenada X del bloque más bajo
        bloque_color = None  # Color del bloque más bajo (para dibujar)
        verde = (0,255,0)
        rojo = (0,0,255)

        for contour in contours:
            M = cv2.moments(contour)
            if M["m00"] > 100:  # Ajusta este umbral para ignorar ruido
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
            if M["m00"] > 100:  # Ajusta este umbral para ignorar ruido
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.drawContours(image, [contour], -1, color, 2)
                cv2.circle(image, (cX, cY), 3, color, -1)
                cv2.putText(image, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                cv2.line(image, (0, cY), (image.shape[1], cY), color2, 1)
                cv2.line(image, (cX, 0), (cX, image.shape[0]), color2, 1)


                if cY > bloque_cercano:
                    bloque_cercano = cY
                    bloque_centro_x = cX
                    bloque_color = verde

        if bloque_cercano != -1:
            cv2.line(image, (bloque_centro_x, 0), (bloque_centro_x, image.shape[0]), (255, 0, 255), 2)
            objetivo = 0

            if bloque_color == verde:
                objetivo = anchura

            cv2.arrowedLine(image, (bloque_centro_x,bloque_cercano), (objetivo, bloque_cercano), bloque_color, thickness=5, line_type=cv2.LINE_8, shift=0, tipLength=0.1)


    draw_centroids_and_contours(red_mask, image, (0, 0, 255), green_mask, (0, 255, 0))
    cv2.line(image, (izquierda, 0), (izquierda, altura), (0, 255, 255), 2)
    cv2.line(image, (derecha, 0), (derecha, altura), (0, 255, 255), 2)

    cv2.imshow('Red Mask', red_mask)
    cv2.imshow('Green Mask', green_mask)
    cv2.imshow('original', image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()