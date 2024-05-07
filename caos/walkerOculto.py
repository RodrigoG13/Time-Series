import pygame
import sys
import random
import threading
import time
import datetime
import pandas as pd
import numpy as np


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


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text


    def draw(self, screen, outline=None):
        if outline:
            pygame.draw.rect(screen, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
            
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text = font.render(self.text, 1, (0,0,0))
            screen.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))


    def is_over(self, pos):
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False


class Map:

    def __init__(self, n, m, cell_size):
        self.n = n
        self.m = m
        self.cell_size = cell_size
        self.map_matrix = [[None for _ in range(m)] for _ in range(n)]
        self.images = {}
        self.objetos_config = {
            0: 'azul.jpg',
            1: 'verde.jpg',
            2: 'naranja.jpg',
            3: 'rosa.jpg',
            4: 'blanco.jpg',

            5: 'amarillo.jpg',
            6: 'morado.jpg',
        }


    def load_images(self):
        for obj, img_path in self.objetos_config.items():
            original_image = pygame.image.load(img_path)
            scaled_image = pygame.transform.scale(original_image, (self.cell_size, self.cell_size))
            self.images[obj] = scaled_image


    def update_cell(self, i, j, value):
        self.map_matrix[i][j] = value


    def draw(self, screen):
        for i in range(self.n):
            for j in range(self.m):
                x, y = j * self.cell_size, i * self.cell_size
                cell_value = self.map_matrix[i][j]
                if cell_value in self.images:
                    screen.blit(self.images[cell_value], (x, y))


class Particula(threading.Thread):

    def __init__(self, x, y, map_obj, id):

        distr = "FeigenbaumExponencial"

        super().__init__()
        self.id = id
        self.x = x
        self.y = y
        self.map = map_obj
        self.running = True
        self.paused = False  
        self.pause_cond = threading.Condition(threading.Lock())
        """self.arch_direccion = open(f'direcciones_{distr.lower()}4.txt', 'w+')
        self.arch_distancia = open(f'distancia_{distr.lower()}4.txt', 'w+')
        self.arch_posiciones = open(f'posiciones_{distr.lower()}4.txt', 'w+')
        self.arch_choques_pared = open(f'choques_{distr.lower()}4.txt', 'w+')"""
        """self.arch_direccion = open(f'z.txt', 'w+')
        self.arch_distancia = open(f'z', 'w+')
        self.arch_posiciones = open(f'z', 'w+')"""
        #self.arch_choques_pared = open(f'z.txt', 'w+')
        aux = leer_col_csv(f"datos{distr}.csv", "Valores x")
        #self.datos = desordenar_lista(aux)
        self.datos = aux
        print(self.datos)
        input()


    def algortimo_random_t2(self, valor_minimo, valor_maximo, valor_prueba):
        minimo_lista = min(self.datos)
        maximo_lista = max(self.datos)
        proporcion = ((valor_prueba - minimo_lista) / (maximo_lista - minimo_lista)) * (valor_maximo - valor_minimo) + valor_minimo
        return int(proporcion)


    def algortimo_random_t(self, minimo_nueva_escala, maximo_nueva_escala, valor_prueba):
        minimo_lista = min(self.datos)
        maximo_lista = max(self.datos)
        valor_reescalado = minimo_nueva_escala + ((valor_prueba - minimo_lista) * (maximo_nueva_escala - minimo_nueva_escala) / (maximo_lista - minimo_lista))        
        return int(valor_reescalado)


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
        self.datos = np.delete(self.datos, 0)
        posicion_random = random.randint(0, len(self.datos))
        #posicion_random = len(self.datos) - 5
        self.datos = np.insert(self.datos, posicion_random, val_prueba_dir)
        direction = definir_direccion(np.array_split(self.datos, 8), val_prueba_dir)
        #self.arch_direccion.write(f"{direction},")

        val_prueba_long = self.datos[0]
        self.datos = np.delete(self.datos, 0)
        posicion_random = random.randint(len(self.datos)-1, len(self.datos))
        #posicion_random = len(self.datos) -5
        self.datos = np.insert(self.datos, posicion_random, val_prueba_long)
        pasos = definir_tam_paso(np.array_split(self.datos, 8), val_prueba_long)
        #self.arch_distancia.write(f"{pasos},")

        bandera_choque = 0

        for _ in range(0, pasos):
            if direction == 0 and self.y > 0:  # Arriba
                self.y -= 1
            elif direction == 1 and self.x < self.map.m - 1:  # Izquierda
                self.x += 1
            elif direction == 2 and self.y < self.map.n - 1:  # Abajo
                self.y += 1
            elif direction == 3 and self.x > 0:  # Derecha
                self.x -= 1
            elif direction == 4 and self.y > 0 and self.x < self.map.m - 1:  # Arriba derecha
                self.y -= 1
                self.x += 1
            elif direction == 5 and self.y < self.map.n - 1 and self.x < self.map.m - 1:  # Abajo izquierda
                self.y += 1
                self.x += 1
            elif direction == 6 and self.y < self.map.n - 1 and self.x > 0:  # Abajo derecha
                self.y += 1
                self.x -= 1
            elif direction == 7 and self.y > 0 and self.x > 0:  # Arriba izquierda
                self.y -= 1
                self.x -= 1

            elif self.y == 0:
                bandera_choque = 1
                break

            elif self.x >= self.map.m - 1:
                bandera_choque = 2
                break

            elif self.y >= self.map.n - 1:
                bandera_choque = 3
                break

            elif self.x == 0:
                bandera_choque = 4
                break
            
            self.map.update_cell(self.y, self.x, self.id)

        #self.arch_posiciones.write(f"{self.x},{self.y};")
        #self.arch_choques_pared.write(f"{bandera_choque},")



