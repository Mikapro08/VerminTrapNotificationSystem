#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
# カメラウィンドウ（Camera.py）
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------
# モジュールのimport
#-------------------------------------------------------------------------------------------------------------------

# GUI系モジュール
import tkinter
from tkinter import ttk
from tkinter import messagebox
import datetime
import os

# 映像処理系モジュール
import cv2
import PIL.Image, PIL.ImageTk

#-------------------------------------------------------------------------------------------------------------------
# メインコード
#-------------------------------------------------------------------------------------------------------------------

os.chdir(os.path.dirname(os.path.abspath(__file__))) # カレントディレクトリをこの.pyが所在するディレクトリへ設定

class Camera(tkinter.Frame):

    # windowの初期設定
    def __init__(self, master = None):

        super().__init__(master)                                               # 初期化
        self.master.geometry("640x580")                                        # windowサイズの指定
        self.master.resizable(False, False)                                    # windowサイズ変更の無効化
        self.master.title("害獣捕獲通知システム")                               # windowタイトルの設定

        self.Timestamp_var = tkinter.IntVar()
        self.scalevar_Bright = tkinter.DoubleVar()
        self.button_img = tkinter.PhotoImage(file="cameraicon.png")

        self.MovieCanvas()
        self.Widget()

    # window内のカメラ映像表示部分（canvas定義とカメラ読み込み）
    def MovieCanvas(self):

        self.vcp = cv2.VideoCapture(0)
        
        self.width = self.vcp.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vcp.get(cv2.CAP_PROP_FRAME_HEIGHT)

        self.canvas = tkinter.Canvas(self.master, width= self.width-6, height=self.height-6, relief=tkinter.SOLID, bd=2)
        self.canvas.grid(row=0,column=0)
        self.canvas.place(x=0,y=0)

        self.update()

    # カメラ画像の更新関数
    def update(self):
            
            self.rat, self.frame = self.vcp.read()
            self.frame = cv2.flip(self.frame,1)
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) 

            self.vcp.set(cv2.CAP_PROP_BRIGHTNESS, self.scalevar_Bright.get())

            if self.Timestamp_var.get() == 0:

                cv2.rectangle(self.frame, (380, 450), (670, 490), (255, 255, 255),thickness=-1)
                cv2.putText(self.frame,
                            text=f"{str(datetime.datetime.now().year)} {str(datetime.datetime.now().month).zfill(2)}/{str(datetime.datetime.now().day).zfill(2)} {str(datetime.datetime.now().hour).zfill(2)}:{str(datetime.datetime.now().minute).zfill(2)}:{str(datetime.datetime.now().second).zfill(2)}",
                            org=(385, 472),
                            fontFace=cv2.FONT_HERSHEY_SIMPLEX,
                            fontScale=0.7,
                            color=(0, 0, 0),
                            thickness=2,
                            lineType=cv2.LINE_AA)

            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(self.frame))

            #《↓ここにソケット通信系のコードを挿入↓》

            #《↑ここにソケット通信系のコードを挿入↑》
            
            self.canvas.create_image(0,0, image= self.photo, anchor = tkinter.NW)
            self.master.after(1, self.update)

    # ウィジェット系の設定全般
    def Widget(self):

        # カメラ設定（明るさ）のスライダー・リセットボタン

        def Brightreset():

            self.vcp.set(cv2.CAP_PROP_BRIGHTNESS, self.scalevar_Bright.set(0))

        labelframe_Bright_lever = ttk.LabelFrame(self.master, text="明るさ設定", relief=tkinter.GROOVE)
        labelframe_Bright_lever.place(x=10,y=485)

        self.scale_Bright = ttk.Scale(labelframe_Bright_lever, from_=-50, to=50, length = 200, variable=self.scalevar_Bright)
        self.scale_Bright.pack(padx=10,pady=0,side=tkinter.LEFT)

        self.button_resetBright = ttk.Button(labelframe_Bright_lever, text="明るさリセット", padding=[5,10,5,10], command=Brightreset)
        self.button_resetBright.pack(padx=5,pady=15,side=tkinter.LEFT)

        # タイムスタンプのON・OFF切り替えラジオボタン

        labelframe_TimeStamp = ttk.LabelFrame(self.master, text="タイムスタンプ表示・記録", relief=tkinter.GROOVE)
        labelframe_TimeStamp.place(x=330,y=485)

        self.Timestamp_boolean = ["ON","OFF"]

        for i in range(len(self.Timestamp_boolean)):
            self.Timestamp_ONOFF = ttk.Radiobutton(labelframe_TimeStamp, value=i, variable=self.Timestamp_var, text=self.Timestamp_boolean[i])
            self.Timestamp_ONOFF.pack(padx=15,pady=25.5,side=tkinter.LEFT)

        # カメラ動作確認用ボタン（.pyファイル直下ディレクトリに保存）

        def shutter(e):
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
            self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB) 
            cv2.imwrite('test.png',self.frame)
            messagebox.showinfo("カメラ画像保存",f"test.pngをフォルダ\n{os.path.dirname(os.path.abspath(__file__))}\nに保存しました。")

        self.canvas_camcheck = tkinter.Canvas(self.master, width=70, height=75)

        self.button_img = self.button_img.subsample(4)
        self.button_cam = self.canvas_camcheck.create_image(36.5, 35.5, image=self.button_img)

        self.canvas_camcheck.tag_bind(self.button_cam, "<Button-1>", shutter)

        self.canvas_camcheck.place(x=520,y=485)

        self.canvas_camcheck_text = tkinter.Label(text="テスト撮影", foreground="#00a1ae")
        self.canvas_camcheck_text.place(x=530,y=555)

def main():

    app = Camera(master=tkinter.Tk())
    app.mainloop()

if __name__ == "__main__":
    main()