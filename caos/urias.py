import pygame
import sys
import random
import threading
import time
import datetime
import pandas as pd
import numpy as np
from vispy import scene
from vispy.scene import visuals
import plotly.graph_objects as go
import numpy as np
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D

"""def cargar_set(archivo):
    with open(archivo, 'r') as file:
        contenido = file.read()
    numeros_str = contenido.split(',')
    numeros_enteros = [float(numero) for numero in numeros_str]
    return numeros_enteros"""
    

def leer_col_csv(file_path, column_name):
    data = pd.read_csv(file_path)
    column_data = data[column_name]
    aux = np.array(column_data)
    return aux


def desordenar_lista(lista):
        n = len(lista)
        for i in range(n-1, 0, -1):
            j = random.randint(0, i)
            lista[i], lista[j] = lista[j], lista[i]
        return lista



class Map3D:
    def __init__(self, n, m, p, cell_size):
        self.n = n
        self.m = m
        self.p = p
        self.cell_size = cell_size
        self.map_matrix = np.array([[[None for _ in range(p)] for _ in range(m)] for _ in range(n)])

    def update_cell(self, i, j, k, value):
        self.map_matrix[i][j][k] = value


class Particula(threading.Thread):

    def __init__(self, x, y, z, map_obj, id):

        distr = "Feigenbaum"

        super().__init__()
        
        self.id = id
        self.x = x
        self.y = y
        self.z = z
        self.map = map_obj
        self.running = True
        self.paused = False  
        self.pause_cond = threading.Condition(threading.Lock())
        self.arch_direccion = open(f'direcciones_{distr.lower()}1.txt', 'w+')
        self.arch_distancia = open(f'distancia_{distr.lower()}1.txt', 'w+')
        self.arch_posiciones = open(f'posiciones_{distr.lower()}1.txt', 'w+')
        self.arch_choques_pared = open(f'choques_{distr.lower()}1.txt', 'w+')
        aux = leer_col_csv(f"datos{distr}.csv", "Valores x")
        self.datos = desordenar_lista(aux)


    def run(self):

        bonito = 0.01
        rapidote = 0.0001

        while self.running:
            with self.pause_cond:
                while self.paused:
                    self.pause_cond.wait()
                self.move()
            time.sleep(rapidote)  


    def pause(self):
        self.paused = True


    def continue_running(self):
        with self.pause_cond:
            self.paused = False
            self.pause_cond.notify()  


    def stop(self):
        self.running = False


    def move(self):
        val_prueba_dir = self.datos[0]
        
        #no
        self.datos = np.delete(self.datos, 0)
        
        posicion_random = random.randint(0, len(self.datos))
        
        #no
        self.datos = np.insert(self.datos, posicion_random, val_prueba_dir)
        
        #aqui se ponen las direcciones disponibles
        direction = definir_direccion(np.array_split(self.datos, 26), val_prueba_dir)
        
        #no
        self.arch_direccion.write(f"{direction},")

        val_prueba_long = self.datos[0]
        self.datos = np.delete(self.datos, 0)
        posicion_random = random.randint(0, len(self.datos))
        self.datos = np.insert(self.datos, posicion_random, val_prueba_long)
        pasos = definir_tam_paso(np.array_split(self.datos, 8), val_prueba_long)
        self.arch_distancia.write(f"{pasos},")

        bandera_choque = 0

        for _ in range(0, pasos):
            if direction == 0 and self.y > 0:  # Arriba
                self.y -= 1
            elif direction == 1 and self.x < self.map.m - 1:  # Derecha
                self.x += 1
            elif direction == 2 and self.y < self.map.n - 1:  # Abajo
                self.y += 1
            elif direction == 3 and self.x > 0:  # Izquierda
                self.x -= 1
            elif direction == 4 and self.z < self.map.p - 1:  # Adelante
                self.z += 1
            elif direction == 5 and self.z > 0:  # Atrás
                self.z -= 1

            # Combinaciones de dos ejes
            elif direction == 6 and self.y > 0 and self.x < self.map.m - 1:  # Arriba Derecha
                self.y -= 1
                self.x += 1
            elif direction == 7 and self.y < self.map.n - 1 and self.x < self.map.m - 1:  # Abajo Derecha
                self.y += 1
                self.x += 1
            elif direction == 8 and self.y < self.map.n - 1 and self.x > 0:  # Abajo Izquierda
                self.y += 1
                self.x -= 1
            elif direction == 9 and self.y > 0 and self.x > 0:  # Arriba Izquierda
                self.y -= 1
                self.x -= 1

            # Combinaciones de dos ejes incluyendo Z
            elif direction == 10 and self.y > 0 and self.z > 0:  # Arriba Atrás
                self.y -= 1
                self.z -= 1
            elif direction == 11 and self.y > 0 and self.z < self.map.p - 1:  # Arriba Adelante
                self.y -= 1
                self.z += 1
            elif direction == 12 and self.x < self.map.m - 1 and self.z > 0:  # Derecha Atrás
                self.x += 1
                self.z -= 1
            elif direction == 13 and self.x < self.map.m - 1 and self.z < self.map.p - 1:  # Derecha Adelante
                self.x += 1
                self.z += 1
            elif direction == 14 and self.y < self.map.n - 1 and self.z > 0:  # Abajo Atrás
                self.y += 1
                self.z -= 1
            elif direction == 15 and self.y < self.map.n - 1 and self.z < self.map.p - 1:  # Abajo Adelante
                self.y += 1
                self.z += 1
            elif direction == 16 and self.x > 0 and self.z > 0:  # Izquierda Atrás
                self.x -= 1
                self.z -= 1
            elif direction == 17 and self.x > 0 and self.z < self.map.p - 1:  # Izquierda Adelante
                self.x -= 1
                self.z += 1

            # Diagonales completas en tres ejes
            # Aquí agregas las combinaciones para movimientos como Arriba Derecha Adelante, Abajo Izquierda Atrás, etc.
            # Ejemplo de una diagonal en tres ejes:
            elif direction == 18 and self.x > 0 and self.y > 0 and self.z > 0:  # Arriba Izquierda Atrás
                self.y -= 1
                self.x -= 1
                self.z -= 1
            elif direction == 19 and self.x < self.map.m - 1 and self.y > 0 and self.z > 0:  # Arriba Derecha Atrás
                self.y -= 1
                self.x += 1
                self.z -= 1
            elif direction == 20 and self.x > 0 and self.y > 0 and self.z < self.map.p - 1:  # Arriba Izquierda Adelante
                self.y -= 1
                self.x -= 1
                self.z += 1
            elif direction == 21 and self.x < self.map.m - 1 and self.y > 0 and self.z < self.map.p - 1:  # Arriba Derecha Adelante
                self.y -= 1
                self.x += 1
                self.z += 1
            elif direction == 22 and self.x > 0 and self.y < self.map.n - 1 and self.z > 0:  # Abajo Izquierda Atrás
                self.y += 1
                self.x -= 1
                self.z -= 1
            elif direction == 23 and self.x < self.map.m - 1 and self.y < self.map.n - 1 and self.z > 0:  # Abajo Derecha Atrás
                self.y += 1
                self.x += 1
                self.z -= 1
            elif direction == 24 and self.x > 0 and self.y < self.map.n - 1 and self.z < self.map.p - 1:  # Abajo Izquierda Adelante
                self.y += 1
                self.x -= 1
                self.z += 1
            elif direction == 25 and self.x < self.map.m - 1 and self.y < self.map.n - 1 and self.z < self.map.p - 1:  # Abajo Derecha Adelante
                self.y += 1
                self.x += 1
                self.z += 1

            # Verificar colisiones
            elif self.y == 0:
                bandera_choque = 1
                break
            elif self.x >= self.map.m - 1:
                bandera_choque = 2
                break
            elif self.y >= self.map.n - 1:
                bandera_choque = 3
                break
            elif self.z == 0 or self.z >= self.map.p - 1:
                bandera_choque = 5
                break
            elif self.x == 0:
                bandera_choque = 4
                break

            # Actualizar la celda actual en el mapa
            self.map.update_cell(self.y, self.x, self.z, self.id)
            
            #print('pasito',self.id,direction)

        self.arch_posiciones.write(f"{self.x},{self.y},{self.z};")
        self.arch_choques_pared.write(f"{bandera_choque},")





