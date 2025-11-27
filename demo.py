# -*- coding: utf-8 -*-
"""
HỆ THỐNG QUẢN LÝ CỬA HÀNG - DÙNG MySQL THẬT
Tác giả: Bạn + Grok (2025)
"""

import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
from typing import Optional, List, Dict

# ==================== CẤU HÌNH MySQL (bạn sửa lại theo máy mình) ====================
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # đổi thành user của bạn
    'password': '123456',  # đổi thành mật khẩu MySQL của bạn
    'database': 'cua_hang_db',
    'port': 3306,
    'autocommit': True
}


# Tạo database + bảng lần đầu (chạy 1 lần thôi)
def init_database():
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS cua_hang_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        cursor.execute("USE cua_hang_db")

        tables = [
            """CREATE TABLE IF NOT EXISTS categories
            (
                id
                VARCHAR
               (
                10
               ) PRIMARY KEY,
                name VARCHAR
               (
                   100
               ) NOT NULL,
                description TEXT
                )""",
            """CREATE TABLE IF NOT EXISTS suppliers
            (
                id
                VARCHAR
               (
                10
               ) PRIMARY KEY,
                name VARCHAR
               (
                   100
               ),
                address TEXT,
                phone VARCHAR
               (
                   15
               ),
                contact_person VARCHAR
               (
                   100
               ),
                email VARCHAR
               (
                   100
               ),
                note TEXT
                )""",
            """CREATE TABLE IF NOT EXISTS products
            (
                id
                VARCHAR
               (
                10
               ) PRIMARY KEY,
                name VARCHAR
               (
                   200
               ) NOT NULL,
                category_id VARCHAR
               (
                   10
               ),
                supplier_id VARCHAR
               (
                   10
               ),
                cost DECIMAL
               (
                   12,
                   2
               ),
                price DECIMAL
               (
                   12,
                   2
               ),
                stock INT DEFAULT 0,
                status ENUM
               (
                   'Có sẵn',
                   'Hết hàng'
               ) DEFAULT 'Hết hàng',
                FOREIGN KEY
               (
                   category_id
               ) REFERENCES categories
               (
                   id
               ),
                FOREIGN KEY
               (
                   supplier_id
               ) REFERENCES suppliers
               (
                   id
               )
                )""",
            """CREATE TABLE IF NOT EXISTS employees
            (
                id
                VARCHAR
               (
                10
               ) PRIMARY KEY,
                name VARCHAR
               (
                   100
               ),
                address TEXT,
                phone VARCHAR
               (
                   15
               ),
                dob DATE,
                gender ENUM
               (
                   'Nam',
                   'Nữ',
                   'Khác'
               ),
                id_card VARCHAR
               (
                   20
               ),
                title VARCHAR
               (
                   50
               ),
                username VARCHAR
               (
                   50
               ) UNIQUE,
                password VARCHAR
               (
                   255
               ),
                email VARCHAR
               (
                   100
               ),
                is_active BOOLEAN DEFAULT TRUE
                )""",
            """CREATE TABLE IF NOT EXISTS customers
            (
                id
                VARCHAR
               (
                10
               ) PRIMARY KEY,
                name VARCHAR
               (
                   100
               ),
                address TEXT,
                phone VARCHAR
               (
                   15
               ),
                points INT DEFAULT 0
                )""",
            """CREATE TABLE IF NOT EXISTS bills
            (
                id
                VARCHAR
               (
                20
               ) PRIMARY KEY,
                customer_id VARCHAR
               (
                   10
               ),
                employee_id VARCHAR
               (
                   10
               ),
                total DECIMAL
               (
                   12,
                   2
               ),
                discount DECIMAL
               (
                   12,
                   2
               ) DEFAULT 0,
                final_amount DECIMAL
               (
                   12,
                   2
               ),
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY
               (
                   customer_id
               ) REFERENCES customers
               (
                   id
               ),
                FOREIGN KEY
               (
                   employee_id
               ) REFERENCES employees
               (
                   id
               )
                )""",
            """CREATE TABLE IF NOT EXISTS bill_items
            (
                bill_id
                VARCHAR
               (
                20
               ),
                product_id VARCHAR
               (
                   10
               ),
                name VARCHAR
               (
                   200
               ),
                quantity INT,
                unit_price DECIMAL
               (
                   12,
                   2
               ),
                FOREIGN KEY
               (
                   bill_id
               ) REFERENCES bills
               (
                   id
               ),
                FOREIGN KEY
               (
                   product_id
               ) REFERENCES products
               (
                   id
               )
                )"""
        ]
        for table in tables:
            cursor.execute(table)
        print("Khởi tạo CSDL MySQL thành công!")
    except Error as e:
        print(f"Lỗi kết nối MySQL: {e}")
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


# ==================== KẾT NỐI TOÀN CỤC ====================
def get_db():
    return mysql.connector.connect(**DB_CONFIG)


# ==================== CÁC CLASS ENTITY ====================
class Category:
    @staticmethod
    def create(id, name, description=""):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO categories VALUES (%s, %s, %s)", (id, name, description))
        conn.close()

    @staticmethod
    def get(id):
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM categories WHERE id = %s", (id,))
        row = cur.fetchone()
        conn.close()
        return row

    @staticmethod
    def all():
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM categories")
        rows = cur.fetchall()
        conn.close()
        return rows


