"Basado en la implementacion de Pratik Lotia: Client-Server-Fast-File-Transfer-using-UDP-on-Python. Sep 17, 2016"

import socket
import time
import os
import sys



psize=4096


def checkArg():
    if len(sys.argv) != 2:
        print(
            "ERROR. Wnum argumentos")
        sys.exit()
    else:
        print("num argumentos ok, iniciando")


def checkPort():
    if int(sys.argv[1]) <= 5000:
        print(
            "num puerto invalido.")
        sys.exit()
    else:
        print("num puertos ok!")




def ServerExit():

    print(
        "System will gracefully exit! Not sending any message to Client. Closing my socket!")
    s.close()  # closing socket
    sys.exit()


def ServerGet(g):
    msg = "comando get valido. procesando "
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)



    if os.path.isfile(g):
        msg = "archivo existe "
        msgEn = msg.encode('utf-8')
        s.sendto(msgEn, clientAddr)
        print("notificacion enviada al cliente.")

        c = 0
        sizeS = os.stat(g)
        sizeSS = sizeS.st_size  # number of packets
        print("File size in bytes:" + str(sizeSS))
        NumS = int(sizeSS / 65536)
        print("paquetes esperados:  " + str(NumS))
        NumS = NumS + 1
        tillSS = str(NumS)
        tillSSS = tillSS.encode('utf8')
        s.sendto(tillSSS, clientAddr)

        check = int(NumS)
        GetRunS = open(g, "rb")
        while check != 0:
            RunS = GetRunS.read(4096)
            s.sendto(RunS, clientAddr)
            c += 1
            check -= 1
            print("Packet number:" + str(c))
            print("Envio de archivo en proceso:")
        GetRunS.close()
        print("Archivo enviado desde servidor")

    else:
        msg = "Error: archivo no existe."
        msgEn = msg.encode('utf-8')
        s.sendto(msgEn, clientAddr)



def ServerElse():
    msg = "Error: : " + \
        t2[0] + " no se encuentra comando en el servidorr."
    msgEn = msg.encode('utf-8')
    s.sendto(msgEn, clientAddr)


host = ""
checkArg()
try:
    port = int(sys.argv[1])
except ValueError:
    print("Error.num puerto invalido.")
    sys.exit()
except IndexError:
    print("Error. num puerto invalido.")
    sys.exit()
checkPort()

#port = 6000
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Servidor iniciado")
    s.bind((host, port))
    print("Esperando cliente(s)")
    # s.setblocking(0)
    # s.settimeout(15)
except socket.error:
    print("error crear socket")
    sys.exit()

# time.sleep(1)
while True:
    try:
        data, clientAddr = s.recvfrom(65536)
    except ConnectionResetError:
        print(
            "Error.num puertos.")
        sys.exit()
    text = data.decode('utf8')
    t2 = text.split()
    #print("data print: " + t2[0] + t2[1] + t2[2])
    if t2[0] == "get":
        print("ejecutando funcion envio archivos")
        ServerGet(t2[1])
    elif t2[0] == "exit":
        print("saliendo")
        ServerExit()
    else:
        ServerElse()

print(" ")
quit()
