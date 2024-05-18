def contar_numeros(archivo):
    with open(archivo, 'r') as file:
        contenido = file.read()
        numeros = contenido.split(',')
        cantidad_numeros = len(numeros)
    return cantidad_numeros

# Ejemplo de uso
archivo = 'direcciones_feigenbaum0.txt'
print(f'El archivo tiene {contar_numeros(archivo)} números.')
