import tkinter as tk
from tkinter import ttk
from connect import connection
from ttkthemes import ThemedStyle
from tkinter import messagebox

cart = []


def auth_user():
    root = tk.Tk()
    root.title("Вход администратора")
    root.geometry("400x300")

    style = ThemedStyle(root)
    style.theme_use("arc")

    def check_user(main_window):
        email = admin_username_entry.get()
        password = admin_password_entry.get()

        if not email or not password:
            status_label.config(text="Статус: Пустое поле", foreground="red")
            return

        with connection.cursor() as cursor:
            query = f"SELECT * FROM customers WHERE email = '{email}' AND password = '{password}';"
            cursor.execute(query)
            result = cursor.fetchone()
            if result:
                messagebox.showinfo('Информация', 'Вход успешен')
                user_id = result[0]

                def update_cart():
                    cart_treeview.delete(*cart_treeview.get_children())
                    for item in cart:
                        cart_treeview.insert("", tk.END, values=item)

                def clear_cart():
                    cart.clear()
                    update_cart()

                def save_cart_to_database():
                    if cart:
                        with connection.cursor() as cursor:
                            for item in cart:
                                product_id = item[0]
                                query = f"INSERT INTO Orders (cust_id, prod_id) VALUES ({user_id}, {product_id});"
                                cursor.execute(query)
                            connection.commit()
                            messagebox.showinfo('Информация', 'Заказ создан ;).')
                            clear_cart()
                    else:
                        messagebox.showwarning('Предупреждение', 'Корзина пуста. Добавьте товары в корзину.')

                def remove_from_cart():
                    selected_item = cart_treeview.selection()
                    if selected_item:
                        item_values = cart_treeview.item(selected_item, "values")
                        product_id = item_values[0]
                        for item in cart:
                            if item[0] == product_id:
                                cart.remove(item)
                                update_cart()  # Обновление корзины после удаления товара
                                break
                    else:
                        messagebox.showwarning('Предупреждение', 'Выберите товар для удаления из корзины.')

                root = tk.Tk()
                root.title("Продукты")
                root.geometry("1250x400")

                main_frame = ttk.Frame(root)
                main_frame.pack(fill=tk.BOTH, expand=True)

                requests_treeview = ttk.Treeview(main_frame)
                requests_treeview["columns"] = ("product_id", "name", "price", "quantity")

                requests_treeview.column("#0", width=0, stretch=tk.NO)
                requests_treeview.column("product_id", anchor=tk.CENTER, width=100)
                requests_treeview.column("name", anchor=tk.CENTER, width=100)
                requests_treeview.column("price", anchor=tk.CENTER, width=100)
                requests_treeview.column("quantity", anchor=tk.CENTER, width=200)

                requests_treeview.heading("#0", text="")
                requests_treeview.heading("product_id", text="Артикул")
                requests_treeview.heading("name", text="Название товара")
                requests_treeview.heading("price", text="Цена")
                requests_treeview.heading("quantity", text="Количество на складе")

                with connection.cursor() as cursor:
                    query = f"SELECT * FROM products"
                    cursor.execute(query)
                    requests = cursor.fetchall()

                    for request in requests:
                        requests_treeview.insert("", tk.END, values=request)
                    requests_treeview.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

                cart_frame = ttk.Frame(main_frame)
                cart_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

                cart_label = ttk.Label(cart_frame, text="Корзина", font="Helvetica 12 bold")
                cart_label.pack()

                cart_treeview = ttk.Treeview(cart_frame)
                cart_treeview["columns"] = ("product_id", "name", "price", "quantity")

                cart_treeview.column("#0", width=0, stretch=tk.NO)
                cart_treeview.column("product_id", anchor=tk.CENTER, width=100)
                cart_treeview.column("name", anchor=tk.CENTER, width=100)
                cart_treeview.column("price", anchor=tk.CENTER, width=100)
                cart_treeview.column("quantity", anchor=tk.CENTER, width=200)

                cart_treeview.heading("#0", text="")
                cart_treeview.heading("product_id", text="Артикул")
                cart_treeview.heading("name", text="Название товара")
                cart_treeview.heading("price", text="Цена")
                cart_treeview.heading("quantity", text="Количество на складе")

                cart_treeview.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, expand=True)

                def add_to_cart():
                    selected_item = requests_treeview.selection()
                    if selected_item:
                        item_values = requests_treeview.item(selected_item, "values")
                        product_id = item_values[0]
                        name = item_values[1]
                        price = item_values[2]
                        quantity = item_values[3]
                        cart.append((product_id, name, price, quantity))
                        update_cart()
                    else:
                        messagebox.showwarning('Предупреждение', 'Выберите товар для добавления в корзину.')

                add_to_cart_button = ttk.Button(main_frame, text="Добавить товар в корзину", command=add_to_cart)
                add_to_cart_button.pack(side=tk.BOTTOM, padx=10, pady=10)

                remove_from_cart_button = ttk.Button(main_frame, text="Удалить товар из корзины",
                                                     command=remove_from_cart)
                remove_from_cart_button.pack(side=tk.BOTTOM, padx=10, pady=10)

                save_to_database_button = ttk.Button(main_frame, text="Сделать заказ",
                                                     command=save_cart_to_database)
                save_to_database_button.pack(side=tk.BOTTOM, padx=10, pady=10)

                main_window.withdraw()
            else:
                messagebox.showerror('Информация', 'Неправильные данные')

    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    admin_username_label = ttk.Label(main_frame, text="Email")
    admin_username_label.pack(pady=10)

    admin_username_entry = ttk.Entry(main_frame)
    admin_username_entry.pack()

    admin_password_label = ttk.Label(main_frame, text="Пароль")
    admin_password_label.pack(pady=10)

    admin_password_entry = ttk.Entry(main_frame, show="*")
    admin_password_entry.pack()

    login_button = ttk.Button(main_frame, text="Войти", command=lambda: check_user(root))
    login_button.pack(pady=10)

    status_label = ttk.Label(main_frame, text="Статус:")
    status_label.pack(pady=10)

    root.mainloop()

