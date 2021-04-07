# Created by Helga on 07.04.2021
import socket
import logging

logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('127.0.0.1', 40000)

try:
    socket.connect(server_address)
    message = input("Input message: ")
    while message != "exit":
        socket.sendall(message.encode("utf-8"))
        data = socket.recv(1024)
        logging.info(f'Receive {data.decode()}')
        message = input("Input message: ")

except ConnectionResetError:
    logging.info(f'Host break connection. Impossible to sent data')
except Exception as e:
    logging.info(f' Exception: {str(e)}')
finally:
    socket.close()
