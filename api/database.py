import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables for local development
load_dotenv()

URL: str = os.environ.get("SUPABASE_URL", "https://utlexxyqsxgikrdbmnix.supabase.co")
KEY: str = os.environ.get("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV0bGV4eHlxc3hnaWtyZGJtbml4Iiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzcyMDkzMzksImV4cCI6MjA5Mjc4NTMzOX0.fXRkOFCc1di7jcSKBy5S8VUAqofVxM5p2O9iTU9csMY")

# Initialize the Supabase client
supabase: Client = None
if URL and KEY:
    supabase = create_client(URL, KEY)

def init_db():
    """
    In Supabase, you create tables via the Dashboard SQL Editor.
    I will provide the SQL in the sharing guide.
    """
    pass

def save_cv(cv_data):
    if not supabase:
        print("Error: Supabase client not initialized")
        return None

    try:
        # Insert or update main CV entry
        cv_id = cv_data.get('id')
        
        cv_payload = {
            "title": cv_data.get('title', 'Untitled'),
            "template": cv_data.get('template', 'Classic'),
            "full_name": cv_data.get('full_name', ''),
            "email": cv_data.get('email', ''),
            "phone": cv_data.get('phone', ''),
            "address": cv_data.get('address', ''),
            "linkedin": cv_data.get('linkedin', ''),
            "summary": cv_data.get('summary', '')
        }

        if cv_id:
            # Update
            supabase.table('cvs').update(cv_payload).eq('id', cv_id).execute()
            # Clear related tables for refresh (simple way to sync nested data)
            supabase.table('experience').delete().eq('cv_id', cv_id).execute()
            supabase.table('education').delete().eq('cv_id', cv_id).execute()
            supabase.table('skills').delete().eq('cv_id', cv_id).execute()
        else:
            # Insert
            res = supabase.table('cvs').insert(cv_payload).execute()
            if not res.data: return None
            cv_id = res.data[0]['id']

        # Batch Insert Experience
        exp_entries = []
        for exp in cv_data.get('experience', []):
            if exp.get('job_title') or exp.get('company'):
                exp_entries.append({
                    "cv_id": cv_id,
                    "job_title": exp.get('job_title', ''),
                    "company": exp.get('company', ''),
                    "start_date": exp.get('start_date', ''),
                    "end_date": exp.get('end_date', ''),
                    "description": exp.get('description', '')
                })
        if exp_entries:
            supabase.table('experience').insert(exp_entries).execute()

        # Batch Insert Education
        edu_entries = []
        for edu in cv_data.get('education', []):
            if edu.get('degree') or edu.get('institution'):
                edu_entries.append({
                    "cv_id": cv_id,
                    "degree": edu.get('degree', ''),
                    "institution": edu.get('institution', ''),
                    "year": edu.get('year', '')
                })
        if edu_entries:
            supabase.table('education').insert(edu_entries).execute()

        # Batch Insert Skills
        skill_entries = []
        skills_raw = cv_data.get('skills', [])
        # Handle both list and string inputs
        if isinstance(skills_raw, str):
            skills_raw = [s.strip() for s in skills_raw.split(',') if s.strip()]
            
        for skill in skills_raw:
            if str(skill).strip():
                skill_entries.append({"cv_id": cv_id, "skill_name": str(skill).strip()})
        if skill_entries:
            supabase.table('skills').insert(skill_entries).execute()

        return cv_id
    except Exception as e:
        print(f"Database Save Error: {e}")
        return None

def get_all_cvs():
    if not supabase: return []
    try:
        res = supabase.table('cvs').select('id, title, full_name').order('id', desc=True).execute()
        return res.data or []
    except Exception as e:
        print(f"Database Fetch Error: {e}")
        return []

def get_cv(cv_id):
    if not supabase: return None
    
    try:
        # Get main CV
        res = supabase.table('cvs').select('*').eq('id', cv_id).execute()
        if not res.data: return None
        cv = res.data[0]
        
        # Get related data in parallel (conceptually)
        exp = supabase.table('experience').select('*').eq('cv_id', cv_id).execute()
        cv['experience'] = exp.data or []
        
        edu = supabase.table('education').select('*').eq('cv_id', cv_id).execute()
        cv['education'] = edu.data or []
        
        skills = supabase.table('skills').select('skill_name').eq('cv_id', cv_id).execute()
        cv['skills'] = [s['skill_name'] for s in (skills.data or [])]
        
        return cv
    except Exception as e:
        print(f"Database Detail Fetch Error: {e}")
        return None

def delete_cv(cv_id):
    if not supabase: return False
    try:
        supabase.table('cvs').delete().eq('id', cv_id).execute()
        return True
    except Exception as e:
        print(f"Database Delete Error: {e}")
        return False