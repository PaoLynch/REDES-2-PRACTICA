import socket, pickle
import sys
import random
import time
buffer_size = 1024

def NewTablero(fil, col, val):  #Crea una matriz con las filas y columnas y valor que le pasemos
    tablero = []
    for i in range(fil):
        tablero.append([])
        for j in range(col):
            tablero[i].append(val)
    return tablero

def coloca_minas1(tablero, minas, fil, col):  #Coloca en el tablero que le pasemos el número de minas que le pasemos
    minas_ocultas = []
    numero = 0
    while numero < minas:
        y = random.randint(0,fil-1)
        x = random.randint(0,col-1)
        if tablero[y][x] != 9:
            tablero[y][x] = 9
            numero += 1
            minas_ocultas.append((y,x))
    return tablero, minas_ocultas

def coloca_minas2(tablero, minas, fil, col):  #Coloca en el tablero que le pasemos el número de minas que le pasemos
    minas_ocultas = []
    numero = 0
    while numero < minas:
        y = random.randint(0,fil-1)
        x = random.randint(0,col-1)
        if tablero[y][x] != 16:
            tablero[y][x] = 16
            numero += 1
            minas_ocultas.append((y,x))
    return tablero, minas_ocultas

def coloca_pistas1(tablero, fil, col):  #Recorre el tablero y pone el número de minas vecinas que tiene cada casilla
    for y in range(fil):
        for x in range(col):
            if tablero[y][x] == 9:
                for i in [-1,0,1]:
                    for j in [-1,0,1]:
                        if 0 <= y+i <= fil-1 and 0 <= x+j <= col-1:
                            if tablero[y+i][x+j] != 9:
                                tablero[y+i][x+j] += 1
    return tablero

def coloca_pistas2(tablero, fil, col):  #Recorre el tablero y pone el número de minas vecinas que tiene cada casilla
    for y in range(fil):
        for x in range(col):
            if tablero[y][x] == 16:
                for i in [-1,0,1]:
                    for j in [-1,0,1]:
                        if 0 <= y+i <= fil-1 and 0 <= x+j <= col-1:
                            if tablero[y+i][x+j] != 16:
                                tablero[y+i][x+j] += 1

def muestra_tablero1(tablero): #Muestra en filas y columnas la matriz que le pasemos
    line3= []
    for fila in tablero:
        for elem in fila:
            line3.append(elem)
    lines = pickle.dumps(line3)
    connection.send(lines)

def muestra_tablero2(tablero): #Muestra en filas y columnas la matriz que le pasemos
    line2= []
    for fila in tablero:
        for elem in fila:
            line2.append(elem)
    lines = pickle.dumps(line2)
    connection.send(lines)

def reemplaza_ceros1(tablero):
    for i in range(9):
        for j in range(9):
            if tablero[i][j] == 0:
                tablero[i][j] = " "
    return tablero

def reemplaza_ceros2(tablero):
    for i in range(16):
        for j in range(16):
            if tablero[i][j] == 0:
                tablero[i][j] = " "
    return tablero

def tablero_completo(tablero, fil, col, val): #Comprueba si el tablero no tiene ninguna casilla con el valor visible inicial
    for y in range(fil):
        for x in range(col):
            if tablero[y][x] == val:
                return False
    return True

def rellenado(oculto, visible, y, x, fil, col, val):
    #Recorre todas las casillas vecinas, y comprueba si son ceros, si es así las descubre,
    # y recorre las vecinas de estas, hasta encontrar casillas con pistas, que también descubre.

    ceros =  [(y,x)]
    while len(ceros) > 0:
        y, x = ceros.pop()
        for i in [-1,0,1]:
            for j in [-1,0,1]:
                if 0 <= y+i <= fil-1 and 0 <= x+j <= col-1:
                    if visible[y+i][x+j] == val and oculto[y+i][x+j] == 0:
                        visible[y+i][x+j] = 0
                        if (y+i, x+j) not in ceros:
                            ceros.append((y+i, x+j))
                    else:
                        visible[y+i][x+j] = oculto[y+i][x+j]

    return visible

def coordenada1(visible, x, y, filas, columnas, real, oculto, minas_ocultas): #Da la posicion de la mina y hace lo necesario
    minas_marcadas = []
    jugando = True
    while jugando:
        try:
            mov = connection.recv(buffer_size)
            print("La cordenada fue: ", mov.decode())
            if mov.decode() == "w":
                if y == 0:
                    y = 0
                else:
                    visible[y][x] = real
                    y -= 1
                    real = visible[y][x]
                    visible[y][x] = "x"

            elif mov.decode() == "s":
                if y == filas - 1:
                    y = filas - 1
                else:
                    visible[y][x] = real
                    y += 1
                    real = visible[y][x]
                    visible[y][x] = "x"

            elif mov.decode() == "a":
                if x == 0:
                    x = 0
                else:
                    visible[y][x] = real
                    x -= 1
                    real = visible[y][x]
                    visible[y][x] = "x"

            elif mov.decode() == "d":
                if x == columnas - 1:
                    x = columnas - 1
                else:
                    visible[y][x] = real
                    x += 1
                    real = visible[y][x]
                    visible[y][x] = "x"

            elif mov.decode() == "b":
                if real == "-":
                    visible[y][x] = "#"
                    real = visible[y][x]
                    if (y, x) not in minas_marcadas:
                        minas_marcadas.append((y, x))

            elif mov.decode() == "v":
                if real == "#":
                    visible[y][x] = "-"
                    real = visible[y][x]
                    if (y, x) in minas_marcadas:
                        minas_marcadas.remove((y, x))

            elif mov.decode() == "m":
                if oculto[y][x] == 9:
                    visible[y][x] = "@"
                    print("PERDISTE")
                    break

                elif oculto[y][x] != 0:
                    visible[y][x] = oculto[y][x]
                    real = visible[y][x]

                elif oculto[y][x] == 0:
                    visible[y][x] = 0
                    visible = rellenado(oculto, visible, y, x, filas, columnas, "-")
                    visible = reemplaza_ceros1(visible)
                    real = visible[y][x]

            muestra_tablero1(visible)

            if tablero_completo(visible, filas, columnas, "-") and \
                    sorted(minas_ocultas) == sorted(minas_marcadas) and \
                    real != "-":
                print("Ganaste")
                break
        except:
            print("No jala")
            connection.close()
    return

