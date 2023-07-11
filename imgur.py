#coding:UTF-8
#組込み開発プロジェクト１ グループ8
#害獣捕獲通知システム
#本体ユニット(main.py) 写真保存サービス(imgur)との通信部
#programmer:1CJK2104 近 佑斗

import requests
import json

def imgur_uproad(img_file):
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


pic = 'image/202306201800.jpg'      #写真のパス #RaspberryPiOS上ではフルパス #捕獲記録部との連結部分

link = imgur_uproad(pic)      #写真アップロードしてリンクを取得

print(link)     #デバッグ用リンク表示

#value2 = link #IFTTTとの通信部との連結部分