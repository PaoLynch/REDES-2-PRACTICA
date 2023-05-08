import socket #Libreria del socket
import wave,pyaudio, pickle,struct #Librerias para usar los audios
from _thread import * #Libreria de hilos
ServerSocket = socket.socket() #Crea el socket
host = '127.0.0.1'
port = 2524
Buffer = 1024
try:
    ServerSocket.bind((host, port)) #Hacemos el bind
except socket.error as e:
    print(str(e))
print('Socket listo')
ServerSocket.listen(5)

#Funcion de trabajo
def ActividadCliente(connection):
    while True:
        p = pyaudio.PyAudio() #Manejo de audio
        stream = p.open(format=p.get_format_from_width(2), channels=2, rate=44100, output=True, frames_per_buffer=Buffer) #Para definir las constantes que se mandan a los puertos de audio
        data = b""
        carga = struct.calcsize("Q") #Guarda los bytes que se mandan de carga y los convierte en binario
        while True:
            try:
                while len(data) < carga:
                    packet = connection.recv(4 * 1024)  # Recibir un audio de calidad
                    if not packet:
                        break
                    data += packet
                paquete_mensaje = data[:carga] #Los elemento de data hasta que lleguen a carga
                data = data[carga:]
                mensaje_tam = struct.unpack("Q", paquete_mensaje)[0] #Desempaquetado de los datos
                while len(data) < mensaje_tam:
                    data += connection.recv(4 * 1024)
                frame_data = data[:mensaje_tam]
                data = data[mensaje_tam:]
                frame = pickle.loads(frame_data) #Lo convierte a una secuencia de bytes ya que estan en binario
                stream.write(frame) #Crea un objeto de escritura de salida
            except:
                break
    connection.close()
while True:
    Client, address = ServerSocket.accept() #Acepta la conexion
    print('Cliente: ' + address[0] ) #Te dice desde donde se conecta
    start_new_thread(ActividadCliente, (Client,)) #Comienza la rutina del hilo
ServerSocket.close()