import socket
import struct
import cv2

ip_address = '127.0.0.1'
port = 8081

img = cv2.imread('nicecat.jpg')
# print(type(img))
# cv2.imshow('image', img)
# while True:
#     k = cv2.waitKey(1)
#     if k == 13:
#         break
imgsiz = img.size
encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
result, imgdata = cv2.imencode('.jpg', img, encode_param)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.bind((ip_address, port))
    sock.listen(1)

    while True:
        print('写真撮影要求信号を待機しています…')
        sock2, addr = sock.accept()
        with sock2:
            print('接続しました：', addr)
            recvbuf = sock2.recv(6)
            if not recvbuf:
                break
            prefix = struct.unpack('!6s', recvbuf)[0]
            print('受信した接頭辞：', prefix)
            if prefix != b'IMGREQ':
                break
            print('写真撮影要求信号を受信しました')
            sendbuf = struct.pack('!6si', b'IMGSIZ', imgsiz)
            sock2.sendall(sendbuf)
            print('写真データサイズ予告信号を送信しました')
            recvbuf = sock2.recv(6)
            if not recvbuf:
                break
            prefix = struct.unpack('!6s', recvbuf)[0]
            print('受信した接頭辞：', prefix)
            if prefix != b'OKNEXT':
                break
            print('続行催促信号を受信しました')
            sock2.sendall(b'IMGDAT')
            sock2.sendall(imgdata)
            print('写真データ信号を送信しました')