def init_pygame(window_size):
    pygame.init()
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Simulación del Camino del Borracho")
    return screen


def run_simulation(screen, game_map, particulas):
    black = (0, 0, 0)
    running = True
    button_pause = Button((0, 255, 0), 10, 10, 100, 50, 'Pausa')
    button_seguir = Button((0, 0, 255), 120, 10, 100, 50, 'Sigue')
    button_foto = Button((255, 0, 255), 230, 10, 100, 50, 'Foto')
    
    for particula in particulas:
        particula.start()

    while running:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                for particula in particulas:
                    particula.stop()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button_pause.is_over(pos):
                    for particula in particulas:
                        particula.pause() 
                if button_seguir.is_over(pos):
                    for particula in particulas:
                        particula.continue_running()
                if button_foto.is_over(pos):
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Formato de sello de tiempo
                    screenshot_filename = f"screenshot_{timestamp}.png"
                    pygame.image.save(screen, screenshot_filename)
                    print(f"Captura de pantalla guardada como {screenshot_filename}")
                    
        screen.fill(black)
        game_map.draw(screen)
        button_pause.draw(screen)
        button_seguir.draw(screen)
        button_foto.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


def partir_conjunto(numeros, n_partes):
    archivo = numeros
    paso =  round((max(archivo) - min(archivo)) / n_partes , 4)
    limites = [min(archivo)+paso*i for i in range(n_partes)]
    limites.append(max(archivo))
    return limites


def definir_direccion(intervalos, valor):
    # Asumimos que 'intervalos' es una lista de arrays NumPy y cada array representa un rango
    for i, segmento in enumerate(intervalos):
        if valor in segmento:
            return i
    return None
    
    
def definir_tam_paso(intervalos, valor):
    intervalo = definir_direccion(intervalos, valor)
    return intervalo + 1




if __name__ == "__main__":
    cell_size = 4
    n, m = 200, 400
    window_size = (m * cell_size, n * cell_size)
    
    game_map = Map(n, m, cell_size)
    game_map.load_images()
    
    game_map.update_cell(0, 100, 7)
    usuarios = int(input("Cuantos quieres?: "))
    particulas = [Particula(random.randint(0, m-1), random.randint(0, n-1), game_map, id) for id in range(usuarios)]
    screen = init_pygame(window_size)
    run_simulation(screen, game_map, particulas)