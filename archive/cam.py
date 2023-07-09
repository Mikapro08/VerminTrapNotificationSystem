import socket
import struct
import cv2

ip_address = '127.0.0.1'
port = 8081

img = cv2.imread('nicecat.jpg')
imgsiz = img.size
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
result, imgdata = cv2.imencode('.jpg', img, encode_param)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_cam:
    sock_cam.bind((ip_address, port))
    sock_cam.listen(1)

    while True:
        print('写真撮影要求信号を待機しています…')
        sock_main, addr = sock_cam.accept()
        with sock_main:
            print('接続しました：', addr)
            recvbuf = sock_main.recv(6)
            if not recvbuf:
                break
            prefix = struct.unpack('!6s', recvbuf)[0]
            print('受信した接頭辞：', prefix)
            if prefix != b'IMGREQ':
                break
            print('写真撮影要求信号を受信しました')
            sendbuf = struct.pack('!6si', b'IMGSIZ', imgsiz)
            sock_main.sendall(sendbuf)
            print('写真データサイズ予告信号を送信しました')
            recvbuf = sock_main.recv(6)
            if not recvbuf:
                break
            prefix = struct.unpack('!6s', recvbuf)[0]
            print('受信した接頭辞：', prefix)
            if prefix != b'OKNEXT':
                break
            print('続行催促信号を受信しました')
            sock_main.sendall(b'IMGDAT')
            sock_main.sendall(imgdata)
            print('写真データ信号を送信しました')