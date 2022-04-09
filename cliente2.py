"Basado en la implementacion de Pratik Lotia: Client-Server-Fast-File-Transfer-using-UDP-on-Python. Sep 17, 2016"

import socket
import time
import os
import sys
import os
import logging



#PARAMETROS PARA LOG
from datetime import datetime

logger = logging.getLogger()
handler = logging.FileHandler('log.log')
logger.addHandler(handler)
logger.error('Our First Log Message')


#ARCHIVOS A SOLICITAR
archivo1="Foo1.txt"
archivo2="10.txt"

tTimeout=150

ntr=1



#$ntr = input("Ingrese el numero de threads\n")



numthreads=ntr

name = datetime.now()
addname= name.strftime("%d%m%Y%H%M%S")
fileout =("C:/Users/jdscc/PycharmProjects/ServidorUDP/log/log"+ addname+".log")
f = open(fileout, "w")
now = datetime.now()
f.write("Fecha de inicio: " + str(now)+"\n")
f.write("Numero de threads: " + str(numthreads)+"\n")
print(" numero de threads establecido: " + str(numthreads))

def checkArg():
    if len(sys.argv) != 3:
        print(
            "Num argumentos incorrectos")
        sys.exit()
    else:
        print("Argumentos Validos")

psize=4096
def checkPort():
    if int(sys.argv[2]) <= 5000:
        print(
            "Numero de puerto invalido (<5000).")
        sys.exit()
    else:
        print("num puerto ok,")

checkArg()
try:
    socket.gethostbyname(sys.argv[1])
except socket.error:
    print("Nombre de host invalido.")
    sys.exit()

host = sys.argv[1]
try:
    port = int(sys.argv[2])
except ValueError:
    print("Error. Numeros de puerto no validos.")
    sys.exit()
except IndexError:
    print("Error. Numeros de puerto no validos.")
    sys.exit()

checkPort()

#host = "127.0.0.1"
#port = 6000
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print("Cliente inicializado")
    s.setblocking(0)
    s.settimeout(tTimeout)
except socket.error:
    print("Failed to create socket")
    sys.exit()
    time.sleep(1)

while True:
    command = input(
    "Inngrese un comando: \n1. get100\n2. get250\n3. exit\n ")

    """o get [file_name]
    o exit"""
    if command =="get100":
        command= ("get "+ archivo1)
    if command =="get250":
        command= ("get "+ archivo2)
    #print("command:   "+command)
    CommClient = command.encode('utf-8')
    try:
        s.sendto(CommClient, (host, port))
    except ConnectionResetError:
        print(
            "Error. Port numbers are not matching. Exiting. Next time please enter same port numbers.")
        sys.exit()
    #text1 = CommClient.decode('utf-8')
    #t3 = text1.split()
    CL = command.split()
    print(
        " iniciando transferencia")
    # starting operations
    if CL[0] == "get":
        print("Esperando servidor")
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "Error. Numeros de puerto no coiciden")
            sys.exit()
        except:
            print("Timeout")
            sys.exit()
        text = ClientData.decode('utf8')
        print(text)
        print("Realizando solicitud Get al serv.")

        try:
            ClientData2, clientAddr2 = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "Error. Numeros de puerto no coiciden")
            sys.exit()
        except:
            print("Timeout")
            sys.exit()

        text2 = ClientData2.decode('utf8')
        print(text2)

        if len(text2) < 30:
            if CL[0] == "get":
                BigC = open("Received-" + CL[1], "wb")
                d = 0
                try:
                    # num paquetes
                    CountC, countaddress = s.recvfrom(psize)
                except ConnectionResetError:
                    print(
                        "Error. Numeros de puerto no coiciden")
                    sys.exit()
                except:
                    print("Timeout ")
                    sys.exit()

                tillC = CountC.decode('utf8')
                tillCC = int(tillC)
                print("Inicido recibo de paquetes desde el servidor.")
                print("tamano de paquete:  ")
                # print(
                #   "Timeout is 15 seconds so please wait for timeout at the end.")
                while tillCC != 0:
                    ClientBData, clientbAddr = s.recvfrom(psize)
                    dataS = BigC.write(ClientBData)
                    d += 1
                    print("Recibido paquete numero:" + str(d))
                    tillCC = tillCC - 1

                BigC.close()
                paquetesTot=d
                print(
                    "Archivo recibido, revise contenido en carpeta local.")

                f.write("tamano total archivo:  " + str(d*psize)+"\n")
                f.write("paquetes totales recibidos: "+ str(paquetesTot)+"\n")
                now2 = datetime.now()
                f.write("Fecha de terminacion: " + str(now2) + "\n")
                f.close()



    elif CL[0] == "list":
        print("Checking for acknowledgement")
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "Error. num puertos.")
            sys.exit()
        except:
            print("Timeout or some other error")
            sys.exit()

        text = ClientData.decode('utf8')
        print(text)

        if text == "Valid List command. Let's go ahead ":
            ClientDataL, clientAddrL = s.recvfrom(psize)
            text2 = ClientDataL.decode('utf8')
            print(text2)
        else:
            print("Error. Invalid.")

    elif CL[0] == "exit":
        print(
            "")
        quit()

    else:
        try:
            ClientData, clientAddr = s.recvfrom(51200)
        except ConnectionResetError:
            print(
                "Error. Numeros de puerto no coiciden")
            sys.exit()
        except:
            print("Timeout ")
            sys.exit()
        text = ClientData.decode('utf8')
        print(text)

print("")
quit()
