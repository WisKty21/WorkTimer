import tkinter as tk
import time
import sqlite3
import matplotlib.pyplot as plt

# データベースのセットアップ
def setup_db():
    conn = sqlite3.connect('work_time.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS work_log (id INTEGER PRIMARY KEY, start_time TEXT, end_time TEXT, duration REAL)''')
    conn.commit()
    conn.close()

# タイマーのスタート
def start_timer():
    global start_time
    start_time = time.time()
    start_button.config(state='disabled')
    stop_button.config(state='normal')

# タイマーのストップ
def stop_timer():
    global start_time
    end_time = time.time()
    duration = end_time - start_time
    save_record(start_time, end_time, duration)
    start_button.config(state='normal')
    stop_button.config(state='disabled')

# レコードを保存
def save_record(start, end, duration):
    conn = sqlite3.connect('work_time.db')
    c = conn.cursor()
    c.execute('''INSERT INTO work_log (start_time, end_time, duration) VALUES (?, ?, ?)''', (time.ctime(start), time.ctime(end), duration))
    conn.commit()
    conn.close()

# 日々の記録を可視化
def visualize():
    conn = sqlite3.connect('work_time.db')
    c = conn.cursor()
    c.execute('SELECT start_time, duration FROM work_log')
    records = c.fetchall()
    conn.close()

    dates = [rec[0] for rec in records]
    durations = [rec[1] for rec in records]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, durations, marker='o')
    plt.xticks(rotation=45)
    plt.xlabel('Date')
    plt.ylabel('Duration (seconds)')
    plt.title('Work Time Record')
    plt.show()

# GUIのセットアップ
root = tk.Tk()
root.title("Work Time Tracker")

start_button = tk.Button(root, text="Start", command=start_timer)
start_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop_timer, state='disabled')
stop_button.pack()

visualize_button = tk.Button(root, text="Visualize", command=visualize)
visualize_button.pack()

# データベースの初期化
setup_db()

root.mainloop()
