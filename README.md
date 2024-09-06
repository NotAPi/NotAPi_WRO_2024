# NotAPi_WRO_2024

Videos:

[1](https://youtu.be/j8WViXHHoxo)

[2](https://youtu.be/NUMMYUzFL58)

1. Gestión de Movilidad
Selección y Implementación de Componentes:
Hemos utilizado tres sensores ultrasónicos para la detección de obstáculos, ubicados uno en cada lado y otro en la parte delantera del vehículo. Para la tracción, hemos incorporado un motor de corriente continua de alto rendimiento. La tracción delantera se logra mediante una configuración de ruedas motrices. El vehículo base es un coche RC de dimensiones 15 x 8 cm, al que hemos realizado numerosas modificaciones para adaptarlo a nuestras necesidades.

Uso de Controlador y Microcontrolador:
El controlador de motor utilizado es el L298N, que nos proporciona la capacidad de controlar la velocidad y dirección del motor de tracción. Para el procesamiento de la información de los sensores y el control del sistema, hemos optado por el Arduino R4. Este microcontrolador nos brinda la flexibilidad necesaria para implementar algoritmos de control avanzados.

Personalización del Vehículo:
Se ha modificado significativamente el vehículo original agregando una base impresa en 3D. Esta base proporciona soporte estructural y alojamiento para los componentes electrónicos adicionales. Además, hemos integrado un mini servo para el control de dirección, lo que nos permite una maniobrabilidad precisa en situaciones complicadas.

Fuente de Alimentación:
El vehículo se alimenta mediante una batería LiPo de 2 celdas, que ofrece una combinación óptima de capacidad y densidad de energía. Esta elección nos proporciona una autonomía adecuada para realizar las pruebas y desafíos previstos.

2. Gestión de Obstáculos
Estrategia de Navegación:
Nuestra estrategia de navegación se basa en la información recopilada por los sensores ultrasónicos. Utilizamos algoritmos de evasión de obstáculos para tomar decisiones rápidas y seguras en entornos dinámicos. La lógica de control se implementa en el Arduino R4, que procesa los datos de los sensores y genera comandos para el controlador de motor y servo de dirección.

3. Utilización de GitHub
Hemos creado un repositorio en GitHub llamado "NotAPi_WRO_2024" donde documentamos nuestro progreso, incluyendo el código fuente, diseños CAD, y registros de reuniones. Realizamos commits regulares para mantener un historial de versiones y facilitar la colaboración entre los miembros del equipo.

4. Fotos del Proyecto en la carpeta "Pictures"
5. Video de Desempeño en la carpeta "Pictures"

6. Factor de Ingeniería
Hemos realizado numerosas modificaciones al vehículo original, incluida la impresión en 3D de soportes para componentes y la integración de nuevos sistemas de control. Nuestro enfoque de ingeniería personalizada nos ha permitido adaptar el vehículo a nuestras necesidades específicas y maximizar su rendimiento en el desafío.

7. Impresión General de los Jueces
Nuestra documentación en GitHub está bien organizada y completa, lo que facilita la comprensión de nuestro diseño y proceso de desarrollo. La comunicación clara y detallada asegura que nuestros esfuerzos puedan ser fácilmente replicados por otros equipos.


________________________________________________________


1. Mobility Management Component Selection and Implementation: We have utilized three ultrasonic sensors for obstacle detection, positioned one on each side and one at the front of the vehicle. For traction, we have incorporated a high-performance direct current motor. Front-wheel drive is achieved through a configuration of drive wheels. The base vehicle is an RC car with dimensions of 15 x 8 cm, to which we have made numerous modifications to adapt it to our needs.

Usage of Controller and Microcontroller: The motor controller used is the L298N, which provides us with the ability to control the speed and direction of the traction motor. For processing sensor information and system control, we have opted for the Arduino R4. This microcontroller gives us the necessary flexibility to implement advanced control algorithms.

Vehicle Customization: The original vehicle has been significantly modified by adding a 3D-printed base. This base provides structural support and housing for additional electronic components. Additionally, we have integrated a mini servo for steering control, allowing for precise maneuverability in challenging situations.

Power Source: The vehicle is powered by a 2-cell LiPo battery, which offers an optimal combination of capacity and energy density. This choice provides us with adequate autonomy to conduct planned tests and challenges.

2. Obstacle Management Navigation Strategy: Our navigation strategy is based on information collected by the ultrasonic sensors. We utilize obstacle avoidance algorithms to make quick and safe decisions in dynamic environments. Control logic is implemented in the Arduino R4, which processes sensor data and generates commands for the motor controller and steering servo.

3. Utilization of GitHub: We have created a repository on GitHub named "NotAPi_WRO_2024" where we document our progress, including source code, CAD designs, and meeting logs. We make regular commits to maintain a version history and facilitate collaboration among team members.

4. Project Media in the "Pictures" Folder: Photos of the project and a performance video are available in the "Pictures" folder.

5. Engineering Factor: We have made numerous modifications to the original vehicle, including 3D printing supports for components and integrating new control systems. Our customized engineering approach has allowed us to adapt the vehicle to our specific needs and maximize its performance in the challenge.

6. Overall Judges' Impression: Our documentation on GitHub is well-organized and comprehensive, facilitating understanding of our design and development process. Clear and detailed communication ensures that our efforts can be easily replicated by other teams.

# NotAPi Autonomous Car Project

## Overview
This project is focused on developing a small autonomous car based on the K989 drift car model. Our team, NotAPi, has been working on this since January, and the main goal is to create a vehicle that can navigate through a course while avoiding obstacles using a combination of sensors and machine vision.

### Specifications
- **Base Car Model**: K989 Drift Car
- **Dimensions**: 15 cm x 8 cm
- **Modifications**:
  - Removed original electronics, except for the motor.
  - Replaced the servo with a custom setup.
  - Added a 3D-printed base for mounting components.

### Components
- **Arduino R4 WiFi**: Controls and processes data from sensors.
- **Raspberry Pi**: Manages camera input and obstacle detection.
- **Voltage Regulators**:
  - 5V for the Arduino and other peripherals.
  - 6V for the motor control.
- **L298N Motor Driver**: Controls the car's single motor.
- **Ultrasonic Sensors**: Three sensors are used to detect obstacles and ensure safe navigation.
- **Camera**: Mounted at the front, controlled by the Raspberry Pi, to identify green and red obstacles.

### Functionality
The autonomous car is programmed to:
- Avoid green and red block obstacles.
- Navigate a predefined course with walls.
- Use ultrasonic sensors for proximity detection.
- Leverage the Raspberry Pi's camera for visual obstacle recognition.

### Assembly and Setup
1. Mount the Arduino R4 WiFi and the Raspberry Pi on the 3D-printed base.
2. Connect the motor to the L298N motor driver.
3. Wire the ultrasonic sensors to the Arduino.
4. Install the camera on the front and link it to the Raspberry Pi.
5. Set up the voltage regulators (5V and 6V) for proper power distribution.

### Installation and Dependencies
1. Install the necessary libraries for Arduino (e.g., NewPing for ultrasonic sensors).
2. Set up the Raspberry Pi for camera control and obstacle detection.
3. Upload the code to the Arduino and Raspberry Pi.
4. Calibrate the sensors and motor control based on the environment.

### Usage
Once everything is set up and powered, place the car on the track. The car will automatically detect and avoid obstacles while following the path.

## Team
NotAPi
