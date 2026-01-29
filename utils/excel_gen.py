import sqlite3
import pandas as pd
import os
from datetime import datetime

def generate_excel_report(db_path="atko_crm.db"):
    if not os.path.exists("reports"):
        os.makedirs("reports")

    today_date = datetime.now().strftime("%Y-%m-%d")
    file_path = f"reports/atko_report_{today_date}.xlsx"

    try:
        conn = sqlite3.connect(db_path)
        query = "SELECT * FROM users"
        df = pd.read_sql_query(query, conn)

        # Ustunlar soni bazadagi bilan mosligini tekshiring (10 ta ustun)
        df.columns = [
            'User ID', 'Ism-sharif', 'Username', 'Telefon', 
            'Start sanasi', 'Dars vaqti', 'Oxirgi dars raqami', 
            'Oxirgi yuborilgan sana', 'Start Log', 'Phone Log'
        ]

        df.to_excel(file_path, index=False, engine='openpyxl')
        conn.close()
        return file_path
    except Exception as e:
        print(f"Excel yaratishda xato: {e}")
        return None