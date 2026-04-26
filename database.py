import sqlite3
import os

DB_PATH = "cv_data.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS cvs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                template TEXT DEFAULT 'Classic',
                full_name TEXT,
                email TEXT,
                phone TEXT,
                address TEXT,
                linkedin TEXT,
                summary TEXT
            )
        ''')
        # Migration: Add template column if it doesn't exist
        cursor.execute("PRAGMA table_info(cvs)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'template' not in columns:
            cursor.execute("ALTER TABLE cvs ADD COLUMN template TEXT DEFAULT 'Classic'")
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS experience (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cv_id INTEGER,
                job_title TEXT,
                company TEXT,
                start_date TEXT,
                end_date TEXT,
                description TEXT,
                FOREIGN KEY(cv_id) REFERENCES cvs(id) ON DELETE CASCADE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS education (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cv_id INTEGER,
                degree TEXT,
                institution TEXT,
                year TEXT,
                FOREIGN KEY(cv_id) REFERENCES cvs(id) ON DELETE CASCADE
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS skills (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                cv_id INTEGER,
                skill_name TEXT,
                FOREIGN KEY(cv_id) REFERENCES cvs(id) ON DELETE CASCADE
            )
        ''')
        cursor.execute('PRAGMA foreign_keys = ON;')
        conn.commit()

def save_cv(cv_data):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        
        # Insert or update
        cv_id = cv_data.get('id')
        if cv_id:
            cursor.execute('''
                UPDATE cvs SET title=?, template=?, full_name=?, email=?, phone=?, address=?, linkedin=?, summary=?
                WHERE id=?
            ''', (
                cv_data.get('title', 'Untitled'), cv_data.get('template', 'Classic'), cv_data.get('full_name', ''), cv_data.get('email', ''),
                cv_data.get('phone', ''), cv_data.get('address', ''), cv_data.get('linkedin', ''),
                cv_data.get('summary', ''), cv_id
            ))
            cursor.execute('DELETE FROM experience WHERE cv_id=?', (cv_id,))
            cursor.execute('DELETE FROM education WHERE cv_id=?', (cv_id,))
            cursor.execute('DELETE FROM skills WHERE cv_id=?', (cv_id,))
        else:
            cursor.execute('''
                INSERT INTO cvs (title, template, full_name, email, phone, address, linkedin, summary)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                cv_data.get('title', 'Untitled'), cv_data.get('template', 'Classic'), cv_data.get('full_name', ''), cv_data.get('email', ''),
                cv_data.get('phone', ''), cv_data.get('address', ''), cv_data.get('linkedin', ''),
                cv_data.get('summary', '')
            ))
            cv_id = cursor.lastrowid
            
        for exp in cv_data.get('experience', []):
            if exp.get('job_title') or exp.get('company'):
                cursor.execute('''
                    INSERT INTO experience (cv_id, job_title, company, start_date, end_date, description)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (cv_id, exp.get('job_title', ''), exp.get('company', ''), exp.get('start_date', ''), exp.get('end_date', ''), exp.get('description', '')))
                
        for edu in cv_data.get('education', []):
            if edu.get('degree') or edu.get('institution'):
                cursor.execute('''
                    INSERT INTO education (cv_id, degree, institution, year)
                    VALUES (?, ?, ?, ?)
                ''', (cv_id, edu.get('degree', ''), edu.get('institution', ''), edu.get('year', '')))
                
        for skill in cv_data.get('skills', []):
            if skill.strip():
                cursor.execute('INSERT INTO skills (cv_id, skill_name) VALUES (?, ?)', (cv_id, skill.strip()))
                
        conn.commit()
        return cv_id

def get_all_cvs():
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, full_name FROM cvs ORDER BY id DESC')
        return [dict(row) for row in cursor.fetchall()]

def get_cv(cv_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM cvs WHERE id = ?', (cv_id,))
        row = cursor.fetchone()
        if not row: return None
        cv = dict(row)
        
        cursor.execute('SELECT * FROM experience WHERE cv_id = ?', (cv_id,))
        cv['experience'] = [dict(r) for r in cursor.fetchall()]
        
        cursor.execute('SELECT * FROM education WHERE cv_id = ?', (cv_id,))
        cv['education'] = [dict(r) for r in cursor.fetchall()]
        
        cursor.execute('SELECT skill_name FROM skills WHERE cv_id = ?', (cv_id,))
        cv['skills'] = [r['skill_name'] for r in cursor.fetchall()]
        
        return cv

def delete_cv(cv_id):
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys = ON;')
        cursor.execute('DELETE FROM cvs WHERE id = ?', (cv_id,))
        conn.commit()