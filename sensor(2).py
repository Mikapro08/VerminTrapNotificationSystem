import tkinter as tk
import random
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

global img1
global img2


def send_socket(e):
    print('test')
    canvas_img.itemconfigure(photo1,image=img2)

def reset():
    canvas_img.itemconfigure(photo1,image=img1)


root = tk.Tk()
cvs = tk.Canvas(width=900,height=600)
cvs.pack()


bg = tk.PhotoImage(file = "./InterfaceImg/Trap_bg.png")
cvs.create_image(450,400,image=bg)
msg=tk.Label(text='猛獣視点イメージ',
             bg='lightgreen',
             fg='black',
             font=100)



canvas_img = tk.Canvas(root,width=380,height=360)

img1 = tk.PhotoImage(file="./InterfaceImg/Oniku1.png")
img2 = tk.PhotoImage(file="./InterfaceImg/Oniku2.png")

img1 = img1.subsample(2)
img2 = img2.subsample(2)
photo1 = canvas_img.create_image(190,170, image=img1)

canvas_img.tag_bind(photo1, "<Button-1>", send_socket)
canvas_img.place(x=250,y=150)

button = tk.Button(text='リセット',
                  width=10,height=2, 
                  compoun="top",
                  command=reset)


#各種ウィジェットの設置
msg.place(x=50,y=30)
button.place(x=750,y=500)

root.mainloop()