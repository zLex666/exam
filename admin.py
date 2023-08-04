import tkinter as tk
from tkinter import ttk
from connect import connection
from tkinter import messagebox

def admin():
    win_admin = tk.Tk()
    win_admin.title("Вход администратора")
    win_admin.geometry("400x300")

    def check_admin():
        email = admin_username_entry.get()
        password = admin_password_entry.get()

        if not email or not password:
            status_label.config(text="Статус: Пустое поле", foreground="red")
            return

        with connection.cursor() as cursor:
            query = f"SELECT * FROM administrators WHERE email = '{email}' AND password = '{password}';"
            cursor.execute(query)
            result = cursor.fetchone()

            if result:
                def choose():
                    win_admin.withdraw()
                    def check_products():
                        win_adm.withdraw()
                        prod_manager = tk.Toplevel(win_adm)
                        prod_manager.title("Заявки")
                        prod_manager.geometry("700x300")

                        manager_treeview = ttk.Treeview(prod_manager)
                        manager_treeview["columns"] = ("product_id", "name", "price", "quantity")

                        manager_treeview.column("#0", width=0, stretch=tk.NO)
                        manager_treeview.column("product_id", anchor=tk.CENTER, width=100)
                        manager_treeview.column("name", anchor=tk.CENTER, width=100)
                        manager_treeview.column("price", anchor=tk.CENTER, width=100)
                        manager_treeview.column("quantity", anchor=tk.CENTER, width=200)

                        manager_treeview.heading("#0", text="")
                        manager_treeview.heading("product_id", text="Артикул")
                        manager_treeview.heading("name", text="Название товара")
                        manager_treeview.heading("price", text="Цена")
                        manager_treeview.heading("quantity", text="Количество на складе")

                        with connection.cursor() as cursor:
                            query = "SELECT * FROM Products"
                            cursor.execute(query)
                            products = cursor.fetchall()

                            for product in products:
                                manager_treeview.insert("", tk.END, values=product)

                        manager_treeview.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

                        def back():
                            prod_manager.withdraw()
                            win_adm.deiconify()

                        back_but = tk.Button(prod_manager, text="Назад", width=10, height=5, command=back)
                        back_but.pack(pady=10)

                        def edit_product():
                            selected_item = manager_treeview.focus()
                            values = manager_treeview.item(selected_item)["values"]
                            if not values:
                                messagebox.showinfo("Ошибка", "Пожалуйста, выберите продукт для редактирования.")
                                return

                            # Создаем новое окно для редактирования выбранного продукта
                            edit_window = tk.Toplevel(prod_manager)
                            edit_window.title("Редактирование продукта")
                            edit_window.geometry("400x200")

                            name_label = tk.Label(edit_window, text="Название:")
                            name_label.pack()
                            name_entry = ttk.Entry(edit_window)
                            name_entry.insert(0, values[1])
                            name_entry.pack()

                            price_label = tk.Label(edit_window, text="Цена:")
                            price_label.pack()
                            price_entry = ttk.Entry(edit_window)
                            price_entry.insert(0, values[2])
                            price_entry.pack()

                            quantity_label = tk.Label(edit_window, text="Количество на складе:")
                            quantity_label.pack()
                            quantity_entry = ttk.Entry(edit_window)
                            quantity_entry.insert(0, values[3])
                            quantity_entry.pack()

                            def save_changes():
                                new_name = name_entry.get()
                                new_price = price_entry.get()
                                new_quantity = quantity_entry.get()

                                selected_item = manager_treeview.focus()
                                manager_treeview.set(selected_item, column="name", value=new_name)
                                manager_treeview.set(selected_item, column="price", value=new_price)
                                manager_treeview.set(selected_item, column="quantity", value=new_quantity)

                                with connection.cursor() as cursor:
                                    query = f"UPDATE Products SET name = '{new_name}', price = {new_price}, quantity = {new_quantity} WHERE product_id = {values[0]}"
                                    cursor.execute(query)
                                    connection.commit()
                                    messagebox.showinfo("Успех", "Продукт успешно обновлен.")
                                    edit_window.destroy()

                            save_button = tk.Button(edit_window, text="Сохранить", command=save_changes)
                            save_button.pack(pady=10)

                        edit_button = tk.Button(prod_manager, text="Редактировать", width=10, height=5,
                                                command=edit_product)
                        edit_button.pack(pady=10)

                    def edit():
                        def edit_selected():
                            selected_item = orders_treeview.focus()
                            values = orders_treeview.item(selected_item)["values"]
                            if not values:
                                messagebox.showinfo("Ошибка", "Пожалуйста, выберите заказ для редактирования.")
                                return

                            edit_window = tk.Toplevel(orders_window)
                            edit_window.title("Редактирование заказа")
                            edit_window.geometry("400x200")

                            customer_label = tk.Label(edit_window, text="Имя клиента:")
                            customer_label.pack()
                            customer_combobox = ttk.Combobox(edit_window, values=get_customer_names())
                            customer_combobox.set(values[0])
                            customer_combobox.pack()

                            product_names = get_product_names()

                            product_label = tk.Label(edit_window, text="Название товара:")
                            product_label.pack()
                            product_combobox = ttk.Combobox(edit_window, values=product_names)
                            product_combobox.set(values[1])
                            product_combobox.pack()

                            status_label = tk.Label(edit_window, text="Статус:")
                            status_label.pack()
                            status_combobox = ttk.Combobox(edit_window, values=get_status_names())
                            status_combobox.set(values[3])
                            status_combobox.pack()

                            def save_changes():
                                new_customer_name = customer_combobox.get()
                                new_product_name = product_combobox.get()
                                new_status_name = status_combobox.get()

                                with connection.cursor() as cursor:
                                    query = "UPDATE orders " \
                                            "SET cust_id = (SELECT customer_id FROM customers WHERE name = %s), " \
                                            "prod_id = (SELECT product_id FROM products WHERE name = %s), " \
                                            "status_id = (SELECT status_id FROM statuses WHERE name = %s) " \
                                            "WHERE order_date = %s"
                                    cursor.execute(query,
                                                   (new_customer_name, new_product_name, new_status_name, values[2]))
                                    connection.commit()

                                orders_treeview.item(selected_item, values=(
                                    new_customer_name, new_product_name, values[2], new_status_name))
                                messagebox.showinfo("Успех", "Изменения сохранены.")
                                edit_window.destroy()

                            save_button = tk.Button(edit_window, text="Сохранить", command=save_changes)
                            save_button.pack(pady=10)

                        win_adm.withdraw()
                        orders_window = tk.Toplevel(win_adm)
                        orders_window.title("Заказы")
                        orders_window.geometry("1250x400")

                        orders_treeview = ttk.Treeview(orders_window)
                        orders_treeview["columns"] = ("customer_name", "product_name", "order_date", "status_name")

                        orders_treeview.column("#0", width=0, stretch=tk.NO)
                        orders_treeview.column("customer_name", anchor=tk.CENTER, width=200)
                        orders_treeview.column("product_name", anchor=tk.CENTER, width=200)
                        orders_treeview.column("order_date", anchor=tk.CENTER, width=200)
                        orders_treeview.column("status_name", anchor=tk.CENTER, width=200)

                        orders_treeview.heading("#0", text="")
                        orders_treeview.heading("customer_name", text="Имя клиента")
                        orders_treeview.heading("product_name", text="Название товара")
                        orders_treeview.heading("order_date", text="Дата заказа")
                        orders_treeview.heading("status_name", text="Статус")

                        with connection.cursor() as cursor:
                            query = "SELECT customers.name, products.name, orders.order_date, statuses.name " \
                                    "FROM orders, customers, products, statuses " \
                                    "WHERE orders.cust_id = customers.customer_id " \
                                    "AND orders.prod_id = products.product_id " \
                                    "AND orders.status_id = statuses.status_id"
                            cursor.execute(query)
                            orders = cursor.fetchall()

                        for order in orders:
                            orders_treeview.insert("", tk.END, values=order)

                        def back():
                            orders_window.withdraw()
                            win_adm.deiconify()

                        orders_treeview.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)
                        edit_button = tk.Button(orders_window, text="Редактировать", width=10, height=5,
                                                command=edit_selected)
                        edit_button.pack(pady=10)
                        back_but = tk.Button(orders_window, text="Назад", width=10, height=5, command=back)
                        back_but.pack(pady=10)

                        orders_window.mainloop()

                    def get_customer_names():
                        with connection.cursor() as cursor:
                            cursor.execute("SELECT name FROM Customers")
                            customers = cursor.fetchall()
                            customer_names = [customer[0] for customer in customers]
                        return customer_names

                    def get_product_names():
                        with connection.cursor() as cursor:
                            cursor.execute("SELECT name FROM Products")
                            products = cursor.fetchall()
                            product_names = [product[0] for product in products]
                        return product_names

                    def get_status_names():
                        with connection.cursor() as cursor:
                            cursor.execute("SELECT name FROM Statuses")
                            statuses = cursor.fetchall()
                            status_names = [status[0] for status in statuses]
                        return status_names

                    win_adm = tk.Toplevel(win_admin)
                    win_adm.title("Вход администратора")
                    win_adm.geometry("400x300")
                    win_adm.resizable(False, False)

                    style = ttk.Style(win_adm)
                    style.theme_use("default")

                    button1 = tk.Button(win_adm, text="Просмотреть товары", width=25, height=5, command=check_products)
                    button1.pack(pady=10)

                    button2 = tk.Button(win_adm, text="Редактировать заказы", width=25, height=5, command=edit)
                    button2.pack(pady=10)

                    win_adm.mainloop()

                choose()

            else:
                messagebox.showerror('Информация', 'Неправильные данные')

    main_frame = ttk.Frame(win_admin)
    main_frame.pack(fill=tk.BOTH, expand=True)

    admin_username_label = ttk.Label(main_frame, text="Email")
    admin_username_label.pack(pady=10)

    admin_username_entry = ttk.Entry(main_frame)
    admin_username_entry.pack()

    admin_password_label = ttk.Label(main_frame, text="Пароль")
    admin_password_label.pack(pady=10)

    admin_password_entry = ttk.Entry(main_frame, show="*")
    admin_password_entry.pack()

    login_button = ttk.Button(main_frame, text="Войти", command=check_admin)
    login_button.pack(pady=10)

    status_label = ttk.Label(main_frame, text="Статус:")
    status_label.pack(pady=10)

    win_admin.mainloop()
