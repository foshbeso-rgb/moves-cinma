# الملف: models.py
import sqlite3

# دالة الاتصال بقاعدة البيانات
def get_db_connection():
    # هذا سيقوم بإنشاء ملف قاعدة البيانات dakhlin_cinema.db في مجلد مشروعك
    conn = sqlite3.connect('dakhlin_cinema.db')
    conn.row_factory = sqlite3.Row
    return conn

# دالة إنشاء الجداول
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # إنشاء جدول التصنيفات
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS categories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE
    )
    ''')

    # إنشاء جدول الأفلام
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        release_year INTEGER,
        category_id INTEGER,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
    ''')
    
    conn.commit()
    conn.close()
    
    

# عند تشغيل هذا الملف لأول مرة، سيتم إنشاء القاعدة والجداول
if __name__ == "__main__":
    init_db()
    print("تم إنشاء قاعدة البيانات والجداول بنجاح في ملف models.py!")