def coordenada2(visible, x, y, filas, columnas, real, oculto, minas_ocultas): #Da la posicion de la mina y hace lo necesario
    minas_marcadas = []
    jugando = True
    while jugando:
        try:
            mov = connection.recv(buffer_size)
            print("La cordenada fue: ", mov.decode())
            if mov.decode() == "w":
                if y == 0:
                    y = 0
                else:
                    visible[y][x] = real
                    y -= 1
                    real = visible[y][x]
                    visible[y][x] = "x"

            elif mov.decode() == "s":
                if y == filas - 1:
                    y = filas - 1
                else:
                    visible[y][x] = real
                    y += 1
                    real = visible[y][x]
                    visible[y][x] = "x"

            elif mov.decode() == "a":
                if x == 0:
                    x = 0
                else:
                    visible[y][x] = real
                    x -= 1
                    real = visible[y][x]
                    visible[y][x] = "x"

            elif mov.decode() == "d":
                if x == columnas - 1:
                    x = columnas - 1
                else:
                    visible[y][x] = real
                    x += 1
                    real = visible[y][x]
                    visible[y][x] = "x"

            elif mov.decode() == "b":
                if real == "-":
                    visible[y][x] = "#"
                    real = visible[y][x]
                    if (y, x) not in minas_marcadas:
                        minas_marcadas.append((y, x))

            elif mov.decode() == "v":
                if real == "#":
                    visible[y][x] = "-"
                    real = visible[y][x]
                    if (y, x) in minas_marcadas:
                        minas_marcadas.remove((y, x))

            elif mov.decode() == "m":
                if oculto[y][x] == 16:
                    visible[y][x] = "@"
                    print("PERDISTE")
                    break

                elif oculto[y][x] != 0:
                    visible[y][x] = oculto[y][x]
                    real = visible[y][x]

                elif oculto[y][x] == 0:
                    visible[y][x] = 0
                    visible = rellenado(oculto, visible, y, x, filas, columnas, "-")
                    visible = reemplaza_ceros2(visible)
                    real = visible[y][x]

            muestra_tablero2(visible)

            if tablero_completo(visible, filas, columnas, "-") and \
                    sorted(minas_ocultas) == sorted(minas_marcadas) and \
                    real != "-":
                print("Ganaste")
                break
        except:
            print("No jala")
            connection.close()
    return

def Principiante():
    columnas = 9
    filas = 9
    visible = NewTablero(filas, columnas, "-")
    oculto = NewTablero(filas, columnas, 0)
    oculto, minas_ocultas = coloca_minas1(oculto, 10, filas, columnas)
    oculto = coloca_pistas1(oculto, filas, columnas)
    presentation = "Usa w/a/s/d - moverse, m - mostrar y b/v - marcar/desmarcar"
    connection.send(presentation.encode())

    y = random.randint(2, filas - 3)
    x = random.randint(2, columnas - 3)
    real = visible[y][x]
    visible[y][x] = "x"
    start = time.time()
    muestra_tablero1(visible)
    coordenada1(visible, x, y, filas, columnas, real, oculto, minas_ocultas)
    end = time.time()
    timeout = end - start
    print("Hola de nuevo")
    print("Hiciste un tiempo de:", timeout)
    #Cerramos el socket
    connection.close()


def Avanzado():
    columnas = 16
    filas = 16
    visible = NewTablero(filas, columnas, "-")
    oculto = NewTablero(filas, columnas, 0)
    oculto, minas_ocultas = coloca_minas2(oculto, 40, filas, columnas)
    oculto = coloca_pistas2(oculto, filas, columnas)
    presentation = "Usa w/a/s/d - moverse, m - mostrar y b/v - marcar/desmarcar"
    connection.send(presentation.encode())

    y = random.randint(2, filas - 3)
    x = random.randint(2, columnas - 3)
    real = visible[y][x]
    visible[y][x] = "x"
    muestra_tablero2(visible)
    coordenada2(visible, x, y, filas, columnas, real, oculto, minas_ocultas)
    print("Hola de nuevo")
    #Cerramos el socket
    connection.close()


# Crear socket
socketAbierto = socket.socket()

# IP del equipo
equipo = input("Introduzca la dirección IP o nombre del equipo (en blanco para localhost): ")
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
    print("Cliente ", address[0],address[1], " conectado")

    #Flujo de mensajes
    mensaje = "Bienvenido al juego de Buscaminas"
    connection.send(mensaje.encode())
    Level = "Le ofrecemos dos niveles 1 - Principiante (9x9) y 2 - Avanzado (16x16)"
    connection.send(Level.encode())

    option = connection.recv(buffer_size)
    print("La opcion elegida es:", option.decode())

    if option.decode() == "1":
        Principiante()
    elif option.decode() == "2":
        connection.close()
    else:
        mess3 = "Adios"
        connection.send(mess3.encode())
        socketAbierto.close()
    #Cerramos el socket
    connection.close()