def init_pygame(window_size):
    pygame.init()
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Simulación del Camino del Borracho")
    return screen


def run_simulation(particulas):
    black = (0, 0, 0)
    running = True
    
    for particula in particulas:
        particula.start()
    
    print('van bien')
    


def partir_conjunto(numeros, n_partes):
    archivo = numeros
    paso =  round((max(archivo) - min(archivo)) / n_partes , 4)
    limites = [min(archivo)+paso*i for i in range(n_partes)]
    limites.append(max(archivo))
    return limites


def definir_direccion(intervalos, valor):
    for i, segmento in enumerate(intervalos):
        if valor in segmento:
            return i
    return None
    
    
def definir_tam_paso(intervalos, valor):
    intervalo = definir_direccion(intervalos, valor)
    return intervalo + 1


class Matrix3DAnimator:
    def __init__(self, matrix, color_map):
        self.matrix = matrix
        self.color_map = color_map
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim(0, matrix.shape[1])
        self.ax.set_ylim(0, matrix.shape[0])
        self.ax.set_zlim(0, matrix.shape[2])

    def update_plot(self, frame):
        self.ax.clear()  # Limpia el gráfico para evitar superposición de puntos
        self.ax.set_xlim(0, self.matrix.shape[1])
        self.ax.set_ylim(0, self.matrix.shape[0])
        self.ax.set_zlim(0, self.matrix.shape[2])

        # Iterar sobre cada elemento en la matriz 3D
        for i in range(self.matrix.shape[0]):
            for j in range(self.matrix.shape[1]):
                for k in range(self.matrix.shape[2]):
                    if self.matrix[i, j, k] is not None and self.matrix[i, j, k] > 0:
                        color = self.color_map[self.matrix[i, j, k]]
                        self.ax.scatter(j, i, k, color=color, marker='o')  # Poner un punto por cada no None

    def animate(self):
        ani = FuncAnimation(self.fig, self.update_plot, frames=np.arange(500), interval=1)
        plt.show()


