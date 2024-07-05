Instrucciones de uso del simulador:

Desde semiconductor.py se carga todo

1. Crear instancia para la clase *detector*, define las dimensiones y características del detector, por orden: 
- Número de canales: número total de strips en el detector.
- Ancho de los canales: anchura de cada strip (se asume que no hay separación entre strips y toda la superficie es detectora).
- Profundidad del detector
- Anchura de las layers: las layers son las superficies en las que se producen los eventos de producción de carga, cuanto más juntas "más veces interactúa la partícula entrante con el detector"
- Número de partículas: número de partículas que entran dentro del detector

2. Simular las condiciones de entrada de las partículas, se puede modificar tanto el punto de entrada como el ángulo, se asumen trayectorias rectas. Hay varias opciones, por defecto se asumen puntos de entrada y ángulos aleatorios. Ver demás opciones en detector.py

3. El método **matriztrayectoria** genera una matriz con la posición de todos los eventos de producción de carga que genera cada una de las partículas. El método **divisor** utiliza esta matriz y los parámetros de la distribución de carga generada (gaussiana por defecto --> desviación estándar, altura) para generar un histograma donde se recoge en cada canal la carga total generada por el paso de una partícula. NOTA: cada fila recoge la carga TOTAL generada por todos los eventos producidos por una partícula, no la carga producida por cada evento.

4. Plots; tres tipos de plots, cada tipo presenta distintas opciones (mirar detector.py):
- Pintar las trayectorias rectas de cada partícula, cada punto es la intersección de la trayectoria y las layers (posición de los eventos).
- Pintar la carga acumulada en cada en cada canal por el paso de una partícula (carga frente a posición).
- Pintar la evolución de la carga en cada canal tras el sucesivo paso de las partículas (carga frente a tiempo)