#!/usr/bin/python3

from time import sleep
import socket

INQ_FOCUS = [0x81, 0x09, 0x04, 0x48, 0xFF]
INQ_ZOOM = [0x81, 0x09, 0x04, 0x47, 0xFF]
INQ_PANTILT = [0x81, 0x09, 0x06, 0x12, 0xFF]

RECALL_PRESET = [0x81, 0x01, 0x04, 0x3F, 0x02, 0x00, 0xFF]
RECALL_PRESET_RESP = [0x90, 0x42, 0xFF, 0x90, 0x52, 0xFF]

presets = [
    {
        'FOCUS': [0x90, 0x50, 0x00, 0x06, 0x05, 0x05, 0xFF],
        'ZOOM': [0x90, 0x50, 0x00, 0x00, 0x00, 0x00, 0xF],
        'PANTILT':
            [0x90, 0x50, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0xFF],
    },
    {
        'FOCUS': [0x90, 0x50, 0x00, 0x06, 0x05, 0x04, 0xFF],
        'ZOOM': [0x90, 0x50, 0x00, 0x00, 0x00, 0x00, 0xFF],
        'PANTILT':
            [0x90, 0x50, 0x00, 0x00, 0x09, 0x0E, 0x00, 0x00, 0x00, 0x0F, 0xFF],
    },
    {
        'FOCUS': [0x90, 0x50, 0x00, 0x01, 0x0D, 0x0D, 0xFF],
        'ZOOM': [0x90, 0x50, 0x02, 0x0F, 0x0F, 0x0D, 0xFF],
        'PANTILT':
            [0x90, 0x50, 0x00, 0x00, 0x00, 0x0F, 0x0F, 0x0F, 0x0B, 0x09, 0xFF],
    },
    {
        'FOCUS': [0x90, 0x50, 0x00, 0x02, 0x05, 0x05, 0xFF],
        'ZOOM': [0x90, 0x50, 0x02, 0x0A, 0x0E, 0x02, 0xFF],
        'PANTILT':
            [0x90, 0x50, 0x00, 0x00, 0x07, 0x05, 0x0F, 0x0F, 0x0B, 0x06, 0xFF],
    },
]

current_preset = 0


def listen():
    HOST = ''                # Symbolic name meaning all available interfaces
    PORT = 5678              # Arbitrary non-privileged port
    global current_preset

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen(1)
        while True:
            conn, addr = s.accept()
            with conn:
                # print("new connection")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break

                    # convert to array of ints
                    data = [x for x in data]

                    if data == INQ_FOCUS:
                        d = presets[current_preset]['FOCUS']
                        print("Responding to INQ_FOCUS with", d)
                        conn.sendall(bytes(d))

                    elif data == INQ_ZOOM:
                        d = presets[current_preset]['ZOOM']
                        print("Responding to INQ_ZOOM with", d)
                        conn.sendall(bytes(d))

                    elif data == INQ_PANTILT:
                        d = presets[current_preset]['PANTILT']
                        print("Responding to INQ_PANTILT with", d)
                        conn.sendall(bytes(d))

                    elif (data[0:4] == RECALL_PRESET[0:4] and
                          data[6] == RECALL_PRESET[6]):

                        current_preset = data[5]
                        if current_preset < 0:
                            current_preset = 0
                        elif current_preset >= len(presets):
                            current_preset = len(presets) - 1

                        print("Recall preset", current_preset)
                        conn.sendall(bytes(RECALL_PRESET_RESP))
                        sleep(0.5)

                    break


if __name__ == "__main__":
    try:
        listen()
    except KeyboardInterrupt:
        pass
