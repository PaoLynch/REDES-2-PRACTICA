import socket, pickle #Libreria del socket y la funcion para imprimir el tablero
import sys
buffer_size = 1024 #Tamaño del buffer para recibir datos

def enviar_datos():
    #Envia constantemente los datos sin embargo no sale
    #Si imprime mas no se puede salir
    while True:
        try:
            mov = input("¿w/s/a/d - m - b/v?: ")
            socketConexion.send(mov.encode())
            print("Se envio dato")
            line3 = socketConexion.recv(buffer_size)
            if not line3:
                break
            tab = pickle.loads(line3)
            print("Se recibio")
            for i, a in enumerate(tab):
                print(a, end="   ")
                if i % 9 == 8:
                    print("\n")
        except:
            socketConexion.close()

# Crear socket
socketConexion = socket.socket()

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

present = socketConexion.recv(buffer_size)
print(present.decode())

if opcion == "1":
    #Imprime primer tablero
    line3 = socketConexion.recv(buffer_size)
    tab = pickle.loads(line3)
    for i, a in enumerate(tab):
        print (a, end = "   ")
        if i % 9 == 8:
            print("\n")
elif opcion == "2":
    #No imprime tablero
    #ERROR: Ran run of input (probablemente sea por el tipo de dato)
    line2 = socketConexion.recv(buffer_size)
    tab = pickle.loads(line2)
    for i, a in enumerate(tab):
        print (a, end = "   ")
        if i % 16 == 15:
            print("\n")

enviar_datos()
# Cerrar el socket
socketConexion.close()