from vispy import scene
from vispy.scene import visuals
import numpy as np

from vispy.color import Color

class Vispy3DAnimator:
    def __init__(self, map_matrix, color_map):
        # Crear un canvas con una vista de escena
        self.canvas = scene.SceneCanvas(keys='interactive', show=True)
        self.view = self.canvas.central_widget.add_view()

        # Configurar la cámara en modo 'arcball' para facilitar la interacción 3D
        self.view.camera = scene.cameras.ArcballCamera(fov=60)
        
        # Almacenar la matriz del mapa y el mapa de colores
        self.map_matrix = map_matrix
        self.color_map = color_map

        # Crear un objeto Scatter3D para los puntos
        self.scatter = visuals.Markers()
        
        # Añadir el objeto Scatter3D a la vista
        self.view.add(self.scatter)

    def update(self):
        # Preparar datos para la visualización
        coords = []
        colors = []
        for i in range(self.map_matrix.shape[0]):
            for j in range(self.map_matrix.shape[1]):
                for k in range(self.map_matrix.shape[2]):
                    if self.map_matrix[i, j, k] is not None:
                        coords.append([j, i, k])  # Asegúrate de que las coordenadas se ajusten según tus necesidades
                        # Convertir color hexadecimal a RGBA
                        color = Color(self.color_map[self.map_matrix[i, j, k]]).rgba
                        colors.append(color)

        # Actualizar los datos del Scatter3D
        self.scatter.set_data(np.array(coords), edge_color=None, face_color=np.array(colors), size=5)

    def show(self):
        # Mostrar el canvas
        self.canvas.app.run()




if __name__ == "__main__":
    cell_size = 2
    n, m, p = 300, 300, 300
    window_size = (m * cell_size, n * cell_size)
    color_dict = {0: '#6a329f', 1: '#f44336', 2: '#8fce00', 3: '#f1c232', 4: '#32f1e3', 5: '#f19132', 6: '#000000'}
    
    game_map = Map3D(n, m, p, cell_size)
    
    game_map.update_cell(0, 0, 0, 3)
    usuarios = int(input("Cuantos quieres?: "))
    particulas = [Particula(random.randint(0, m-1), random.randint(0, n-1), random.randint(0, p-1), game_map, id) for id in range(usuarios)]
    run_simulation(particulas)
    #print(game_map.map_matrix)
    # Suponemos que game_map.map_matrix y color_dict están definidos como antes
    animator = Matrix3DAnimator(game_map.map_matrix, color_dict)
    animator.animate()
    """animator.update()  # Cargar datos para la visualización
    animator.show()"""