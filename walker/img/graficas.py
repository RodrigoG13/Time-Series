import numpy as np
import matplotlib.pyplot as plt
# Importamos 'ggplot' para el estilo de las gráficas
plt.style.use('ggplot')

# Definir las funciones de activación
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def tanh(x):
    return np.tanh(x)

def relu(x):
    return np.maximum(0, x)

# Definir el rango de valores para x
x = np.linspace(-5, 5, 100)

# Calcular los valores de las funciones de activación
y_sigmoid = sigmoid(x)
y_tanh = tanh(x)
y_relu = relu(x)

# Gráfica para la función de activación Sigmoidal
plt.figure(figsize=(8, 6))
plt.plot(x, y_sigmoid, label='Sigmoidal', color='navy', linewidth=2, linestyle='--')
plt.xlabel('Valor h', fontsize=14, fontweight='bold')
plt.ylabel('Sigmoide(h)', fontsize=14, fontweight='bold')
plt.title('Función Sigmoidal', fontsize=16, fontweight='bold')
plt.legend()
plt.grid(True)
plt.savefig('sigmoidal.pdf', format='pdf')
plt.close()

# Gráfica para la función de activación Tangente Hiperbólica
plt.figure(figsize=(8, 6))
plt.plot(x, y_tanh, label='Tangente Hiperbólica', color='crimson', linewidth=2, linestyle='-.')
plt.xlabel('Valor h', fontsize=14, fontweight='bold')
plt.ylabel('tanh(x)', fontsize=14, fontweight='bold')
plt.title('Función Tangente Hiperbólica', fontsize=16, fontweight='bold')
plt.legend()
plt.grid(True)
plt.savefig('tanh.pdf', format='pdf')
plt.close()

# Gráfica para la función de activación ReLU
plt.figure(figsize=(8, 6))
plt.plot(x, y_relu, label='ReLU', color='forestgreen', linewidth=2, dash_capstyle='round')
plt.xlabel('Valor h', fontsize=14, fontweight='bold')
plt.ylabel('ReLu(h)', fontsize=14, fontweight='bold')
plt.title('Función ReLu', fontsize=16, fontweight='bold')
plt.legend()
plt.grid(True)
plt.savefig('relu.pdf', format='pdf')
plt.close()
