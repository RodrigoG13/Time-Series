"""import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

posiciones = [(1, 2), (3, 4), (4, 5), (6, 7), (8, 9)]


x, y = zip(*posiciones)
tiempo = range(len(posiciones))
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

ax.plot(x, y, tiempo, '-o', label='Partícula')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Tiempo')

ax.set_title('Movimiento de la Partícula en el Espacio 2D a lo largo del Tiempo')
ax.legend()

plt.show()
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Definir una función para calcular el número de bins usando el método de Rice
def rice_rule(n):
    return int(np.ceil(2 * (n ** (1/3))))

# Definir la función para plotear el histograma 3D
def plot_3d_histogram(positions):
    # Convertir la lista de tuplas en un array de numpy para facilitar los cálculos
    positions_array = np.array(positions)
    
    # Extraer las coordenadas x e y
    x = positions_array[:, 0]
    y = positions_array[:, 1]
    
    # Calcular el número de bins usando el método de Rice
    bins = rice_rule(len(x))
    
    # Calcular el histograma 2D con los bins calculados
    hist, xedges, yedges = np.histogram2d(x, y, bins=[bins, bins])
    
    # Filtro para asegurarnos de que sólo incluyamos barras con altura no nula
    nonzero = hist != 0
    
    # Preparar los centros de los bins para el plotting
    xpos, ypos = np.meshgrid(xedges[:-1] + np.diff(xedges)/2, yedges[:-1] + np.diff(yedges)/2)
    xpos = xpos[nonzero]
    ypos = ypos[nonzero]
    zpos = 0
    
    # Dimensiones de las barras
    dx = dy = np.ones_like(zpos) * (xedges[1] - xedges[0])
    dz = hist[nonzero]
    
    # Crear la figura y el eje para el plot 3D
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plotear las barras
    ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')
    
    # Etiquetas y título
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Frecuencia')
    plt.title('Histograma 3D de Posiciones')
    
    # Mostrar el plot
    plt.show()

# Datos de ejemplo
positions = [(1, 2), (3, 4), (4, 5), (20, 30)]

# Llamar a la función
plot_3d_histogram(positions)
