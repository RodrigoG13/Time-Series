import numpy as np
import pandas as pd
import random
import threading
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def desordenar_lista(lista):
        n = len(lista)
        for i in range(n-1, 0, -1):
            j = random.randint(0, i)
            lista[i], lista[j] = lista[j], lista[i]
        return lista

# Función para leer datos de CSV y regresar un array numpy desordenado
def leer_col_csv(file_path, column_name):
    data = pd.read_csv(file_path)
    return np.random.permutation(data[column_name].values)

# Clase para manejar el espacio 3D
class Map3D:
    def __init__(self, n, m, p):
        self.shape = (n, m, p)
        self.map_matrix = np.zeros(self.shape, dtype=int)  # Usamos un array NumPy para eficiencia

    def update_cell(self, x, y, z, value):
        self.map_matrix[y, x, z] = value  # Asegúrate de acceder con el orden correcto
        
        
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

# Clase para la particula que hereda de Thread
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
        while self.running:
            self.move()
            time.sleep(0.01)  # Ajuste este tiempo según la necesidad de la simulación

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
            elif direction == 1 and self.x < self.map.shape[1] - 1:  # Derecha
                self.x += 1
            elif direction == 2 and self.y < self.map.shape[0] - 1:  # Abajo
                self.y += 1
            elif direction == 3 and self.x > 0:  # Izquierda
                self.x -= 1
            elif direction == 4 and self.z < self.map.shape[2] - 1:  # Adelante
                self.z += 1
            elif direction == 5 and self.z > 0:  # Atrás
                self.z -= 1

            # Combinaciones de dos ejes
            elif direction == 6 and self.y > 0 and self.x < self.map.shape[1] - 1:  # Arriba Derecha
                self.y -= 1
                self.x += 1
            elif direction == 7 and self.y < self.map.shape[0] - 1 and self.x < self.map.shape[1] - 1:  # Abajo Derecha
                self.y += 1
                self.x += 1
            elif direction == 8 and self.y < self.map.shape[0] - 1 and self.x > 0:  # Abajo Izquierda
                self.y += 1
                self.x -= 1
            elif direction == 9 and self.y > 0 and self.x > 0:  # Arriba Izquierda
                self.y -= 1
                self.x -= 1

            # Combinaciones de dos ejes incluyendo Z
            elif direction == 10 and self.y > 0 and self.z > 0:  # Arriba Atrás
                self.y -= 1
                self.z -= 1
            elif direction == 11 and self.y > 0 and self.z < self.map.shape[2] - 1:  # Arriba Adelante
                self.y -= 1
                self.z += 1
            elif direction == 12 and self.x < self.map.shape[1] - 1 and self.z > 0:  # Derecha Atrás
                self.x += 1
                self.z -= 1
            elif direction == 13 and self.x < self.map.shape[1] - 1 and self.z < self.map.shape[2] - 1:  # Derecha Adelante
                self.x += 1
                self.z += 1
            elif direction == 14 and self.y < self.map.shape[0] - 1 and self.z > 0:  # Abajo Atrás
                self.y += 1
                self.z -= 1
            elif direction == 15 and self.y < self.map.shape[0] - 1 and self.z < self.map.shape[2] - 1:  # Abajo Adelante
                self.y += 1
                self.z += 1
            elif direction == 16 and self.x > 0 and self.z > 0:  # Izquierda Atrás
                self.x -= 1
                self.z -= 1
            elif direction == 17 and self.x > 0 and self.z < self.map.shape[2] - 1:  # Izquierda Adelante
                self.x -= 1
                self.z += 1

            # Diagonales completas en tres ejes
            # Aquí agregas las combinaciones para movimientos como Arriba Derecha Adelante, Abajo Izquierda Atrás, etc.
            # Ejemplo de una diagonal en tres ejes:
            elif direction == 18 and self.x > 0 and self.y > 0 and self.z > 0:  # Arriba Izquierda Atrás
                self.y -= 1
                self.x -= 1
                self.z -= 1
            elif direction == 19 and self.x < self.map.shape[1] - 1 and self.y > 0 and self.z > 0:  # Arriba Derecha Atrás
                self.y -= 1
                self.x += 1
                self.z -= 1
            elif direction == 20 and self.x > 0 and self.y > 0 and self.z < self.map.shape[2] - 1:  # Arriba Izquierda Adelante
                self.y -= 1
                self.x -= 1
                self.z += 1
            elif direction == 21 and self.x < self.map.shape[1] - 1 and self.y > 0 and self.z < self.map.shape[2] - 1:  # Arriba Derecha Adelante
                self.y -= 1
                self.x += 1
                self.z += 1
            elif direction == 22 and self.x > 0 and self.y < self.map.shape[0] - 1 and self.z > 0:  # Abajo Izquierda Atrás
                self.y += 1
                self.x -= 1
                self.z -= 1
            elif direction == 23 and self.x < self.map.shape[1] - 1 and self.y < self.map.shape[0] - 1 and self.z > 0:  # Abajo Derecha Atrás
                self.y += 1
                self.x += 1
                self.z -= 1
            elif direction == 24 and self.x > 0 and self.y < self.map.shape[0] - 1 and self.z < self.map.shape[2] - 1:  # Abajo Izquierda Adelante
                self.y += 1
                self.x -= 1
                self.z += 1
            elif direction == 25 and self.x < self.map.shape[1] - 1 and self.y < self.map.shape[0] - 1 and self.z < self.map.shape[2] - 1:  # Abajo Derecha Adelante
                self.y += 1
                self.x += 1
                self.z += 1

            # Verificar colisiones
            elif self.y == 0:
                bandera_choque = 1
                break
            elif self.x >= self.map.shape[1] - 1:
                bandera_choque = 2
                break
            elif self.y >= self.map.shape[0] - 1:
                bandera_choque = 3
                break
            elif self.z == 0 or self.z >= self.map.shape[2] - 1:
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

    def stop(self):
        self.running = False

# Optimización del animador
class Matrix3DAnimator:
    def __init__(self, map3d):
        self.map3d = map3d
        self.fig, self.ax = plt.subplots(subplot_kw={'projection': '3d'})
    
    def update_plot(self, frame):
        self.ax.clear()
        where = np.argwhere(self.map3d.map_matrix > 0)
        for (y, x, z) in where:
            self.ax.scatter(x, y, z, color='blue')  # Simplificación: un solo color

    def animate(self):
        ani = FuncAnimation(self.fig, self.update_plot, frames=1, interval=0.001)
        plt.show()
        

if __name__ == "__main__":
    n, m, p = 300, 300, 300
    game_map = Map3D(n, m, p)
    particulas = [Particula(random.randint(0, m-1), random.randint(0, n-1), random.randint(0, p-1), game_map, id) for id in range(2)]  # Reducir número si es necesario
    for particula in particulas:
        particula.start()

    animator = Matrix3DAnimator(game_map)
    animator.animate()

    for particula in particulas:
        particula.stop()
