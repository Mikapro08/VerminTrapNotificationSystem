import cv2
import socket
import struct


ip_addr = '127.0.0.1'
port = 8080


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((ip_addr, port))           # サーバに接続を要求する
    sock.sendall(b'SENSED')