# Database utility for the app using SQLite
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'auto_repair.db')


class Database:
    def delete_obdii_record(self, record_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM obdii WHERE id = ?', (record_id,))
        self.conn.commit()
    def delete_appointment(self, appointment_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM appointments WHERE id = ?', (appointment_id,))
        self.conn.commit()
    def delete_billing(self, billing_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM billing WHERE id = ?', (billing_id,))
        self.conn.commit()
    def delete_inventory_item(self, item_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM inventory WHERE id = ?', (item_id,))
        self.conn.commit()
    def delete_customer(self, customer_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
        self.conn.commit()
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                surname TEXT NOT NULL,
                plate TEXT NOT NULL,
                chassis TEXT NOT NULL
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT,
                code TEXT,
                quantity INTEGER,
                price REAL,
                supplier TEXT,
                location TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS obdii (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                dtc TEXT NOT NULL,
                description TEXT,
                fix TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS billing (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                total REAL,
                notes TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                service TEXT,
                status TEXT,
                notes TEXT
            )
        ''')
        self.conn.commit()

    def add_billing(self, customer_name, date, description, total, notes):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO billing (customer_name, date, description, total, notes)
            VALUES (?, ?, ?, ?, ?)
        ''', (customer_name, date, description, total, notes))
        self.conn.commit()

    def get_billing(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, customer_name, date, description, total, notes FROM billing')
        return cursor.fetchall()

    def add_appointment(self, customer_name, date, time, service, status, notes):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO appointments (customer_name, date, time, service, status, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (customer_name, date, time, service, status, notes))
        self.conn.commit()

    def get_appointments(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, customer_name, date, time, service, status, notes FROM appointments')
        return cursor.fetchall()

    # Duplicate create_tables removed. Only the correct, complete method remains above.
    def add_obdii_record(self, dtc, description, fix):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO obdii (dtc, description, fix)
            VALUES (?, ?, ?)
        ''', (dtc, description, fix))
        self.conn.commit()

    def get_obdii_records(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, dtc, description, fix FROM obdii')
        return cursor.fetchall()
    def add_inventory_item(self, name, category, code, quantity, price, supplier, location):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO inventory (name, category, code, quantity, price, supplier, location)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (name, category, code, quantity, price, supplier, location))
        self.conn.commit()

    def get_inventory(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, category, code, quantity, price, supplier, location FROM inventory')
        return cursor.fetchall()

    def add_customer(self, name, surname, plate, chassis):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO customers (name, surname, plate, chassis)
            VALUES (?, ?, ?, ?)
        ''', (name, surname, plate, chassis))
        self.conn.commit()

    def get_customers(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id, name, surname, plate, chassis FROM customers')
        return cursor.fetchall()

    def close(self):
        self.conn.close()
