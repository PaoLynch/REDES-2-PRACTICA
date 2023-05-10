import socket, pickle #Libreria del socket y la funcion para imprimir el tablero
import sys
import numpy as np
buffer_size = 1024 #Tamaño del buffer para recibir datos

# Crear socket
socketConexion = socket.socket()

def Imprimir_Matriz1(A):
    k = 0
    columnas = 9
    print("|", end="")
    for i in range (columnas):
        print(i, end="")
    print()
    print(end="")
    for i in range (columnas):
        print("--", end="")
    print()
    for i in A:
        print(k, end="|")
        for j in i:
            print(j,end="")
        k +=1
        print()

def Imprimir_Matriz2(A):
    k = 0
    columnas = 16
    print("|", end="")
    for i in range (columnas):
        print(i, end="")
    print()
    print(end="")
    for i in range (columnas):
        print("--", end="")
    print()
    for i in A:
        print(k, end="|")
        for j in i:
            print(j,end="")
        k +=1
        print()

# IP a utilizar
servidor = input("Introduzca la dirección IP a usar: ")
# El puerto que se va a utilizar
puerto = int(input("Introduzca el puerto a usar: "))

try:
    # Conectar el socket
    socketConexion.connect((servidor, puerto))
except socket.error as message:
    print("Falló la conexión con el servidor {} por el puerto {}".format(servidor, puerto))
    print(message)
    sys.exit()

#Flujo de mensajes
mensajeBienvenida = socketConexion.recv(buffer_size)
print(mensajeBienvenida.decode())

mensajeMenu = socketConexion.recv(buffer_size)
print(mensajeMenu.decode())


opcion = input("Introduzca la opcion que quiere jugar: ")
socketConexion.send(opcion.encode())

data = socketConexion.recv(buffer_size)
arr = pickle.loads(data)
if (opcion == "1"):
    Imprimir_Matriz1(arr)
elif (opcion == "2"):
    Imprimir_Matriz2(arr)

x = input("La cordenada en x: ")
socketConexion.send(x.encode())
y = input("La cordenada en y: ")
socketConexion.send(y.encode())


mess = socketConexion.recv(buffer_size)
print(mess.decode())

data1 = socketConexion.recv(buffer_size)
arr1 = pickle.loads(data1)
if (opcion == "1"):
    Imprimir_Matriz1(arr1)
elif (opcion == "2"):
    Imprimir_Matriz2(arr1)

# Cerrar el socket
socketConexion.close()