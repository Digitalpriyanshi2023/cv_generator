import database
import os

def test_db():
    print("Initializing DB...")
    database.init_db()
    
    test_cv = {
        'title': 'Test Resume',
        'template': 'Formal',
        'full_name': 'John Doe',
        'email': 'john@example.com',
        'phone': '123456789',
        'address': '123 Main St',
        'linkedin': 'linkedin.com/in/johndoe',
        'summary': 'Test summary',
        'experience': [{'job_title': 'Dev', 'company': 'Tech', 'start_date': '2020', 'end_date': '2021', 'description': 'desc'}],
        'education': [{'degree': 'BS', 'institution': 'Univ', 'year': '2019'}],
        'skills': ['Python', 'SQL']
    }
    
    print("Saving CV...")
    cv_id = database.save_cv(test_cv)
    print(f"Saved CV ID: {cv_id}")
    
    print("Retrieving CV...")
    retrieved = database.get_cv(cv_id)
    print(f"Retrieved Title: {retrieved['title']}")
    
    print("Getting all CVs...")
    all_cvs = database.get_all_cvs()
    print(f"Total CVs: {len(all_cvs)}")

if __name__ == "__main__":
    if os.path.exists("cv_data.db"):
        os.remove("cv_data.db") # Start fresh for test
    test_db()
