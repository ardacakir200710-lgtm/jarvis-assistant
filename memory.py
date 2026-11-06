import sqlite3
from datetime import datetime

class JarvisMemory:
    def __init__(self, db_path="jarvis_memory.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        # Sohbet geçmişi tablosunu oluştur
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS chat_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()

    def save_message(self, role, content):
        # Yeni mesajı veritabanına ekle
        self.cursor.execute(
            "INSERT INTO chat_history (role, content, timestamp) VALUES (?, ?, ?)",
            (role, content, datetime.now())
        )
        self.conn.commit()

    def get_recent_context(self, limit=6):
        # Son N mesajı çek (Bağlamı korumak ve 2048 token sınırını aşmamak için 6 idealdir)
        self.cursor.execute(
            "SELECT role, content FROM chat_history ORDER BY id DESC LIMIT ?", 
            (limit,)
        )
        rows = self.cursor.fetchall()
        
        # Veritabanından gelen veriyi Eskiden -> Yeniye doğru sırala ve Dict listesi yap
        messages = [{"role": row[0], "content": row[1]} for row in reversed(rows)]
        return messages