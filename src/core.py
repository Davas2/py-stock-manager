import sqlite3
from datetime import datetime
from typing import List, Optional
from .models import Product, User, Movement

class InventoryManager:
    def __init__(self, db_path: str = 'database/inventory.db'):
        self.db_path = db_path
        self._initialize_db()

    def _initialize_db(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Products table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price REAL NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Users table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL
                )
            ''')
            
            # Movements table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS movements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    product_id INTEGER NOT NULL,
                    quantity INTEGER NOT NULL,
                    unit_price REAL NOT NULL,
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    FOREIGN KEY (product_id) REFERENCES products (id)
                )
            ''')
            conn.commit()

    # Product methods
    def add_product(self, name: str, quantity: int, unit_price: float) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO products (name, quantity, unit_price)
                VALUES (?, ?, ?)
            ''', (name, quantity, unit_price))
            conn.commit()
            return cursor.lastrowid

    def get_product(self, product_id: int) -> Optional[Product]:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
            row = cursor.fetchone()
            return Product(*row) if row else None

    # User methods
    def add_user(self, name: str, email: str) -> int:
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            try:
                cursor.execute('''
                    INSERT INTO users (name, email)
                    VALUES (?, ?)
                ''', (name, email))
                conn.commit()
                return cursor.lastrowid
            except sqlite3.IntegrityError:
                raise ValueError(f"Email {email} already registered")

    # Inventory movement methods
    def withdraw_product(self, user_id: int, product_id: int, quantity: int):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Check stock
            cursor.execute('''
                SELECT quantity, unit_price FROM products 
                WHERE id = ?
            ''', (product_id,))
            result = cursor.fetchone()
            
            if not result:
                raise ValueError("Product not found")
            
            available, unit_price = result
            if available < quantity:
                raise ValueError(f"Insufficient stock. Available: {available}")
            
            # Update stock
            cursor.execute('''
                UPDATE products 
                SET quantity = quantity - ? 
                WHERE id = ?
            ''', (quantity, product_id))
            
            # Record movement
            cursor.execute('''
                INSERT INTO movements (user_id, product_id, quantity, unit_price)
                VALUES (?, ?, ?, ?)
            ''', (user_id, product_id, quantity, unit_price))
            
            conn.commit()

    # Reporting methods
    def generate_monthly_report(self, month: int, year: int) -> str:
        import pandas as pd
        from pathlib import Path
        
        with sqlite3.connect(self.db_path) as conn:
            df = pd.read_sql('''
                SELECT 
                    u.name as user,
                    p.name as product,
                    SUM(m.quantity) as total_quantity,
                    m.unit_price,
                    SUM(m.quantity * m.unit_price) as total_spent,
                    strftime('%d/%m/%Y', m.created_at) as date
                FROM movements m
                JOIN users u ON m.user_id = u.id
                JOIN products p ON m.product_id = p.id
                WHERE strftime('%m', m.created_at) = ? 
                  AND strftime('%Y', m.created_at) = ?
                GROUP BY u.name, p.name, m.unit_price
                ORDER BY total_spent DESC
            ''', conn, params=(f"{month:02d}", str(year)))
            
            if df.empty:
                return "No data found for selected period"
            
            # Create directory if needed
            Path('src/reports').mkdir(exist_ok=True)
            
            # Save report
            report_path = f'src/reports/report_{month}_{year}.xlsx'
            df.to_excel(report_path, index=False)
            return f"Report generated at: {report_path}"
