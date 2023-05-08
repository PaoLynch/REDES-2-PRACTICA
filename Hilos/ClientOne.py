#Librerias a usar
import socket
import wave,pyaudio,pickle,struct

#Creacion del socket cliente
ClienteSocket = socket.socket()
host = '127.0.0.1'
port = 2524
Buffer = 1024
try:
    ClienteSocket.connect((host, port)) #Conecta con el servidor
except socket.error as e:
    print(str(e))
while True:
    wf = wave.open("AitanaAngeles.wav", 'rb')

    p = pyaudio.PyAudio()

    #Width = ancho de la muestra bytes, channels = estero o mono, rate = velocidad
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(), rate=wf.getframerate(), input=True, frames_per_buffer=Buffer)
    data = None
    while True:
        if ClienteSocket:
            print("Comienza el Audio")
            while True:
                data = wf.readframes(Buffer) #Lee y devuelve como máximo n/buffer fotogramas de audio, como un objeto de bytes
                a = pickle.dumps(data) #Escribe en data
                message = struct.pack("Q", len(a)) + a #Convierte en bytes lo que no sean bytes
                ClienteSocket.sendall(message)
                if not data:
                    stream.close()
                    ClienteSocket.close()
                    break
            break
ClienteSocket.close()