class Supplier:
    @staticmethod
    def create(id, name, address="", phone="", contact="", email="", note=""):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""INSERT INTO suppliers
                       VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                    (id, name, address, phone, contact, email, note))
        conn.close()

    @staticmethod
    def get(id):
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM suppliers WHERE id=%s", (id,))
        row = cur.fetchone()
        conn.close()
        return row


class Product:
    @staticmethod
    def create(id, name, category_id, cost, price, stock=0, supplier_id=None):
        conn = get_db()
        cur = conn.cursor()
        status = "Có sẵn" if stock > 0 else "Hết hàng"
        cur.execute("""INSERT INTO products (id, name, category_id, supplier_id, cost, price, stock, status)
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (id, name, category_id, supplier_id, cost, price, stock, status))
        conn.close()

    @staticmethod
    def update_stock(product_id, delta):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE products SET stock = stock + %s WHERE id = %s", (delta, product_id))
        cur.execute("UPDATE products SET status = IF(stock>0,'Có sẵn','Hết hàng') WHERE id = %s", (product_id,))
        conn.close()

    @staticmethod
    def get(id):
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM products WHERE id=%s", (id,))
        row = cur.fetchone()
        conn.close()
        return row

    @staticmethod
    def all():
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM products")
        rows = cur.fetchall()
        conn.close()
        return rows


class Employee:
    @staticmethod
    def create(id, name, address, phone, dob, gender, id_card, title, username, password, email):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""INSERT INTO employees
                       VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE)""",
                    (id, name, address, phone, dob, gender, id_card, title, username, password, email))
        conn.close()

    @staticmethod
    def login(username, password):
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM employees WHERE username=%s AND password=%s AND is_active=1", (username, password))
        emp = cur.fetchone()
        conn.close()
        return emp


class Customer:
    @staticmethod
    def get_or_create(id, name="", phone=""):
        conn = get_db()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM customers WHERE id=%s", (id,))
        cus = cur.fetchone()
        if not cus:
            cur.execute("INSERT INTO customers (id, name, phone) VALUES (%s,%s,%s)", (id, name, phone))
            cus = {"id": id, "name": name, "phone": phone, "points": 0}
        conn.close()
        return cus

    @staticmethod
    def add_points(customer_id, amount_spent):
        if amount_spent >= 50000:
            points = amount_spent // 50000
            conn = get_db()
            cur = conn.cursor()
            cur.execute("UPDATE customers SET points = points + %s WHERE id=%s", (points, customer_id))
            conn.close()
            return points
        return 0


class Bill:
    @staticmethod
    def create(customer_id, employee_id, items: List[dict], discount=0):
        conn = get_db()
        cur = conn.cursor()

        total = sum(it["quantity"] * it["unit_price"] for it in items)
        final = total - discount
        bill_id = datetime.now().strftime("HD%Y%m%d%H%M%S")

        cur.execute("""INSERT INTO bills (id, customer_id, employee_id, total, discount, final_amount)
                       VALUES (%s, %s, %s, %s, %s, %s)""",
                    (bill_id, customer_id, employee_id, total, discount, final))

        for it in items:
            cur.execute("""INSERT INTO bill_items
                           VALUES (%s, %s, %s, %s, %s)""",
                        (bill_id, it["product_id"], it["name"], it["quantity"], it["unit_price"]))
            # trừ tồn kho
            Product.update_stock(it["product_id"], -it["quantity"])

        conn.close()
        return bill_id, total, final


# ==================== CHẠY CHƯƠNG TRÌNH ====================
if __name__ == "__main__":
    init_database()

    # Tạo dữ liệu mẫu (chỉ chạy lần đầu)
    try:
        Category.create("DM001", "Nước giải khát")
        Category.create("DM002", "Bánh kẹo")
        Supplier.create("NCC001", "Công ty Coca Cola VN", phone="02838384567", contact="Mr.Long")
        Product.create("SP001", "Coca Cola 330ml", "DM001", 7000, 10000, 200, "NCC001")
        Product.create("SP002", "Pepsi 330ml", "DM001", 7000, 10000, 150, "NCC001")
        Product.create("SP003", "Bánh Oreo", "DM002", 15000, 22000, 80)
        Employee.create("NV001", "Trần Văn Admin", "Hà Nội", "0901234567", "1995-01-01", "Nam",
                        "001095123456", "Quản lý", "admin", "123456", "admin@shop.com")
        print("Tạo dữ liệu mẫu thành công!")
    except:
        pass

    print("\n=== HỆ THỐNG QUẢN LÝ CỬA HÀNG - MySQL ===")
    print("Ví dụ bán hàng nhanh:")

    # Bán hàng thử
    items = [
        {"product_id": "SP001", "name": "Coca Cola 330ml", "quantity": 5, "unit_price": 10000},
        {"product_id": "SP003", "name": "Bánh Oreo", "quantity": 2, "unit_price": 22000}
    ]
    bill_id, total, final = Bill.create("KH001", "NV001", items, discount=10000)

    Customer.get_or_create("KH001", "Nguyễn Văn Khách VIP", "0909123123")
    Customer.add_points("KH001", final)

    print(f"Đã tạo hóa đơn {bill_id} | Tổng: {total:,}đ → Thanh toán: {final:,}đ")
    print("Dữ liệu đã được lưu vào MySQL!")

    print("\nBạn có thể mở phpMyAdmin hoặc MySQL Workbench để xem bảng dữ liệu ngay bây giờ!")