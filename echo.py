#!/usr/bin/python3

import socket

def listen():
    HOST = ''                # Symbolic name meaning all available interfaces
    PORT = 5555              # Arbitrary non-privileged port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break

                    datastr = data.decode('utf-8')

                    if datastr == 'quit\n':
                        conn.shutdown(1)
                        conn.close()
                        break

                    elif datastr == 'stop\n':
                        conn.shutdown(1)
                        conn.close()
                        exit()

                    elif data:
                        conn.send(data)
                        # print(datastr, end='')


if __name__ == "__main__":
    try:
        listen()
    except KeyboardInterrupt:
        pass
