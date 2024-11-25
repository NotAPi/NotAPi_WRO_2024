import cv2
import numpy as np
import argparse
import imutils

# Iniciar la captura de video desde la cámara (0 es el índice de la cámara principal)
video_path = "/home/jara/Robotica/OpenCv/Imagenes/wro2020-fe-POV2-120d.mp4"
cap = cv2.VideoCapture(video_path)

#image = cv2.imread("/home/jara/Robotica/OpenCv/Imagenes/volanvoAlCIRIO.JPG")# Cargar una imagen desde el disco





while True:
    # Leer un cuadro de la cámara
    ret, frame = cap.read()

    
    image = cv2.resize(frame, (640, 480))
    

    cv2.waitKey(0)

    reduccion = 1 #cuantas veces mas pequeña va a ser la imagen final respecto la entrada
    altura, anchura = image.shape[:2]# Obtener las dimensiones de la imagen
    izquierda = (anchura//reduccion)//3 
    derecha = 2*(anchura//reduccion)//3
    abajo = altura//reduccion
    color = (0, 255, 255)  # amarillo chillon, Definir el color (amarillo, en formato BGR)


    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)# Convert the image from BGR to HSV

    # Define HSV range for red
    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([179, 255, 255])

    # Define HSV range for green
    lower_green = np.array([35, 100, 50])
    upper_green = np.array([85, 255, 255])


    # Create masks for the red range
    mask_red1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask_red2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
    red_mask = cv2.bitwise_or(mask_red1, mask_red2)  # Combine both masks for red

    # Create a mask for the green range
    green_mask = cv2.inRange(hsv_image, lower_green, upper_green)


    # Filter the red and green areas in the image
    red_object = cv2.bitwise_and(image, image, mask=red_mask)
    green_object = cv2.bitwise_and(image, image, mask=green_mask)
    # Resize the masks and objects to 1/5 of their original size
    red_mask_resized = cv2.resize(red_mask, (anchura // reduccion, altura // reduccion))
    green_mask_resized = cv2.resize(green_mask, (anchura // reduccion, altura // reduccion))
    red_object_resized = cv2.resize(red_object, (anchura // reduccion, altura // reduccion))
    green_object_resized = cv2.resize(green_object, (anchura // reduccion, altura // reduccion))
    original_resized = cv2.resize(image, (anchura // reduccion, altura // reduccion))


    

    # Función para dibujar los centroides y contornos de múltiples objetos
    def draw_centroids_and_contours(mask, image, color, mask2, color2):
        # Encontrar contornos en la máscara
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours2, _ = cv2.findContours(mask2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


        # Variable para rastrear el bloque más bajo
        bloque_cercano = -1
        bloque_centro_x = -1  # Coordenada X del bloque más bajo
        bloque_color = None  # Color del bloque más bajo (para dibujar)


        for contour in contours:
            # Calcular los momentos de cada contorno
            M = cv2.moments(contour)
            

            # Solo calcular el centroide y dibujar el contorno si el área es significativa
            if M["m00"] > 100:  # Ajusta este umbral para ignorar ruido
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                
                 # Verificar si este contorno está más abajo que el actual bloque más bajo
                if cY > bloque_cercano:
                    bloque_cercano = cY
                    bloque_centro_x = cX


                # Dibujar el contorno
                cv2.drawContours(image, [contour], -1, color, 2)  # Grosor del contorno: 2
                
                # Dibujar el centroide en la imagen
                cv2.circle(image, (cX, cY), 3, color, -1)
                cv2.putText(image, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                
                # Dibujar las líneas cruzadas en el centroide
                cv2.line(image, (0, cY), (image.shape[1], cY), color, 1)
                cv2.line(image, (cX, 0), (cX, image.shape[0]), color, 1)

        for contour in contours2:
            # Calcular los momentos de cada contorno
            M = cv2.moments(contour)
            

            # Solo calcular el centroide y dibujar el contorno si el área es significativa
            if M["m00"] > 100:  # Ajusta este umbral para ignorar ruido
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                
                 # Verificar si este contorno está más abajo que el actual bloque más bajo
                if cY > bloque_cercano:
                    bloque_cercano = cY
                    bloque_centro_x = cX


                # Dibujar el contorno
                cv2.drawContours(image, [contour], -1, color2, 2)  # Grosor del contorno: 2
                
                # Dibujar el centroide en la imagen
                cv2.circle(image, (cX, cY), 3, color2, -1)
                cv2.putText(image, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color2, 2)
                
                # Dibujar las líneas cruzadas en el centroide
                cv2.line(image, (0, cY), (image.shape[1], cY), color2, 1)
                cv2.line(image, (cX, 0), (cX, image.shape[0]), color2, 1)
        
        
        
        # Dibujar una línea amarilla en el bloque más bajo
        if bloque_cercano != -1:
            cv2.line(image, (bloque_centro_x, 0), (bloque_centro_x, image.shape[0]), (255, 0, 255), 2)

    # Usar la función para calcular y dibujar los centroides y contornos
    draw_centroids_and_contours(red_mask_resized, original_resized, (0, 0, 255), green_mask_resized, (0, 255, 0))  # Rojo
    #draw_centroids_and_contours(green_mask_resized, original_resized, (0, 255, 0))  # Verde

    cv2.line(original_resized, (izquierda, 0), (izquierda, abajo), color, 2)
    cv2.line(original_resized, (derecha, 0), (derecha, abajo), color, 2)

    cv2.imshow('Red Mask', red_mask_resized)
    cv2.imshow('Green Mask', green_mask_resized)
    cv2.imshow('Red Object', red_object_resized)
    cv2.imshow('Green Object', green_object_resized)
    cv2.imshow('original', original_resized)

    # Presiona 'q' para salir del bucle y cerrar la ventana
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar las ventanas
cap.release()
cv2.destroyAllWindows()

