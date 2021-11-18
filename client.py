import socket
import sys

TCPserverAddressPort   = ('127.0.0.1', 19876)
UDPserverAddressPort   = ('127.0.0.2', 19875)
bufferSize          = 1024

# Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
# Create a TCP/IP socket
TCPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connectionType = input('Connection type: (UDP/TCP)')
user = input('Set name:')

if (connectionType == 'UDP'):
    UDPClientSocket.sendto(
        str.encode(user),
        UDPserverAddressPort
    )
else:
    TCPClientSocket.connect(TCPserverAddressPort)
    TCPClientSocket.sendall(str.encode(user))

while (True):


    if (connectionType == 'UDP'):
        bytesAddressPair = UDPClientSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        messageString = message.decode('UTF-8')
        print(messageString)

        if messageString == 'OK':
            serverMessage = input('Escribir mensaje al servidor:')
            UDPClientSocket.sendto(
                str.encode(serverMessage),
                UDPserverAddressPort
            )
            sys.exit()
        else:
            sys.exit()

    else:
        data = TCPClientSocket.recv(16)
        messageString = data.decode('UTF-8')
        print(messageString)
        if messageString == 'OK':
            serverMessage = input('Escribir mensaje al servidor:')
            TCPClientSocket.sendall(str.encode(serverMessage))
            sys.exit()
        else:
            sys.exit()
