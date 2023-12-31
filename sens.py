import cv2
import socket
import struct
import tkinter as tk
import os
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

ip_addr = '127.0.0.1'
port = 8080
global img1
global img2


def reset():
    canvas_img.itemconfigure(photo1,image=img1)


class Sensor:
    def __init__(self):
        pass

    def send_sensed(self, e):
        print('罠が作動しました')
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock_main:
            sock_main.connect((ip_addr, port))  # 本体ユニット接続を要求する
            sock_main.sendall(b'SENSED')
            print("罠発動検知信号を送信しました")
        canvas_img.itemconfigure(photo1,image=img2)


sensor = Sensor()

root = tk.Tk()
cvs = tk.Canvas(width=900,height=600)
cvs.pack()

bg = tk.PhotoImage(file = "./InterfaceImg/Trap_bg.png")
cvs.create_image(450,400,image=bg)
msg = tk.Label(text='猛獣視点イメージ',
             bg='lightgreen',
             fg='black',
             font=100)

canvas_img = tk.Canvas(root,width=380,height=360,bd=-2,relief=tk.FLAT)

img1 = tk.PhotoImage(file="./InterfaceImg/Oniku1.png")
img2 = tk.PhotoImage(file="./InterfaceImg/Oniku2.png")

img1 = img1.subsample(2)
img2 = img2.subsample(2)
photo1 = canvas_img.create_image(190,170, image=img1)

canvas_img.tag_bind(photo1, "<Button-1>", sensor.send_sensed)
canvas_img.place(x=250,y=150)

button = tk.Button(text='リセット',
                  width=10,height=2, 
                  compoun="top",
                  command=reset)

#各種ウィジェットの設置
msg.place(x=50,y=30)
button.place(x=750,y=500)

root.mainloop()