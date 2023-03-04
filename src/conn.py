import struct
from socket import socket, AF_INET, SOCK_STREAM

import bcon


def recv_len(conn, length):
    data = b""
    tries = 0
    while len(data) < length:
        data += conn.recv(length - len(data))
        tries += 1
        if tries > 1000:
            raise Exception("recv() failed")

    return data

def send(conn, obj):
    data = bcon.dumps(obj)
    conn.send(struct.pack("<I", len(data)))
    conn.send(data)

def recv(conn):
    length = struct.unpack("<I", recv_len(conn, 4))[0]
    data = recv_len(conn, length)
    return bcon.loads(data)


def make_request(config, data):
    """
    Create connection, request, response.
    """
    conn = socket(AF_INET, SOCK_STREAM)
    conn.connect((config["ip"], config["port"]))
    send(conn, data)
    response = recv(conn)
    conn.close()
    return response
