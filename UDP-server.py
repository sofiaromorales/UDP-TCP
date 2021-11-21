import socket
import sys
import filemanager
from datetime import datetime

localIP     = "127.0.0.1"
localPort   = 19875
bufferSize  = 1024
msgFromServer  = "Hello UDP Client"
bytesToSend = str.encode(msgFromServer)
file_name = "names.txt"

#####CONNECTION

# Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

# Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

print('UDP server up and listening')

# Listen for incoming datagrams

while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(4096)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]
    print(address)

    clientMsg = message.decode('utf-8')
    print(clientMsg)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    if clientMsg.startswith('helloiam'):
        # Looking name in file
        result = filemanager.search_string_in_file(file_name, clientMsg.split()[-1])
        print(result)
        if len(result) != 0:
            # Sending response to client
            UDPServerSocket.sendto(
                str.encode('OK'),
                address
            )
        elif len(result) == 0:
            # Sending response to client
            UDPServerSocket.sendto(
                str.encode('Usuario inexistente'),
                address
            )
            with open('log.txt', 'a') as f:
                f.write('Usuario inexistente' + ' ' + dt_string + ' ' + address[0] + ' ' + str(localPort) + ' UDP')
                f.write('\n')
            sys.exit()

    else:
        with open('log.txt', 'a') as f:
            f.write(clientMsg + ' ' + dt_string + ' ' + address[0] + ' ' + str(localPort) + ' UDP')
            f.write('\n')
