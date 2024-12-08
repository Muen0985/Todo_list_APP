import tkinter as tk

root = tk.Tk()
root.title('oxxo.studio')
root.geometry('200x200')

# 定義 show 函式，印出勾選的值
def show():
    print(var1.get(), var2.get())   # 使用 get() 方法取得變數內容

var1 = tk.StringVar()   # 設定文字變數，並綁定第一個 Checkbutton
check_btn1 = tk.Checkbutton(root, text='Apple',
                            variable=var1, onvalue='Apple', offvalue='--',
                            command=show)
check_btn1.pack()
check_btn1.deselect()   # 開始時不要勾選

var2 = tk.StringVar()   # 設定文字變數，並綁定第二個 Checkbutton
check_btn2 = tk.Checkbutton(root, text='Banana',
                            variable=var2, onvalue='Banana', offvalue='--',
                            command=show)
check_btn2.pack()
check_btn2.deselect()   # 開始時不要勾選

root.mainloop()