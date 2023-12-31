# 組込み開発プロジェクト１ グループ8 害獣捕獲通知システム
# 本体ユニット(main.py)
# Programmer(socket) : 1CJK2102 Mikihiko Takubo
# Programmer(imgur)  : 1CJK2104 Yuto Kon
# Programmer(IFTTT)  : 1CJK2106 Tomohito Abe

# coding: utf-8

import cv2              # 画像を扱うためにインポート
import numpy            # OpenCVで画像を扱う際のオブジェクトが内部的にnumpyのオブジェクトであるためインポート
import socket           # ソケット通信をするためにインポート
import struct           # ソケット通信をする際にデータをパック・アンパックするためにインポート
import requests
import datetime         # 日付時刻をファイル名にして写真を保存するためにインポート
import os               # カレントディレクトリを設定するためにインポート
import json             # jsonデータ形式を利用するのでjsonライブラリをインポート
import urllib.request   # 標準のURLライブラリを利用する


debug = False


class MainBody:
    def __init__(self):
        pass

    
    def send_imgreq(self, sock):
        sock.sendall(b'IMGREQ')                     # 写真撮影要求信号を送信
        print('写真撮影要求信号を送信しました')

    
    def send_oknext(self, sock):
        sock.sendall(b'OKNEXT')                     # 続行催促信号を送信
        print('続行催促信号を送信しました')

    
    def save_img_local(self, img):
        print(type(img))
        nowdate = datetime.datetime.now()
        path = nowdate.strftime('./OutputImg/%Y-%m-%d_%H-%M-%S-%f.jpg')
        os.chdir(os.path.dirname(os.path.abspath(__file__)))    # このファイルが存在する場所をカレントディレクトリに設定
        cv2.imwrite(path, img)
        print('写真をローカルに保存しました')
        return path

    
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


    def post_to_ifttt(self, photolink):
        # In[1]:
        before = datetime.datetime.now()
        value1 = before.strftime('%Y/%m/%d %H:%M:%S')
        value2 = photolink   #写真保存サービス(imgur)との通信部で取得したURLを格納するようにする

        # In[2]:
        EventName = 'RP-posted'             ##IFTTT イベント名                 
        # APIkey = 'd1N9nTzOZua9XmDPvF4RxP'   ##この中の''内を編集すれば使用するユーザを変更可
        APIkey = 'dLkCI-wnfwQV0sJGXLOU-s'   ##この中の''内を編集すれば使用するユーザを変更可
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

mainbody = MainBody()                                                       # MainBodyのインスタンスを生成

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_main:        # 罠発動検知ユニットとの接続
    sock_main.bind((ip_address, sens_port))                                 # バインド
    sock_main.listen(1)                                                     # 受信待機
    print('罠発動検知信号を待機しています…')
    while True:
        sock_sens, addr = sock_main.accept()                                # 接続要求を受けいれる
        with sock_sens:
            print('接続しました：', addr)

            recvbuf = sock_sens.recv(6)                                     # 信号識別符号を受信
            if not recvbuf:
                break
            prefix = struct.unpack('!6s', recvbuf)[0]
            print('受信した接頭辞：', prefix)
            if prefix != b'SENSED':
                break
            print('罠発動検知信号を受信しました')

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_cam:
                sock_cam.connect((ip_address, cam_port))                    # カメラユニットに接続を要求する

                mainbody.send_imgreq(sock_cam)                              # 写真撮影要求信号を送信

                recvbuf = sock_cam.recv(6)                                  # 信号識別符号を受信
                if not recvbuf:
                    break
                prefix = struct.unpack('!6s', recvbuf)[0]
                print('受信した接頭辞：', prefix)
                if prefix != b'IMGSIZ':
                    break
                print('写真データサイズ予告信号を受信しました')
                recvbuf = sock_cam.recv(4)                                  # データサイズを受信
                if not recvbuf:
                    break
                imgsiz = struct.unpack('!i', recvbuf)[0]
                print('予告された写真データサイズ：', imgsiz)

                mainbody.send_oknext(sock_cam)                              # 続行催促信号を送信

                recvbuf = sock_cam.recv(6)                                  # 信号識別符号を受信
                if not recvbuf:
                    break
                prefix = struct.unpack('!6s', recvbuf)[0]
                print('受信した接頭辞：', prefix)
                if prefix != b'IMGDAT':
                    break
                print('写真データ信号を受信しました')
                recvbuf = sock_cam.recv(imgsiz)                             # 写真データを受信
            
            imgdata = numpy.frombuffer(recvbuf, dtype=numpy.uint8)          # 受信したデータをデコード
            img = cv2.imdecode(imgdata, 1)                                  # データを画像に変換
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)                      # PillowはRGB,cv2はBGRなので変換が必要

            if debug == True:
                cv2.imshow('image', img)                                        # 画像を表示
                while True:
                    k = cv2.waitKey(1)                                          # キー入力を待機
                    if k == 13:                                                 # Enterキー
                        break
                cv2.destroyAllWindows()

            pic_path = mainbody.save_img_local(img)                         # ローカルに写真を保存(RaspberryPiOS上で実行して検証するべき)

            link = mainbody.upload_to_imgur(pic_path)                       # 写真アップロードしてリンクを取得

            mainbody.post_to_ifttt(link)                                    # IFTTTにメッセージと写真リンクを送信