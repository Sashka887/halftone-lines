import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import os
import shutil
import re

def run_script():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    raw_path = entry_img.get()
    
    if not raw_path or not os.path.exists(raw_path):
        messagebox.showerror("Ошибка", "Сначала выбери картинку!")
        return

    try:
        # 1. Подготовка локального файла
        local_input = os.path.join(base_dir, "temp_input.jpg")
        shutil.copy2(raw_path, local_input)
        
        # 2. Чистка RGB (убираем лишнее, оставляем только (R,G,B) без пробелов)
        def clean_rgb(val):
            digits = re.findall(r'\d+', val)
            if len(digits) != 3: return "(0,0,0)"
            return f"({digits[0]},{digits[1]},{digits[2]})"

        # 3. Сборка команды со ВСЕМИ параметрами из README
        cmd = [
            "python", "-W", "ignore", "halftone_lines_cmd.py",
            "-s", entry_side.get(),      # Side (Плотность)
            "-k", entry_kernel.get(),    # Kernel (Зерно)
            "-al", entry_alpha.get(),    # Alpha (Толщина линий)
            "-an", entry_angle.get(),    # Angle (Угол наклона)
            "-bg", clean_rgb(entry_bg.get()), # Background
            "-fg", clean_rgb(entry_fg.get())  # Foreground
        ]
        
        if var_invert.get(): cmd.append("-nv") # Инверсия
        if var_no_contrast.get(): cmd.append("-nc") # Отключить авто-контраст

        cmd.append("temp_input.jpg")

        # 4. Выполнение
        result = subprocess.run(cmd, cwd=base_dir, capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode == 0:
            messagebox.showinfo("Готово", "Картинка создана! Ищи файл с префиксом out- в папке.")
        else:
            messagebox.showerror("Ошибка скрипта", result.stderr if result.stderr else result.stdout)
            
    except Exception as e:
        messagebox.showerror("Ошибка GUI", str(e))

def select_file():
    path = filedialog.askopenfilename()
    if path:
        entry_img.delete(0, tk.END)
        entry_img.insert(0, path)

# Визуал
root = tk.Tk()
root.title("Halftone Lines Full PRO")
root.geometry("550x550")

# Блок настроек
frame = tk.LabelFrame(root, text=" Полный список параметров ")
frame.pack(padx=15, pady=10, fill="x")

# Сетка параметров (2 колонки для компактности)
params = [
    ("Плотность (-s):", "100", 0, 0),
    ("Ядро (-k):", "3", 1, 0),
    ("Толщина линий (-al):", "1", 0, 2),
    ("Угол наклона (-an):", "45", 1, 2),
    ("Фон RGB:", "255,255,255", 2, 0),
    ("Линии RGB:", "0,0,0", 3, 0)
]

entries = {}
for text, default, r, c in params:
    tk.Label(frame, text=text).grid(row=r, column=c, padx=5, pady=5, sticky="w")
    e = tk.Entry(frame, width=15)
    e.insert(0, default)
    e.grid(row=r, column=c+1, padx=5, pady=5)
    entries[text] = e

# Распаковываем ссылки на инпуты для функции run_script
entry_side, entry_kernel = entries["Плотность (-s):"], entries["Ядро (-k):"]
entry_alpha, entry_angle = entries["Толщина линий (-al):"], entries["Угол наклона (-an):"]
entry_bg, entry_fg = entries["Фон RGB:"], entries["Линии RGB:"]

# Чекбоксы
var_invert = tk.IntVar()
tk.Checkbutton(frame, text="Инвертировать (-nv)", variable=var_invert).grid(row=4, column=0, columnspan=2)
var_no_contrast = tk.IntVar()
tk.Checkbutton(frame, text="Без авто-контраста (-nc)", variable=var_no_contrast).grid(row=4, column=2, columnspan=2)

# Выбор файла
tk.Label(root, text="Исходное изображение:").pack(pady=5)
entry_img = tk.Entry(root, width=60)
entry_img.pack()
tk.Button(root, text="Выбрать файл", command=select_file).pack(pady=5)

# Кнопка старта
tk.Button(root, text="СГЕНЕРИРОВАТЬ ШЕДЕВР", command=run_script, bg="#27ae60", fg="white", font=("Arial", 12, "bold"), height=2).pack(pady=20)

root.mainloop()