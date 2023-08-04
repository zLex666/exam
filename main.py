import tkinter as tk
from tkinter import ttk
from connect import connection
from ttkthemes import ThemedStyle
from tkinter import messagebox
from auth_user_products import auth_user
from manager import manager
from admin import admin

main_win = tk.Tk()
main_win.geometry('400x360')
main_win.title('Спорт магазин')
main_win.resizable(False,False)

style = ThemedStyle(main_win)
style.set_theme("arc")

l1 = tk.Label(text='Добро пожаловать в спорт-магазин', font='Times 16', bd=3,)
l1.pack(pady=20)

b1 = tk.Button(text='Войти в аккаунт', font='Times 14', width=25, height=2,  background='white', bd=3, command=auth_user)
b1.pack(pady=6)
b1.place(x=70, y=80)

b3 = tk.Button(text='Войти как администратор', font='Times 14', width=25, height=2,  background='white', bd=3, command=admin)
b3.pack(pady=6)
b3.place(x=70, y=200)

b4 = tk.Button(text='Войти как менеджер', font='Times 14', width=25, height=2,  background='white', bd=3, command=manager)
b4.pack(pady=6)
b4.place(x=70, y=260)

main_win.mainloop()