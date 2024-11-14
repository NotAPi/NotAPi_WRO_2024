import cv2
import numpy as np
import argparse
import imutils

image = cv2.imread("/home/jara/Robotica/OpenCv/Imagenes/fe-001-both.jpg")# Cargar una imagen desde el disco

reduccion = 2 #cuantas veces mas pequeña va a ser la imagen final respecto la entrada
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

# Encontrar contornos en las máscaras rojas y verdes
#Esta función detecta los contornos en una imagen binaria (la máscara red_mask_resized en este caso).
#cv2.RETR_EXTERNAL indica que se obtendrán solo los contornos externos (más externos), ignorando los contornos internos.
#cv2.CHAIN_APPROX_SIMPLE reduce el número de puntos de un contorno, eliminando puntos redundantes y simplificando su forma.
#El resultado de esta función es una lista de contornos (contours_red) y una jerarquía (que se ignora aquí con _).
contours_red, _ = cv2.findContours(red_mask_resized, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours_green, _ = cv2.findContours(green_mask_resized, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


# Función para dibujar contornos y centros
#contours: la lista de contornos a procesar.
#image: la imagen en la que se van a dibujar los contornos y centros.
#color: el color que se usará para dibujar (en formato BGR, por ejemplo (0, 0, 255) para rojo).
def draw_contours_and_centers(contours, image, color):
    for c in contours:#Itera a través de cada contorno c en la lista contours. 
        # Calcular el momento para encontrar el centroide
        M = cv2.moments(c) #Calcula los momentos de imagen de cada contorno c usando cv2.moments(c). Esto da un diccionario M con varios valores de momento (como m00, m10, m01, etc.) que se usan para caracterizar la forma y calcular el centroide.
        if M["m00"] > 100: #area del objeto que le busca el centroide
            cX = int(M["m10"] / M["m00"])#Calcula las coordenadas del centroide (cX, cY) del contorno usando 
            cY = int(M["m01"] / M["m00"])#los momentos M["m10"] y M["m01"], divididos por el área M["m00"].
            # Dibujar el contorno y el centroide
            cv2.drawContours(image, [c], -1, color, 2) #Dibuja el contorno c en la imagen image.
                                                        #El -1 indica que se dibujará todo el contorno.
                                                        #color es el color del contorno.
                                                        #2 es el grosor de la línea del contorno.
            cv2.circle(image, (cX, cY), 3, color, -1)#Dibuja un círculo pequeño (de radio 5) en el centroide (cX, cY) del contorno. -1 significa que el círculo estará relleno.
            cv2.putText(image, "center", (cX - 20, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)#Agrega el texto "center" cerca del centroide, ligeramente desplazado hacia arriba y a la izquierda (cX - 20, cY - 20).
                                                                                                    #cv2.FONT_HERSHEY_SIMPLEX define el tipo de letra.
                                                                                                    #0.5 es el tamaño de la letra.
                                                                                                    #color es el color del texto.
                                                                                                    #2 es el grosor del texto.
            cv2.line(image, (0 , cY), (anchura, cY), color, 1)#Dibuja una línea horizontal de 40 píxeles centrada en el centroide (cX, cY), con color y grosor 2.
            cv2.line(image, (cX, 0), (cX, altura), color, 1)#Los puntos (cX - 20, cY) y (cX + 20, cY) son los extremos de la línea horizontal.

# Dibujar contornos y centros para los objetos rojos y verdes
#Llama a la función draw_contours_and_centers para dibujar los contornos y centros de las figuras rojas y verdes en sus 
#respectivas imágenes redimensionadas (red_object_resized y green_object_resized), 
#usando el color rojo (0, 0, 255) y verde (0, 255, 0) según corresponda.
draw_contours_and_centers(contours_red, red_object_resized, (0, 0, 255))  # Rojo
draw_contours_and_centers(contours_green, green_object_resized, (0, 255, 0))  # Verde

draw_contours_and_centers(contours_red, original_resized, (0, 0, 255))  # Rojo
draw_contours_and_centers(contours_green, original_resized, (0, 255, 0))  # Verde


cv2.imshow('Red Mask', red_mask_resized)
cv2.imshow('Green Mask', green_mask_resized)
cv2.imshow('Red Object', red_object_resized)
cv2.imshow('Green Object', green_object_resized)
cv2.imshow('original', original_resized)
cv2.waitKey(0)
cv2.destroyAllWindows()