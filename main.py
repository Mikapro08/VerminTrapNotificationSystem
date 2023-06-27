#組込み開発プロジェクト１ グループ8 害獣捕獲通知システム
#本体ユニット(main.py)
#Programmer(socket) : 1CJK2102 Mikihiko Takubo
#Programmer(imgur) : 1CJK2104 Yuto Kon
#Programmer(IFTTT) : 1CJK2106 Tomohito Abe

# coding: utf-8

import cv2
import socket
import struct
import numpy
import requests
import datetime
import json             # jsonデータ形式を利用するのでjsonライブラリをインポート
import urllib.request   # 標準のURLライブラリを利用する


class MainBody:
    def __init__(self):
        pass

    def send_imgreq(self):
        pass

    def send_oknext(self):
        pass

    def upload_to_imgur(self, img_file):
        client_id = '383dded1422ae4a'   #APIキー(固定)
        image_path = img_file    #写真のパス

        headers = {
            'authorization': f'Client-ID {client_id}',
        }
        files = {
            'image': (open(image_path, 'rb')),
        }

        r = requests.post('https://api.imgur.com/3/upload', headers=headers, files=files)   #写真のアップロードと情報取得

        url = json.loads(r.text)['data']['link']    #取得したjsonデータからリンクを抽出

        return url

    def save_img_local(self):
        pass

    def save_log(self):
        pass

    def post_to_ifttt(self, photolink):
        # In[1]:
        before = datetime.datetime.now()
        value1 = before.strftime('%Y/%m/%d %H:%M:%S')
        value2 = photolink   #写真保存サービス(imgur)との通信部で取得したURLを格納するようにする

        # In[2]:
        EventName = 'RP-posted'             ##IFTTT イベント名                 
        APIkey = 'd1N9nTzOZua9XmDPvF4RxP'   ##この中の''内を編集すれば使用するユーザを変更可
        url = f'https://maker.ifttt.com/trigger/{EventName}/with/key/{APIkey}'
        data = {
            'value1': value1 ,'value2': value2,
        }

        # Content-Type: application/json でデータを送信する
        headers = {
            'Content-Type': 'application/json',
        }

        # print(url)
        # print(data)
        # print(headers)

        # In[3]:
        # Request オブジェクト作成時に data パラメータ(json.dumps(data))を
        # 指定するとPOST メソッドとしてリクエストを飛ばすことができる
        # json.dumps(data)で、dataをjson形式に変換する

        rq = urllib.request.Request(url, json.dumps(data).encode(), headers)
        # print('URL=',rq, 'data=', rq)

        try:
            with urllib.request.urlopen(rq) as rs:
                body = rs.read()
                print(body)

        # HTTP ステータスコードが 4xx または 5xx だったとき
        except urllib.error.HTTPError as err:
            print('HTTP Error',err.code)
        # HTTP 通信に失敗したとき
        except urllib.error.URLError as err:
            print('URL Error',err.reason)



ip_address = '127.0.0.1'
sens_port = 8080
cam_port = 8081

mainbody = MainBody() #MainBodyのインスタンスを生成

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
                            # while True:
                            #     k = cv2.waitKey(1)
                            #     if k == 13:
                            #         break
                            # cv2.destroyAllWindows()

                            #ローカルに写真を保存(捕獲記録) #RaspberryPiOS上で実行する必要がある

                            pic = 'C:image/XXXXXXXXXX.jpg'      #写真のパス #RaspberryPiOS上ではフルパス #save_img_localとの連結部分

                            link = mainbody.upload_to_imgur(pic)      #写真アップロードしてリンクを取得

                            mainbody.post_to_ifttt(link)    #IFTTTにメッセージと写真リンクを送信
            else:
                print('受信した接頭辞：', prefix)
                print('よくわからない信号を受信しました')