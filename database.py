import sqlite3
import os
from typing import Dict

class Database:
    def __init__(self, db_name: str = 'ocr_results.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(db_name)
        self.create_table()
    
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('DROP TABLE IF EXISTS ocr_results')
        cursor.execute('''
            CREATE TABLE ocr_results (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                image_path TEXT NOT NULL,
                extracted_text TEXT NOT NULL,
                detected_language TEXT NOT NULL,
                confidence FLOAT,
                processed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT NOT NULL
            )
        ''')
        self.conn.commit()
    
    def save_result(self, image_path: str, text: str, language: str, confidence: float, status: str) -> int:
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO ocr_results (image_path, extracted_text, detected_language, confidence, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (image_path, text, language, confidence, status))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_result(self, id: int) -> Dict:
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM ocr_results WHERE id = ?', (id,))
        result = cursor.fetchone()
        if result:
            return {
                'id': result[0],
                'image_path': result[1],
                'text': result[2],
                'language': result[3],
                'confidence': result[4],
                'date': result[5],
                'status': result[6]
            }
        return None
    
    def close(self):
        self.conn.close()

# First, delete the existing database if it exists
if os.path.exists('ocr_results.db'):
    os.remove('ocr_results.db')
