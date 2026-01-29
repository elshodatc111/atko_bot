import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_path="atko_crm.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY, full_name TEXT, username TEXT, phone TEXT,
            join_date TEXT, send_time TEXT, current_lesson INTEGER DEFAULT 0,
            last_sent_date TEXT, sent_start_log INTEGER DEFAULT 0, sent_phone_log INTEGER DEFAULT 0
        )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS lessons (
            lesson_num INTEGER PRIMARY KEY, message_id INTEGER, title TEXT
        )''')
        self.conn.commit()

    def add_user(self, user_id, full_name, username):
        date = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("INSERT OR IGNORE INTO users (user_id, full_name, username, join_date) VALUES (?,?,?,?)", 
                           (user_id, full_name, username, date))
        self.conn.commit()

    def update_phone(self, user_id, phone):
        self.cursor.execute("UPDATE users SET phone = ? WHERE user_id = ?", (phone, user_id))
        self.conn.commit()

    def set_user_time(self, user_id, time):
        self.cursor.execute("UPDATE users SET send_time = ? WHERE user_id = ?", (time, user_id))
        self.conn.commit()

    def add_lesson(self, lesson_num, msg_id, title):
        self.cursor.execute("INSERT OR REPLACE INTO lessons VALUES (?,?,?)", (lesson_num, msg_id, title))
        self.conn.commit()

    def get_lesson_msg_id(self, lesson_num):
        self.cursor.execute("SELECT message_id FROM lessons WHERE lesson_num = ?", (lesson_num,))
        res = self.cursor.fetchone()
        return res[0] if res else None

    def update_lesson_progress(self, user_id, lesson_num):
        today = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("UPDATE users SET current_lesson = ?, last_sent_date = ? WHERE user_id = ?", 
                           (lesson_num, today, user_id))
        self.conn.commit()

    def get_users_for_lesson(self, time):
        today = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute("SELECT user_id, current_lesson FROM users WHERE send_time = ? AND (last_sent_date != ? OR last_sent_date IS NULL) AND phone IS NOT NULL", (time, today))
        return self.cursor.fetchall()

    def get_stats(self):
        total = self.cursor.execute("SELECT COUNT(*) FROM users").fetchone()[0]
        with_phone = self.cursor.execute("SELECT COUNT(*) FROM users WHERE phone IS NOT NULL").fetchone()[0]
        return total, with_phone, total - with_phone

    def get_audience(self, target):
        if target == "all": return self.cursor.execute("SELECT user_id FROM users").fetchall()
        if target == "no_phone": return self.cursor.execute("SELECT user_id FROM users WHERE phone IS NULL").fetchall()
        return self.cursor.execute("SELECT user_id FROM users WHERE phone IS NOT NULL").fetchall()
    
    def get_user_info(self, user_id):
        # send_time ustunini ham qo'shdik
        self.cursor.execute("SELECT phone, current_lesson, send_time FROM users WHERE user_id = ?", (user_id,))
        return self.cursor.fetchone()

    def is_start_logged(self, uid): return self.cursor.execute("SELECT sent_start_log FROM users WHERE user_id=?", (uid,)).fetchone()[0]
    def set_start_logged(self, uid): self.cursor.execute("UPDATE users SET sent_start_log=1 WHERE user_id=?", (uid,)); self.conn.commit()
    def is_phone_logged(self, uid): return self.cursor.execute("SELECT sent_phone_log FROM users WHERE user_id=?", (uid,)).fetchone()[0]
    def set_phone_logged(self, uid): self.cursor.execute("UPDATE users SET sent_phone_log=1 WHERE user_id=?", (uid,)); self.conn.commit()