import sqlite3
import os
import json

DB_PATH = os.path.join(os.path.dirname(__file__), 'resumes.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cursor = conn.cursor()
    
    # Main CVS table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cvs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        template TEXT,
        full_name TEXT,
        email TEXT,
        phone TEXT,
        address TEXT,
        linkedin TEXT,
        summary TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    # Experience table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS experience (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cv_id INTEGER,
        job_title TEXT,
        company TEXT,
        start_date TEXT,
        end_date TEXT,
        description TEXT,
        FOREIGN KEY (cv_id) REFERENCES cvs (id) ON DELETE CASCADE
    )
    ''')
    
    # Education table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS education (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cv_id INTEGER,
        degree TEXT,
        institution TEXT,
        year TEXT,
        FOREIGN KEY (cv_id) REFERENCES cvs (id) ON DELETE CASCADE
    )
    ''')
    
    # Skills table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS skills (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cv_id INTEGER,
        skill_name TEXT,
        FOREIGN KEY (cv_id) REFERENCES cvs (id) ON DELETE CASCADE
    )
    ''')
    
    conn.commit()
    conn.close()

def save_cv(cv_data):
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cv_id = cv_data.get('id')
        
        if cv_id:
            # Update existing
            cursor.execute('''
            UPDATE cvs SET 
                title = ?, template = ?, full_name = ?, email = ?, 
                phone = ?, address = ?, linkedin = ?, summary = ?
            WHERE id = ?
            ''', (
                cv_data.get('title'), cv_data.get('template'), cv_data.get('full_name'),
                cv_data.get('email'), cv_data.get('phone'), cv_data.get('address'),
                cv_data.get('linkedin'), cv_data.get('summary'), cv_id
            ))
            
            # Clear old nested data
            cursor.execute('DELETE FROM experience WHERE cv_id = ?', (cv_id,))
            cursor.execute('DELETE FROM education WHERE cv_id = ?', (cv_id,))
            cursor.execute('DELETE FROM skills WHERE cv_id = ?', (cv_id,))
        else:
            # Insert new
            cursor.execute('''
            INSERT INTO cvs (title, template, full_name, email, phone, address, linkedin, summary)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                cv_data.get('title'), cv_data.get('template'), cv_data.get('full_name'),
                cv_data.get('email'), cv_data.get('phone'), cv_data.get('address'),
                cv_data.get('linkedin'), cv_data.get('summary')
            ))
            cv_id = cursor.lastrowid
            
        # Insert Experience
        for exp in cv_data.get('experience', []):
            cursor.execute('''
            INSERT INTO experience (cv_id, job_title, company, start_date, end_date, description)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (cv_id, exp.get('job_title'), exp.get('company'), exp.get('start_date'), exp.get('end_date'), exp.get('description')))
            
        # Insert Education
        for edu in cv_data.get('education', []):
            cursor.execute('''
            INSERT INTO education (cv_id, degree, institution, year)
            VALUES (?, ?, ?, ?)
            ''', (cv_id, edu.get('degree'), edu.get('institution'), edu.get('year')))
            
        # Insert Skills
        skills = cv_data.get('skills', [])
        if isinstance(skills, str):
            skills = [s.strip() for s in skills.split(',') if s.strip()]
        for skill in skills:
            cursor.execute('INSERT INTO skills (cv_id, skill_name) VALUES (?, ?)', (cv_id, skill))
            
        conn.commit()
        conn.close()
        return cv_id
    except Exception as e:
        print(f"Database Error: {e}")
        return None

def get_all_cvs():
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT id, title, full_name FROM cvs ORDER BY created_at DESC')
        rows = cursor.fetchall()
        cvs = [dict(row) for row in rows]
        conn.close()
        return cvs
    except Exception as e:
        print(f"Database Error: {e}")
        return []

def get_cv(cv_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Main info
        cursor.execute('SELECT * FROM cvs WHERE id = ?', (cv_id,))
        row = cursor.fetchone()
        if not row:
            conn.close()
            return None
        
        cv = dict(row)
        
        # Experience
        cursor.execute('SELECT * FROM experience WHERE cv_id = ?', (cv_id,))
        cv['experience'] = [dict(r) for r in cursor.fetchall()]
        
        # Education
        cursor.execute('SELECT * FROM education WHERE cv_id = ?', (cv_id,))
        cv['education'] = [dict(r) for r in cursor.fetchall()]
        
        # Skills
        cursor.execute('SELECT skill_name FROM skills WHERE cv_id = ?', (cv_id,))
        cv['skills'] = [r['skill_name'] for r in cursor.fetchall()]
        
        conn.close()
        return cv
    except Exception as e:
        print(f"Database Error: {e}")
        return None

def delete_cv(cv_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('PRAGMA foreign_keys = ON') # Ensure cascade works
        cursor.execute('DELETE FROM cvs WHERE id = ?', (cv_id,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Database Error: {e}")
        return False