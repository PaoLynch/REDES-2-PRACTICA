import socket, pickle
import sys
import random
import time
buffer_size = 1024

def Crear_Matriz_Bool(A):
    for i in range(filas):
        C = []
        for j in range (columnas):
            C.append(0)
        A.append(C)
    k = 1
    while k <= minas:
        x = random.randint(0, filas-1)
        y = random.randint(0, columnas-1)
        if A[x][y] == 0:
            A[x][y] = "*"
            k +=1

def Imprimir_Matriz(A):
    k = 0
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

def Verificar(A):
    for i in range(filas):
        for j in range(columnas):
            #Esquina superior izquierda
            if i == 0 and j == 0 and A[i][j] !="*":
                if A[i][j+1] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i+1][j+1] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i+1][j] == "*":
                    A[i][j] = A[i][j] + 1
            #Esquina superior derecha
            elif i == 0 and j == columnas-1 and A[i][j] !="*":
                if A[i][j-1]== "*":
                    A[i][j] = A[i][j] + 1
                if A[i+1][j-1] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i+1][j] == "*":
                    A[i][j] = A[i][j] + 1

            #Esquina inferior izquierda
            elif i == filas-1 and j == 0 and A[i][j] !="*":
                if A[i-1][j] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i-1][j+1] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i][j+1] == "*":
                    A[i][j] = A[i][j] + 1

            #Esquina inferior derecha
            elif i == filas-1 and j == columnas-1 and A[i][j] != "*":
                if A[i-1][j] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i-1][j-1] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i][j-1] == "*":
                    A[i][j] = A[i][j] + 1

            #Lateral superior
            elif i == 0 and j > 0 and j < columnas-1 and A[i][j] != "*":
                if A[i][j+1] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i+1][j+1] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i+1][j] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i][j-1] == "*":
                    A[i][j] = A[i][j] + 1

            #Lateral derecho
            elif i < filas-1 and i >0 and j == columnas-1 and A[i][j] !="*":
                if A[i+1][j] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i-1][j-1] == "*":
                    A[i][j] = A[i][j] +1
                if A[i][j-1] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i+1][j-1] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i+1][j] == "*":
                    A[i][j] = A[i][j] + 1

            #Lateral inferior
            elif i == filas-1 and j >0 and j < columnas-1 and A[i][j] !="*":
                if A[i][j-1] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i-1][j-1] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i-1][j] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i][j+1] == "*":
                    A[i][j] = A[i][j]  + 1

            #Lateral izquierdo
            elif i < filas-1 and i >0 and j == 0 and A[i][j] !="*":
                if A[i-1][j] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i-1][j+1] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i][j+1] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i+1][j+1] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i+1][j] == "*":
                    A[i][j] = A[i][j] + 1

            #Centro
            elif i > 0 and i < filas-1 and j > 0 and j < columnas-1 and A[i][j] !="*":
                if A[i-1][j] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i-1][j+1] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i][j+1] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i+1][j+1] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i+1][j] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i+1][j-1] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i][j-1] == "*":
                    A[i][j] = A[i][j] + 1
                if A[i-1][j-1] == "*":
                    A[i][j] = A[i][j] + 1

            if A[i][j] == 0:
                A[i][j] = " "

def Matriz_juego(B, filas, columnas):
    for i in range(filas):
        C = []
        for j in range(columnas):
            C.append("#")
        B.append(C)

def Matriz_final(A, C, filas, columnas):
    for i in range(filas):
        D = []
        for j in range(columnas):
            D.append(A[i][j])
        C.append(D)

