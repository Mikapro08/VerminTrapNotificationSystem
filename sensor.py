import tkinter as tk
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
import time


#rootメインウィンドウの設定
root = tk.Tk()
root.title("害獣捕獲装置")
root.geometry("500x600")


#メインフレームの作成と設置
frame = tk.Frame(root)
frame.pack(fill = tk.BOTH, padx=20, pady=10)




#センサ発動時の処理
def send_socket():
    print('テスト')

def change_img():
    pass




#画像ファイルをインスタンス変数に代入
img1 = tk.PhotoImage(file="./img/Oniku1.png")
img1 = img1.subsample(3,3)

img2 = tk.PhotoImage(file="./img/Oniku2.png")
img2 = img2.subsample(3,3)


img= img1

#各種ウィジェットの作成
#ボタンの配置
button = tk.Button(frame, 
                   text="↑↑↑害獣のエサ↑↑↑",
                   width=400,height=400, 
                   image=img, compoun="top",
                   command= send_socket)

#ラベルの配置
label = tk.Label(frame, text='エサ', font=("MSゴシック","20","bold"))


#時間を表示する
#時計のラベルを作成
clock = tk.Label(root, font=("times",50,"bold"))


#時計を更新する関数
def tick():
    #現在の日時を取得   
    now = time.strftime("%H:%M:%S")
    #ラベルのテキストを更新
    clock.config(text=now)
    #1000msごとに再度tick関数を呼び出す
    clock.after(1000,tick)



#各種ウィジェットの設置
#label.pack(padx=10,pady=50,side=tk.TOP)
clock.pack(padx=5,pady=5,side=tk.TOP)
button.pack(padx=50,pady=30,side=tk.LEFT)


tick()
root.mainloop()