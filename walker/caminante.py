import pygame
import sys
import random
import threading
import time
import datetime 

def cargar_set(archivo):
    with open(archivo, 'r') as file:
        contenido = file.read()
    numeros_str = contenido.split(',')
    numeros_enteros = [float(numero) for numero in numeros_str]
    return numeros_enteros

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
        # Pos is the mouse position or a tuple of (x,y) coordinates
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
            0: 'blanco.jpg', # Asegúrate de tener una imagen para cada partícula
            1: 'azul.jpg',
            2: 'verde.jpg',
            3: 'naranja.jpg',
            4: 'rosa.jpg',
            5: 'morado.jpg',
            6: 'negro.jpg',
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
        super().__init__()
        self.id = id
        self.x = x
        self.y = y
        self.map = map_obj
        self.running = True
        self.paused = False  
        self.pause_cond = threading.Condition(threading.Lock())

    def run(self):
        while self.running:
            with self.pause_cond:
                while self.paused:
                    self.pause_cond.wait()

                self.move()
            time.sleep(0.001)  

    def pause(self):
        self.paused = True

    def continue_running(self):
        with self.pause_cond:
            self.paused = False
            self.pause_cond.notify()  

    def stop(self):
        self.running = False


    def move(self):
        direction = random.randint(0, 7)
        pasos = random.randint(1, 5)
        
        for _ in range(0, pasos):
            if direction == 0 and self.y > 0:  # Norte
                self.y -= 1
            elif direction == 1 and self.x < self.map.m - 1:  # Este
                self.x += 1
            elif direction == 2 and self.y < self.map.n - 1:  # Sur
                self.y += 1
            elif direction == 3 and self.x > 0:  # Oeste
                self.x -= 1
            elif direction == 4 and self.y > 0 and self.x < self.map.m - 1:  # Noreste
                self.y -= 1
                self.x += 1
            elif direction == 5 and self.y < self.map.n - 1 and self.x < self.map.m - 1:  # Sureste
                self.y += 1
                self.x += 1
            elif direction == 6 and self.y < self.map.n - 1 and self.x > 0:  # Suroeste
                self.y += 1
                self.x -= 1
            elif direction == 7 and self.y > 0 and self.x > 0:  # Noroeste
                self.y -= 1
                self.x -= 1

            self.map.update_cell(self.y, self.x, self.id)




def init_pygame(window_size):
    pygame.init()
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Simulación de Movimiento Browniano")
    return screen


def run_simulation(screen, game_map, particulas):
    black = (0, 0, 0)
    running = True
    button1 = Button((0, 255, 0), 10, 10, 100, 50, 'Pausa')
    button2 = Button((0, 0, 255), 120, 10, 100, 50, 'Sigue')
    button3 = Button((255, 0, 255), 230, 10, 100, 50, 'Foto')

    
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
                if button1.is_over(pos):
                    for particula in particulas:
                        particula.pause() 
                if button2.is_over(pos):
                    for particula in particulas:
                        particula.continue_running()
                if button3.is_over(pos):
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")  # Formato de sello de tiempo
                    screenshot_filename = f"screenshot_{timestamp}.png"
                    pygame.image.save(screen, screenshot_filename)
                    print(f"Captura de pantalla guardada como {screenshot_filename}")


                    
        screen.fill(black)
        game_map.draw(screen)
        button1.draw(screen)
        button2.draw(screen)
        button3.draw(screen)
        # Dibuja más botones si los agregaste
        pygame.display.flip()

    pygame.quit()
    sys.exit()

def partir_conjunto(numeros, n_partes):
    archivo = numeros
    paso =  round((max(archivo) - min(archivo)) / n_partes , 4)
    limites = [min(archivo)+paso*i for i in range(n_partes)]
    limites.append(max(archivo))
    return limites

def definir_direccion(self, intervalos, valor):
    print(f"Los intervalos son: {intervalos}")
    for i in range(len(intervalos) - 1):
        if valor >= intervalos[i] and valor < intervalos[i + 1]:
            return i+1
    if valor >= intervalos[-1]:
        return len(intervalos) - 1
    else:
        print(valor)
        return None  
    
def definir_tam_paso(self, intervalos, valor):
    intervalo = self.definir_direccion(intervalos, valor)
    return intervalo * 3



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
