#imgurにアップロードされた害獣画像をIFTTTに共有する
#Programmer : 1CJK2106 Tomohito Abe

# coding: utf-8
# In[1]:
import tkinter
import datetime
import json             # jsonデータ形式を利用するのでjsonライブラリをインポート
import urllib.request   # 標準のURLライブラリを利用する
# urllibの代わりに、Python の HTTP 通信ライブラリとして、Requests ライブラリがある。
# Requests はurllibよりもシンプルに、プログラムを記述できる。ただしインストール必要。
# In[2]:
before = datetime.datetime.now()
value1 = before.strftime('%Y/%m/%d %H:%M:%S')
value2 = "https://i.imgur.com/1bn2WJl.png"   ##後々main.pyで取得したURLを格納するようにする

# In[3]:
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

# In[5]:
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


