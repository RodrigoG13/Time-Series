import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
import random
import threading
import queue
import time
import pandas as pd


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


class Particula(threading.Thread):
    def __init__(self, x, y, z, color, update_queue, lim_x, lim_y, lim_z, id):
        super().__init__()
        distr = "Feigenbaum"
        self.x, self.y, self.z = x, y, z
        self.color = tuple(color)  # Convert color to a tuple to use it as dictionary key
        self.update_queue = update_queue
        self.running = True
        self.lim_x = lim_x
        self.lim_y = lim_y
        self.lim_z = lim_z
        aux = leer_col_csv(f"datos{distr}.csv", "Valores x")
        self.datos = desordenar_lista(aux)

    def run(self):
        while self.running:
            self.move()
            self.update_queue.put((self.x, self.y, self.z, self.color))
            time.sleep(0.1)  # Control particle movement speed

    def move(self):
        val_prueba_dir = self.datos[0]
        self.datos = np.delete(self.datos, 0)
        posicion_random = random.randint(0, len(self.datos))
        self.datos = np.insert(self.datos, posicion_random, val_prueba_dir)
        direction = definir_direccion(np.array_split(self.datos, 26), val_prueba_dir)
        #self.arch_direccion.write(f"{direction},")
        val_prueba_long = self.datos[0]
        self.datos = np.delete(self.datos, 0)
        posicion_random = random.randint(0, len(self.datos))
        self.datos = np.insert(self.datos, posicion_random, val_prueba_long)
        pasos = definir_tam_paso(np.array_split(self.datos, 4), val_prueba_long)
        #self.arch_distancia.write(f"{pasos},")

        bandera_choque = 0

        for _ in range(0, pasos):
            if direction == 0 and self.y > 0:  # Arriba
                self.y -= 1
            elif direction == 1 and self.x < self.lim_x - 1:  # Derecha
                self.x += 1
            elif direction == 2 and self.y < self.lim_y - 1:  # Abajo
                self.y += 1
            elif direction == 3 and self.x > 0:  # Izquierda
                self.x -= 1
            elif direction == 4 and self.z < self.lim_z - 1:  # Adelante
                self.z += 1
            elif direction == 5 and self.z > 0:  # Atrás
                self.z -= 1

            # Combinaciones de dos ejes
            elif direction == 6 and self.y > 0 and self.x < self.lim_x - 1:  # Arriba Derecha
                self.y -= 1
                self.x += 1
            elif direction == 7 and self.y < self.lim_y - 1 and self.x < self.lim_x - 1:  # Abajo Derecha
                self.y += 1
                self.x += 1
            elif direction == 8 and self.y < self.lim_y - 1 and self.x > 0:  # Abajo Izquierda
                self.y += 1
                self.x -= 1
            elif direction == 9 and self.y > 0 and self.x > 0:  # Arriba Izquierda
                self.y -= 1
                self.x -= 1

            # Combinaciones de dos ejes incluyendo Z
            elif direction == 10 and self.y > 0 and self.z > 0:  # Arriba Atrás
                self.y -= 1
                self.z -= 1
            elif direction == 11 and self.y > 0 and self.z < self.lim_z - 1:  # Arriba Adelante
                self.y -= 1
                self.z += 1
            elif direction == 12 and self.x < self.lim_x - 1 and self.z > 0:  # Derecha Atrás
                self.x += 1
                self.z -= 1
            elif direction == 13 and self.x < self.lim_x - 1 and self.z < self.lim_z - 1:  # Derecha Adelante
                self.x += 1
                self.z += 1
            elif direction == 14 and self.y < self.lim_y - 1 and self.z > 0:  # Abajo Atrás
                self.y += 1
                self.z -= 1
            elif direction == 15 and self.y < self.lim_y - 1 and self.z < self.lim_z - 1:  # Abajo Adelante
                self.y += 1
                self.z += 1
            elif direction == 16 and self.x > 0 and self.z > 0:  # Izquierda Atrás
                self.x -= 1
                self.z -= 1
            elif direction == 17 and self.x > 0 and self.z < self.lim_z - 1:  # Izquierda Adelante
                self.x -= 1
                self.z += 1

            # Diagonales completas en tres ejes
            elif direction == 18 and self.x > 0 and self.y > 0 and self.z > 0:  # Arriba Izquierda Atrás
                self.y -= 1
                self.x -= 1
                self.z -= 1
            elif direction == 19 and self.x < self.lim_x - 1 and self.y > 0 and self.z > 0:  # Arriba Derecha Atrás
                self.y -= 1
                self.x += 1
                self.z -= 1
            elif direction == 20 and self.x > 0 and self.y > 0 and self.z < self.lim_z - 1:  # Arriba Izquierda Adelante
                self.y -= 1
                self.x -= 1
                self.z += 1
            elif direction == 21 and self.x < self.lim_x - 1 and self.y > 0 and self.z < self.lim_z - 1:  # Arriba Derecha Adelante
                self.y -= 1
                self.x += 1
                self.z += 1
            elif direction == 22 and self.x > 0 and self.y < self.lim_y - 1 and self.z > 0:  # Abajo Izquierda Atrás
                self.y += 1
                self.x -= 1
                self.z -= 1
            elif direction == 23 and self.x < self.lim_x - 1 and self.y < self.lim_y - 1 and self.z > 0:  # Abajo Derecha Atrás
                self.y += 1
                self.x += 1
                self.z -= 1
            elif direction == 24 and self.x > 0 and self.y < self.lim_y - 1 and self.z < self.lim_z - 1:  # Abajo Izquierda Adelante
                self.y += 1
                self.x -= 1
                self.z += 1
            elif direction == 25 and self.x < self.lim_x - 1 and self.y < self.lim_y - 1 and self.z < self.lim_z - 1:  # Abajo Derecha Adelante
                self.y += 1
                self.x += 1
                self.z += 1

            # Verificar colisiones
            elif self.y == 0:
                bandera_choque = 1
                break
            elif self.x >= self.lim_x - 1:
                bandera_choque = 2
                break
            elif self.y >= self.lim_y - 1:
                bandera_choque = 3
                break
            elif self.z == 0 or self.z >= self.lim_z - 1:
                bandera_choque = 5
                break
            elif self.x == 0:
                bandera_choque = 4
                break

        """self.arch_posiciones.write(f"{self.x},{self.y},{self.z};")
        self.arch_choques_pared.write(f"{bandera_choque},")"""

    def stop(self):
        self.running = False


