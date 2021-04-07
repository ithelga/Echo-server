import logging
import multiprocessing
import socket
import select

logging.basicConfig(format='%(levelname)s - %(asctime)s: %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)


def server(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    logging.info(f'Binding to {ip}:{port}')
    sock.bind((ip, port))

    sock.setblocking(False)
    sock.listen(100)
    logging.info(f'Listening on {ip}:{port}')

    inputs = [sock]
    outputs = []
    while inputs:
        readable, writable, exceptional = select.select(inputs, outputs, inputs)

        for s in readable:
            try:
                if s == sock:
                    client, address = s.accept()
                    client.setblocking(False)
                    inputs.append(client)
                    logging.info(f'Connection: {address}')
                else:
                    data = s.recv(1024)
                    if data:
                        logging.info(f'Echo: {data.decode()}')
                        s.send(data)
                    else:
                        logging.info(f'Remove: {s}')
                        s.close()
                        inputs.remove(s)

            except Exception as ex:
                logging.warning(ex.args)
            finally:
                pass


def main():
    proc = multiprocessing.Process(target=server, args=['127.0.0.1', 40000], daemon=True, name='Server')

    while True:
        command = input('Enter a command (start, stop) ')
        if command == 'start':
            logging.info('Starting the server')
            try:
                proc.start()
            except AssertionError:
                logging.info(f'Cannot start a process twice')

        if command == 'stop':
            try:
                logging.info('Stopping the server')
                proc.terminate()
                proc.join()
                proc.close()
            except AttributeError:
                logging.info(f'You should start')
                break
            logging.info('Server stopped')
            break
    logging.info('Finish')


if __name__ == "__main__":
    main()
