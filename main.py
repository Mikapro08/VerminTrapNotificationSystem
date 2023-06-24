import cv2
import socket
import struct
import numpy


class MainBody:
    def __init__(self):
        pass

    def send_imgreq(self):
        pass

    def send_oknext(self):
        pass

    def upload_to_imgur(self):
        pass

    def save_img_local(self):
        pass

    def save_log(self):
        pass

    def post_to_ifttt(self):
        pass


ip_address = '127.0.0.1'
sens_port = 8080
cam_port = 8081


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock1: # 罠発動検知ユニットとの接続
    sock1.bind((ip_address, sens_port))  # バインド
    sock1.listen(1)  # 受信待機
    print('罠発動検知信号を待機しています…')
    while True:
        conn, addr = sock1.accept()  # 接続要求を受けいれる
        with conn:
            print('接続しました：', addr)
            recvbuf1 = conn.recv(6) # 信号識別符号を受信
            if not recvbuf1:
                break
            prefix = struct.unpack('!6s', recvbuf1)[0]
            print('受信した接頭辞：', prefix)
            if prefix == b'SENSED':
                print('罠発動検知信号を受信しました')
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock2:
                    sock2.connect((ip_address, cam_port))   # サーバに接続を要求する
                    sock2.sendall(b'IMGREQ')
                    print('写真撮影要求信号を送信しました')
                    recvbuf2 = sock2.recv(6)
                    if not recvbuf2:
                        break
                    prefix = struct.unpack('!6s', recvbuf2)[0]
                    print('受信した接頭辞：', prefix)
                    if prefix == b'IMGSIZ':
                        print('写真データサイズ予告信号を受信しました')
                        recvbuf3 = sock2.recv(4)
                        if not recvbuf3:
                            break
                        imgsiz = struct.unpack('!i', recvbuf3)[0]
                        print('予告された写真データサイズ：', imgsiz)
                        sock2.sendall(b'OKNEXT')
                        print('続行催促信号を送信しました')
                        recvbuf3 = sock2.recv(6)
                        if not recvbuf3:
                            break
                        prefix = struct.unpack('!6s', recvbuf3)[0]
                        print('受信した接頭辞：', prefix)
                        if prefix == b'IMGDAT':
                            print('写真データ信号を受信しました')
                            recvbuf3 = sock2.recv(imgsiz)
                            # 受信したデータをデコード
                            imgdata = numpy.frombuffer(recvbuf3, dtype=numpy.uint8)
                            # データを画像に変換
                            img = cv2.imdecode(imgdata, 1)
                            # 画像を表示
                            cv2.imshow('image', img)
                            # キー入力を待機
                            while True:
                                k = cv2.waitKey(1)
                                if k == 13:
                                    break
                            cv2.destroyAllWindows()
            else:
                print('受信した接頭辞：', prefix)
                print('よくわからない信号を受信しました')