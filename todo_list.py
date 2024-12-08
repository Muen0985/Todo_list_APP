import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import requests
from datetime import datetime

list_api="http://127.0.0.1:5000/todos"

selected_task_info = None 
selected_task_label = None  
selected_bool=False

def select_task(task_label, task_details):
    global selected_task_info, selected_task_label, selected_bool

    if selected_bool is False:
        selected_task_info = task_details
        selected_task_label = task_label
        selected_bool=True
        
        task_label.config(font=("Comic Sans MS", 18),fg="#f05c51")
        print(f"Selected Task: {selected_task_info}, {selected_bool}")

    else:
        selected_task_info = None
        selected_task_label = None
        selected_bool = False

        task_label.config(font=("Comic Sans MS", 15),fg="#000000") 
        print("Deselected Task: No task selected")
        print(f'{selected_task_info},{selected_bool}')
    

def add_task_tolistframe(task_detail):
    # 每個任務的容器框架
    task_frame = tk.Frame(task_list_frame)
    task_frame.pack(fill="x", pady=5)

    # Label 顯示任務文字
    task_label = tk.Label(task_frame, text=task_detail['title'], font=("Comic Sans MS", 14), anchor="w")
    task_label.pack(side="left", fill="x", expand=True, padx=10)

    # Checkbutton 連結狀態變數
    task_var = tk.BooleanVar()  # 用於追蹤該任務的打勾狀態
    task_checked = task_var.get() # 返回true或false
    task_checkbutton = tk.Checkbutton(task_frame, variable=task_var)
    task_checkbutton.pack(side="right", padx=10)

    task_label.bind("<Button-1>", lambda e: select_task(task_label, task_detail))
    task_checkbutton.bind("<Button-1>", lambda e: update_task(task_detail, not task_var.get()))

# for debug
def findelement(td,tc):
    print(td)
    print(tc)
    print('-----')

def fetch_todo():
    try:
        response=requests.get(list_api)
        response.raise_for_status() 
        todos=response.json()

        for widget in task_list_frame.winfo_children():
            widget.destroy()
        for do in todos:
            print(do)
            add_task_tolistframe(do)

    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch todos: {e}")

def add_task():
    task_title=task_entry.get()
    if task_title.strip():
        try:
            response=requests.post(list_api,json={"title":task_title})
            response.raise_for_status()
            fetch_todo()
            task_entry.delete(0,tk.END)
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to add todo: {e}")

def update_task(updated_task,task_checked):
    try:
        list_api_update=f"{list_api}/updatetodo/{updated_task['id']}"
        if updated_task is not None and task_checked is None:
            response=requests.put(list_api_update,json=updated_task)
            print("goes from updated task")
            for widget in task_list_frame.winfo_children():
                widget.destroy()
            fetch_todo()
        elif task_checked is not None :
            response=requests.put(list_api_update,json={
                "id": updated_task["id"],
                "title": updated_task["title"],
                "completed": task_checked})
            print("goes from task_checked")
        else:
            response=requests.put(list_api_update,json=selected_task_info)
            print("goes from text updated task")
        response.raise_for_status()
        
        selected_task_info = None
        print("end of the function")
    except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to update list: {e}")
    

def delete_task():
    global selected_task_info
    try:
        response=requests.delete(f"{list_api}/deletetodo/{selected_task_info['id']}")
        response.raise_for_status()
        selected_task_info = None
        fetch_todo()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to delete task: {e}")


def clear_db():
    try:
        response=requests.delete(list_api+"/clearlist")
        response.raise_for_status()
        selected_task_info = None 
        for widget in task_list_frame.winfo_children():
            widget.destroy()
    except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to clear list: {e}")

def open_update_window():
    popup = tk.Toplevel()
    popup.title("Update Task")
    popup.geometry("300x200")
    popup.resizable(False, False)
    
    tk.Label(popup, text="Task Title:", font=("Arial", 12)).pack(pady=5)
    title_entry = tk.Entry(popup, font=("Arial", 12))
    title_entry.insert(0, selected_task_info.get('title', ''))
    title_entry.pack(pady=5, padx=10, fill="x")
    
    def submit_update():
        updated_task = {
            "id": selected_task_info["id"],
            "title": title_entry.get(),
            "completed": selected_task_info["completed"]
        }
        try:
            update_task(updated_task,None)
            popup.destroy()  
        except Exception as e:
            messagebox.showerror("Error", f"Failed to update task: {e}")
    
    submit_button = tk.Button(
        popup, 
        text="Update Task", 
        font=("Arial", 12, "bold"), 
        bg="#4CAF50", 
        fg="white", 
        command=submit_update
    )
    submit_button.pack(pady=10)


