import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env')
if os.path.exists(env_path):
    load_dotenv(env_path)
else:
    load_dotenv()

url: str = os.environ.get("SUPABASE_URL", "")
key: str = os.environ.get("SUPABASE_KEY", "")

# Initialize Supabase client
supabase: Client = create_client(url, key) if url and key else None

def init_db():
    """
    In Supabase, tables should be created via the SQL Editor in the dashboard.
    This function check if connection is active.
    """
    if not supabase:
        print("Supabase client not initialized. Check your environment variables.")
    else:
        print("Connected to Supabase.")

def save_cv(cv_data):
    try:
        cv_id = cv_data.get('id')
        
        # Main CV data
        cv_payload = {
            "title": cv_data.get('title'),
            "template": cv_data.get('template'),
            "full_name": cv_data.get('full_name'),
            "email": cv_data.get('email'),
            "phone": cv_data.get('phone'),
            "address": cv_data.get('address'),
            "linkedin": cv_data.get('linkedin'),
            "summary": cv_data.get('summary')
        }

        if cv_id:
            # Update existing
            supabase.table("cvs").update(cv_payload).eq("id", cv_id).execute()
            # Clear nested data
            supabase.table("experience").delete().eq("cv_id", cv_id).execute()
            supabase.table("education").delete().eq("cv_id", cv_id).execute()
            supabase.table("skills").delete().eq("cv_id", cv_id).execute()
            supabase.table("projects").delete().eq("cv_id", cv_id).execute()
        else:
            # Insert new
            response = supabase.table("cvs").insert(cv_payload).execute()
            cv_id = response.data[0]['id']

        # Insert Experience
        exp_data = []
        for exp in cv_data.get('experience', []):
            exp_data.append({
                "cv_id": cv_id,
                "job_title": exp.get('job_title'),
                "company": exp.get('company'),
                "start_date": exp.get('start_date'),
                "end_date": exp.get('end_date'),
                "description": exp.get('description')
            })
        if exp_data:
            supabase.table("experience").insert(exp_data).execute()

        # Insert Education
        edu_data = []
        for edu in cv_data.get('education', []):
            edu_data.append({
                "cv_id": cv_id,
                "degree": edu.get('degree'),
                "institution": edu.get('institution'),
                "year": edu.get('year')
            })
        if edu_data:
            supabase.table("education").insert(edu_data).execute()

        # Insert Skills
        skills_raw = cv_data.get('skills', [])
        if isinstance(skills_raw, str):
            skills_raw = [s.strip() for s in skills_raw.split(',') if s.strip()]
        
        skill_data = [{"cv_id": cv_id, "skill_name": s} for s in skills_raw]
        if skill_data:
            supabase.table("skills").insert(skill_data).execute()

        # Insert Projects
        proj_data = []
        for proj in cv_data.get('projects', []):
            proj_data.append({
                "cv_id": cv_id,
                "name": proj.get('name'),
                "link": proj.get('link'),
                "description": proj.get('description')
            })
        if proj_data:
            supabase.table("projects").insert(proj_data).execute()

        return cv_id
    except Exception as e:
        print(f"Supabase Error: {e}")
        return None

def get_all_cvs():
    try:
        response = supabase.table("cvs").select("id, title, full_name").order("created_at", desc=True).execute()
        return response.data
    except Exception as e:
        print(f"Supabase Error: {e}")
        return []

def get_cv(cv_id):
    try:
        # Get main info
        cv_response = supabase.table("cvs").select("*").eq("id", cv_id).single().execute()
        cv = cv_response.data
        
        if not cv:
            return None

        # Get nested data
        exp_response = supabase.table("experience").select("*").eq("cv_id", cv_id).execute()
        cv['experience'] = exp_response.data

        edu_response = supabase.table("education").select("*").eq("cv_id", cv_id).execute()
        cv['education'] = edu_response.data

        skills_response = supabase.table("skills").select("skill_name").eq("cv_id", cv_id).execute()
        cv['skills'] = [s['skill_name'] for s in skills_response.data]

        proj_response = supabase.table("projects").select("*").eq("cv_id", cv_id).execute()
        cv['projects'] = proj_response.data

        return cv
    except Exception as e:
        print(f"Supabase Error: {e}")
        return None

def delete_cv(cv_id):
    try:
        # Foreign key constraints in Supabase (ON DELETE CASCADE) should handle child tables
        supabase.table("cvs").delete().eq("id", cv_id).execute()
        return True
    except Exception as e:
        print(f"Supabase Error: {e}")
        return False