def Jugada(A, B, C, x, y):
    global k,n
    if A[x][y] != "*" and A[x][y] != 0 and A[x][y] != False:
        B[x][y] = A[x][y]
        if A[x][y] == " ":
            n += 1
            A[x][y] = 0
            if x == 0 and y == 0:
                Jugada(A,B,C,x,y+1)
                Jugada(A,B,C,x+1,y+1)
                Jugada(A,B,C,x+1,y)
            elif x == 0 and y == columnas-1:
                Jugada(A,B,C,x,y-1)
                Jugada(A,B,C,x+1,y-1)
                Jugada(A,B,C,x+1,y)
            elif x == filas-1 and y == 0:
                Jugada(A,B,C,x-1,y)
                Jugada(A,B,C,x-1,y-1)
                Jugada(A,B,C,x,y+1)
            elif x == filas-1 and y == columnas-1:
                Jugada(A,B,C,x-1,y)
                Jugada(A,B,C,x-1,y-1)
                Jugada(A,B,C,x,y-1)
            elif x == 0 and y > 0 and y < columnas-1:
                Jugada(A,B,C,x,y-1)
                Jugada(A,B,C,x+1,y+1)
                Jugada(A,B,C,x+1,y)
                Jugada(A,B,C,x+1,y+1)
                Jugada(A,B,C,x,y+1)
            elif x > 0 and x < filas-1 and y == columnas-1:
                Jugada(A, B, C, x-1, y)
                Jugada(A, B, C, x-1, y-1)
                Jugada(A, B, C, x, y+1)
                Jugada(A, B, C, x+1, y-1)
                Jugada(A, B, C, x+1, y)
            elif x == filas-1 and y > 0 and y < columnas-1:
                Jugada(A, B, C, x, y-1)
                Jugada(A, B, C, x, y+1)
                Jugada(A, B, C, x-1, y-1)
                Jugada(A, B, C, x-1, y)
                Jugada(A, B, C, x-1, y+1)
            elif x > 0 and x < filas-1 and y == 0:
                Jugada(A, B, C, x+1, y)
                Jugada(A, B, C, x-1, y)
                Jugada(A, B, C, x-1, y+1)
                Jugada(A, B, C, x, y+1)
                Jugada(A, B, C, x+1, y+1)
            elif x > 0 and x < filas-1 and y < columnas-1 and y > 0:
                Jugada(A, B, C, x-1, y-1)
                Jugada(A, B, C, x-1, y)
                Jugada(A, B, C, x+1, y+1)
                Jugada(A, B, C, x, y-1)
                Jugada(A, B, C, x, y+1)
                Jugada(A, B, C, x+1, y-1)
                Jugada(A, B, C, x+1, y)
                Jugada(A, B, C, x+1, y+1)
        elif A[x][y] > 0:
            n += 1
            A[x][y] =False
    elif A[x][y] == "*":
        k = False
        P = "Perdiste"
        connection.send(P.encode())
        Imprimir_Matriz(C)

# Crear socket
socketAbierto = socket.socket()

# IP del equipo
equipo = input("Introduzca la dirección IP o nombre del equipo: ")
# Puerto
puerto = int(input("Introduzca el puerto de escucha: "))

try:
    #Conecta al socket
    socketAbierto.bind((equipo, puerto))
except socket.error as message:
    print("Falló la escucha por el puerto ", puerto)
    print(message)
    sys.exit()
#Comenzamos a escuchar
socketAbierto.listen()
print("Escuchando en el puerto: ", puerto)
while True:
    #Espera la conexion
    connection,address = socketAbierto.accept()
    print("Cliente ", address[0],address[1], "conectado")

    #Flujo de mensajes
    mensaje = "Bienvenido al juego de Buscaminas"
    connection.send(mensaje.encode())
    Level = "Le ofrecemos dos niveles 1 - Principiante (9x9) y 2 - Avanzado (16x16)"
    connection.send(Level.encode())

    option = connection.recv(buffer_size)
    print("La opcion elegida es:", option.decode())

    if option.decode() == "1":
        filas = 9
        columnas = 9
        minas = 10
        k = True
        n = 0
        A = []
        B = []
        C = []
        Crear_Matriz_Bool(A)
        Verificar(A)
        Matriz_final(A,C,filas, columnas)
        Matriz_juego(B,filas,columnas)
        Imprimir_Matriz(B)
        arr_pickle = pickle.dumps(B)
        connection.sendall(arr_pickle)
        x = connection.recv(buffer_size)
        y = connection.recv(buffer_size)
        print("Las cordenadas son", x.decode() ,y.decode())
        coorx = int(x.decode())
        coory = int(y.decode())
        if coorx >= filas or coory >= columnas:
            mess = "La jugada es invalida"
        else:
            if A[coorx][coory] == 0:
                mess = "La jugada fue realizada"
            else:
                Jugada(A,B,C,coorx,coory)
        G = "Ganaste"
        connection.send(G.encode())
        Imprimir_Matriz(C)
        arr_pickleF = pickle.dumps(C)
        connection.sendall(arr_pickleF)
        break
    elif option.decode() == "2":
        filas = 16
        columnas = 16
        minas = 40
        k = True
        n = 0
        A = []
        B = []
        C = []
        Crear_Matriz_Bool(A)
        Verificar(A)
        Matriz_final(A,C,filas, columnas)
        Matriz_juego(B,filas,columnas)
        Imprimir_Matriz(B)
        arr_pickle = pickle.dumps(B)
        connection.sendall(arr_pickle)
        x = connection.recv(buffer_size)
        y = connection.recv(buffer_size)
        print("Las cordenadas son", x.decode() ,y.decode())
        coorx = int(x.decode())
        coory = int(y.decode())
        if coorx >= filas or coory >= columnas:
            mess = "La jugada es invalida"
        else:
            if A[coorx][coory] == 0:
                mess = "La jugada fue realizada"
            else:
                Jugada(A,B,C,coorx,coory)
        G = "Ganaste"
        connection.send(G.encode())
        Imprimir_Matriz(C)
        arr_pickleF = pickle.dumps(C)
        connection.sendall(arr_pickleF)
        break
#Cerramos el socket
connection.close()