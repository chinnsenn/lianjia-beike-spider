import threading
import tkinter as tk
from time import ctime,sleep
 
# 创建主窗口
window = tk.Tk()
window.title('测试')
window.geometry('630x200')
 
def music():
    for i in range(2):
        print("I was listening to music %s" % ctime())
        sleep(1)
 
def move():
    for i in range(2):
        print("I was at the movie  %s" % ctime())
        sleep(1)
 
def test():
    # 多线程
    threads = []
    t1 = threading.Thread(target=music)
    threads.append(t1)
    t2 = threading.Thread(target=move)
    threads.append(t2)
    for t in threads:
        t.setDaemon(True)
        t.start()
 
btn_download = tk.Button(window, text='启动', command=test)
btn_download.place(x=400, y=150)
 
window.mainloop()