def round_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    """在 Canvas 上繪製圓角矩形"""
    points = [
        (x1 + radius, y1),
        (x1 + radius, y1),
        (x2 - radius, y1),
        (x2 - radius, y1),
        (x2, y1),
        (x2, y1 + radius),
        (x2, y1 + radius),
        (x2, y2 - radius),
        (x2, y2 - radius),
        (x2, y2),
        (x2 - radius, y2),
        (x2 - radius, y2),
        (x1 + radius, y2),
        (x1 + radius, y2),
        (x1, y2),
        (x1, y2 - radius),
        (x1, y2 - radius),
        (x1, y1 + radius),
        (x1, y1 + radius),
        (x1, y1),
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


# 初始化主視窗
root = tk.Tk()
root.title("Cute Todo List")
root.geometry("420x580")
root.resizable(False, False)
root.configure(bg="#FFFAF0")

# 背景
canvas = tk.Canvas(root, width=420, height=580, bg="#bad7f5", highlightthickness=0)
canvas.pack(fill="both", expand=True)
round_rectangle(canvas, 10, 10, 410, 570, radius=30, fill="#FFE4E1", outline="")

# 顯示今天日期
today_date = datetime.today().strftime("%Y-%m-%d")
date_label = tk.Label(
    root,
    text=f"Today: {today_date}",
    font=("Comic Sans MS", 11),
    fg="#FF69B4",
    bg="#FFE4E1",
)
date_label.place(x=140, y=60)

# 標題區域
title_label = tk.Label(
    root,
    text="Cute Todo List 🐾",
    font=("Comic Sans MS", 20, "bold"),
    fg="#FF69B4",
    bg="#FFE4E1",
)
title_label.place(x=110, y=20)

# 輸入區域
input_frame = tk.Frame(root, bg="#FFE4E1")
input_frame.place(x=20, y=80, width=380, height=60)

task_entry = ttk.Entry(input_frame, font=("Comic Sans MS", 14))
task_entry.pack(side="left", padx=10, pady=10, expand=True, fill="x")

add_button = tk.Button(
    input_frame,
    text="Add 📌",
    font=("Comic Sans MS", 12, "bold"),
    bg="#FFB6C1",
    fg="white",
    relief="flat",
    activebackground="#FF69B4",
    activeforeground="white",
    command=add_task
)
add_button.pack(side="right", padx=10)

# 清單區域
task_list_frame = tk.Frame(root, bg="#FFE4E1")
task_list_frame.place(x=20, y=150, width=380, height=330)

# 控制按鈕區域
control_frame = tk.Frame(root, bg="#FFE4E1")
control_frame.place(x=20, y=500, width=380, height=60)

delete_button = tk.Button(
    control_frame,
    text="Delete 🗑️",
    font=("Comic Sans MS", 12, "bold"),
    bg="#FFB6C1",
    fg="white",
    relief="flat",
    activebackground="#FF69B4",
    activeforeground="white",
    command=delete_task
)
delete_button.pack(side="left", padx=20)

fix_button = tk.Button(
    control_frame,
    text="Update 🖊",
    font=("Comic Sans MS", 12, "bold"),
    bg="#FFB6C1",
    fg="white",
    relief="flat",
    activebackground="#FF69B4",
    activeforeground="white",
    command=open_update_window
)
fix_button.pack(side="right", padx=10)

clear_button = tk.Button(
    control_frame,
    text="Clear 🧹",
    font=("Comic Sans MS", 12, "bold"),
    bg="#FFB6C1",
    fg="white",
    relief="flat",
    activebackground="#FF69B4",
    activeforeground="white",
    command=clear_db
)
clear_button.pack(side="right", padx=10)

try:
    fetch_todo()
except:
    print("fetch list susscessfully")
# 啟動主迴圈
root.mainloop()