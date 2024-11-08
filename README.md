# NotAPi_WRO_2024

=================================
##1. Gestión de Movilidad
----------------------------------
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