class Animation3D:
    def __init__(self, update_queue, lim_x, lim_y, lim_z):
        self.update_queue = update_queue
        self.fig, self.ax = plt.subplots(subplot_kw={'projection': '3d'})
        self.ax.set_xlim(0, lim_x)
        self.ax.set_ylim(0, lim_y)
        self.ax.set_zlim(0, lim_z)
        self.lines = {}

    def update(self, frame):
        while not self.update_queue.empty():
            x, y, z, color = self.update_queue.get()
            if color not in self.lines:
                self.lines[color] = self.ax.plot([x], [y], [z], color=color, linewidth=2)[0]
            else:
                line = self.lines[color]
                xd, yd, zd = line.get_data_3d()
                line.set_data_3d(np.append(xd, x), np.append(yd, y), np.append(zd, z))

    def animate(self):
        ani = FuncAnimation(self.fig, self.update, interval=20)
        plt.show()


if __name__ == "__main__":
    
    lim_x = 100
    lim_y = 100
    lim_z = 100

    
    colores_predefinidos = [np.array([0.27606088, 0.74246267, 0.6464469 ]), np.array([0.09161601, 0.75869024, 0.76659079]), 
                            np.array([0.1252212 , 0.05280823, 0.71721886]), np.array([0.77492683, 0.59771033, 0.10067767]), 
                            np.array([0.90620177, 0.24177441, 0.71045307])]
        
    
    print("\t\t\t*** CAMINANTE ALEATORIO ***")
    
    num_caminantes = int(input("\n¿Cuántos caminantes se visualizarán?: "))
    
    
    update_queue = queue.Queue()
    particles = [Particula(random.randint(0, lim_x), random.randint(0, lim_y), random.randint(0, lim_z), colores_predefinidos[id], 
                            update_queue, lim_x, lim_y, lim_z, id) for id in range(1,num_caminantes+1)]

    for particle in particles:
        particle.start()

    animator = Animation3D(update_queue, lim_x, lim_y, lim_z)
    animator.animate()

    for particle in particles:
        particle.stop()
        particle.join()