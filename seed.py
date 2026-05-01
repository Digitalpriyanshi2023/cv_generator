import sys
import os

# Add api directory to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'api'))

import database

demo_cv = {
    "title": "Senior Engineer - Professional Demo",
    "template": "Modern",
    "full_name": "Alex Rivera",
    "email": "alex.rivera@example.com",
    "phone": "+1 (415) 555-0198",
    "address": "San Francisco, CA",
    "linkedin": "linkedin.com/in/alexrivera",
    "summary": "Visionary Senior Software Engineer with 8+ years of experience in designing scalable microservices and leading cross-functional teams. Passionate about cloud-native architecture, performance optimization, and building robust, user-centric applications. Proven track record of delivering high-impact technical solutions.",
    "experience": [
        {
            "job_title": "Lead Staff Engineer",
            "company": "TechNova Solutions",
            "start_date": "Mar 2021",
            "end_date": "Present",
            "description": "Spearheaded the migration of a legacy monolithic application to a microservices architecture using Kubernetes and Go.\nImproved overall system reliability to 99.99% and reduced CI/CD deployment time by 40%.\nManaged a team of 6 engineers."
        },
        {
            "job_title": "Software Engineer II",
            "company": "CloudScape Systems",
            "start_date": "Jun 2018",
            "end_date": "Feb 2021",
            "description": "Developed high-throughput REST APIs using Python and FastAPI, serving over 2M requests daily.\nOptimized PostgreSQL database queries, reducing average API response time from 200ms to 45ms."
        }
    ],
    "education": [
        {
            "degree": "M.S. in Computer Science",
            "institution": "Stanford University",
            "year": "2018"
        },
        {
            "degree": "B.S. in Software Engineering",
            "institution": "UC Berkeley",
            "year": "2016"
        }
    ],
    "skills": "Python, Go, Kubernetes, PostgreSQL, AWS Cloud, System Architecture, Docker, React, Next.js, GraphQL",
    "projects": [
        {
            "name": "Nexus Queue (Open Source)",
            "link": "github.com/arivera/nexus",
            "description": "Created and maintain an open-source distributed task queue in Go. Reached 2k+ stars on GitHub and adopted by 4 enterprise companies."
        },
        {
            "name": "AI Content Optimizer",
            "link": "contentai.io",
            "description": "Built a scalable SaaS application leveraging OpenAI's GPT-4 to optimize marketing copy for SEO, reaching $10k MRR."
        }
    ]
}

if __name__ == "__main__":
    print("Seeding database with professional demo CV...")
    cv_id = database.save_cv(demo_cv)
    if cv_id:
        print(f"Successfully seeded CV! ID: {cv_id}")
    else:
        print("Failed to seed database. Check Supabase connection and schema.")
