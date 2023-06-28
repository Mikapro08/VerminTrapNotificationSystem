import cv2
import socket
import struct


ip_addr = '127.0.0.1'
port = 8080


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_main:
    sock_main.connect((ip_addr, port))  # 本体ユニット接続を要求する
    sock_main.sendall(b'SENSED')