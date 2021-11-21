import socket
import sys
import filemanager
from datetime import datetime

file_name = "names.txt"

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 19876)
print('TCP server up and listening')
sock.bind(server_address)

# Listen for incoming connections
sock.listen(1)

while True:
    # Wait for a connection
    print('waiting for a connection')
    connection, client_address = sock.accept()

    print('connection from', client_address)

    # Receive the data in small chunks and retransmit it
    while True:
        data = connection.recv(16)
        message = data.decode('UTF-8')
        print(message)
        if message.startswith('helloiam'):
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            result = filemanager.search_string_in_file(file_name, message.split()[-1])
            print(result)
            if len(result) != 0:
                # Sending response to client
                connection.sendall(str.encode('OK'))

            elif len(result) == 0:
                # Sending response to client
                connection.sendall(str.encode('Usuario inexistente'))
                with open('log.txt', 'a') as f:
                    f.write('Usuario inexistente' + ' ' + dt_string + ' ' + client_address[0] + ' 19876' + ' TCP')
                    f.write('\n')
                    sys.exit()
        else:
            with open('log.txt', 'a') as f:
                f.write(message + ' ' + dt_string + ' ' + client_address[0] + ' 19876' + ' TCP')
                f.write('\n')
                sys.exit()
