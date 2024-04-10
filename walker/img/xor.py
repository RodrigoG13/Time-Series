import numpy as np
import matplotlib.pyplot as plt

class SimpleNeuralNetwork:
    def __init__(self, input_size, hidden_size, output_size):
        self.weights_hidden = np.random.uniform(-1, 1, (input_size, hidden_size))
        self.bias_hidden = np.random.uniform(-1, 1, hidden_size)
        self.weights_output = np.random.uniform(-1, 1, hidden_size)
        self.bias_output = np.random.uniform(-1, 1)
        self.activation = lambda x: np.tanh(x)
        self.activation_derivative = lambda x: 1 - np.tanh(x) ** 2

    def forward(self, X):
        self.hidden = self.activation(np.dot(X, self.weights_hidden) + self.bias_hidden)
        output = self.activation(np.dot(self.hidden, self.weights_output) + self.bias_output)
        return output

    def train(self, X, y, learning_rate=0.1, epochs=10000):
        for epoch in range(epochs):
            for x, target in zip(X, y):
                output = self.forward(x)
                error = target - output
                d_output = error * self.activation_derivative(output)
                error_hidden = d_output * self.weights_output
                d_hidden = error_hidden * self.activation_derivative(self.hidden)
                self.weights_output += learning_rate * self.hidden * d_output
                self.bias_output += learning_rate * d_output
                self.weights_hidden += learning_rate * x[:, np.newaxis] * d_hidden
                self.bias_hidden += learning_rate * d_hidden

def predict(nn, X):
    predictions = np.array([nn.forward(x) for x in X])
    return np.round(predictions).flatten()



# Datos para la compuerta XOR
X_xor = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_xor = np.array([0, 1, 1, 0])

# Crear y entrenar la red
nn = SimpleNeuralNetwork(input_size=2, hidden_size=7, output_size=1)
nn.train(X_xor, y_xor, learning_rate=0.1, epochs=100000)

# Generar una malla de puntos para visualizar el límite de decisión
x1_range = np.linspace(-0.5, 1.5, 1000)
x2_range = np.linspace(-0.5, 1.5, 1000)
xx1, xx2 = np.meshgrid(x1_range, x2_range)
grid = np.c_[xx1.ravel(), xx2.ravel()]

# Predicciones para cada punto en la malla
predictions_grid = predict(nn, grid).reshape(xx1.shape)

# Graficar el límite de decisión y los puntos de entrenamiento
plt.figure(figsize=(8, 8))
plt.contourf(xx1, xx2, predictions_grid, alpha=0.7, levels=[-1, 0, 1])
plt.scatter(X_xor[:, 0], X_xor[:, 1], c=y_xor, s=100, edgecolor='k', marker='o')
plt.title('Límite de Decisión de la Red Neuronal para XOR')
plt.xlabel('Input 1')
plt.ylabel('Input 2')
plt.grid(True)
plt.savefig('xor4.pdf') 
plt.show()


# Generar una malla de puntos para visualizar el límite de decisión
x1_range = np.linspace(-10, 10, 1000)
x2_range = np.linspace(-10, 10, 1000)
xx1, xx2 = np.meshgrid(x1_range, x2_range)
grid = np.c_[xx1.ravel(), xx2.ravel()]

# Predicciones para cada punto en la malla
predictions_grid = predict(nn, grid).reshape(xx1.shape)
