def get_web_html(cv_data):
    """Generates an ultra-premium, full-page designer HTML resume optimized for PDF export."""
    theme = cv_data.get('template', 'Classic')
    
    themes = {
        "Classic": {
            "primary": "#1e293b", "secondary": "#64748b", "accent": "#f1f5f9",
            "font_main": "'Inter', sans-serif", "font_head": "'Inter', sans-serif",
            "header_bg": "#ffffff", "border_color": "#1e293b", "sidebar_bg": "#f8fafc"
        },
        "Formal": {
            "primary": "#0f172a", "secondary": "#475569", "accent": "#f1f5f9",
            "font_main": "'Inter', sans-serif", "font_head": "'Inter', sans-serif",
            "header_bg": "#f1f5f9", "border_color": "#0f172a", "sidebar_bg": "#ffffff"
        },
        "Modern": {
            "primary": "#6366f1", "secondary": "#4f46e5", "accent": "#eef2ff",
            "font_main": "'Inter', sans-serif", "font_head": "'Outfit', sans-serif",
            "header_bg": "#ffffff", "border_color": "#6366f1", "sidebar_bg": "#ffffff"
        },
        "Colorful": {
            "primary": "#4f46e5", "secondary": "#6366f1", "accent": "#f5f3ff",
            "font_main": "'Inter', sans-serif", "font_head": "'Inter', sans-serif",
            "header_bg": "#4f46e5", "border_color": "#4f46e5", "sidebar_bg": "#ffffff", "header_text": "#ffffff"
        }
    }
    t = themes.get(theme, themes["Classic"])
    header_text_color = t.get('header_text', t['primary'])

    # Sections builder
    summary_html = f'''
    <div class="section">
        <h2 class="section-title">Professional Summary</h2>
        <div class="summary-text">{cv_data.get('summary', '')}</div>
    </div>
    ''' if cv_data.get('summary') else ''

    experience_items = ""
    for exp in cv_data.get('experience', []):
        desc = exp.get('description', '').replace('\n', '<br>')
        experience_items += f"""
        <div class="exp-item">
            <div class="exp-header">
                <div class="exp-main">
                    <span class="job-title">{exp.get('job_title', 'Job Title')}</span>
                    <span class="company-name">{exp.get('company', 'Company Name')}</span>
                </div>
                <div class="exp-date">{exp.get('start_date', '')} — {exp.get('end_date', 'Present')}</div>
            </div>
            <div class="exp-desc">{desc}</div>
        </div>
        """
    experience_html = f'''
    <div class="section">
        <h2 class="section-title">Work Experience</h2>
        {experience_items}
    </div>
    ''' if experience_items else ''

    education_items = ""
    for edu in cv_data.get('education', []):
        education_items += f"""
        <div class="side-item">
            <div class="side-item-title">{edu.get('degree', 'Degree')}</div>
            <div class="side-item-sub">{edu.get('institution', 'Institution')}</div>
            <div class="side-item-meta">{edu.get('year', '')}</div>
        </div>
        """
    education_html = f'''
    <div class="side-section">
        <h3 class="side-title">Education</h3>
        {education_items}
    </div>
    ''' if education_items else ''

    skills_raw = cv_data.get('skills', [])
    if isinstance(skills_raw, str):
        skills_raw = [s.strip() for s in skills_raw.split(',') if s.strip()]
    
    skill_tags = "".join([f'<span>{s}</span>' for s in skills_raw])
    skills_html = f'''
    <div class="side-section">
        <h3 class="side-title">Skills</h3>
        <div class="skill-cloud">{skill_tags}</div>
    </div>
    ''' if skill_tags else ''

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{cv_data.get('full_name', 'Resume')}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Outfit:wght@700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: {t['primary']};
            --secondary: {t['secondary']};
            --accent: {t['accent']};
            --header-text: {header_text_color};
        }}
        * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; }}
        
        @page {{ size: A4; margin: 0; }}

        body {{
            background: #cbd5e1;
            font-family: 'Inter', sans-serif;
            color: #1e293b;
            margin: 0;
            padding: 40px 0;
            line-height: 1.5;
        }}

        .page {{
            width: 210mm;
            min-height: 297mm;
            margin: 0 auto;
            background: white;
            box-shadow: 0 40px 100px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            overflow: hidden;
        }}

        @media print {{
            body {{ background: white; padding: 0; }}
            .page {{ box-shadow: none; margin: 0; width: 100%; }}
            .no-print {{ display: none !important; }}
        }}

        header {{
            padding: 60px 80px;
            background: {t['header_bg']};
            border-bottom: 8px solid var(--primary);
            color: var(--header-text);
        }}
        header h1 {{
            margin: 0;
            font-family: 'Outfit', sans-serif;
            font-size: 48px;
            font-weight: 800;
            line-height: 1.1;
            letter-spacing: -2px;
            text-transform: uppercase;
        }}
        .header-meta {{
            margin-top: 20px;
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            font-size: 14px;
            font-weight: 600;
            opacity: 0.9;
        }}

        .grid {{
            display: grid;
            grid-template-columns: 1.8fr 1fr;
            flex-grow: 1;
        }}

        .main-col {{ padding: 50px 40px 50px 80px; }}
        .side-col {{
            background: {t['sidebar_bg']};
            padding: 50px 60px 50px 40px;
            border-left: 1px solid #e2e8f0;
        }}

        .section {{ margin-bottom: 40px; }}
        .section-title {{
            font-size: 16px;
            font-weight: 800;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 20px;
            border-bottom: 2px solid var(--accent);
            padding-bottom: 8px;
        }}

        .summary-text {{ font-size: 14px; color: #334155; text-align: justify; }}
        
        .exp-item {{ margin-bottom: 25px; }}
        .exp-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px; }}
        .job-title {{ font-size: 18px; font-weight: 700; color: #0f172a; display: block; }}
        .company-name {{ font-size: 15px; font-weight: 600; color: var(--primary); }}
        .exp-date {{ font-size: 12px; font-weight: 700; color: var(--secondary); white-space: nowrap; }}
        .exp-desc {{ font-size: 13.5px; color: #475569; line-height: 1.6; }}

        .side-section {{ margin-bottom: 35px; }}
        .side-title {{
            font-size: 14px;
            font-weight: 800;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 15px;
        }}
        .side-item {{ margin-bottom: 20px; }}
        .side-item-title {{ font-size: 14px; font-weight: 700; color: #0f172a; }}
        .side-item-sub {{ font-size: 13px; color: var(--secondary); font-weight: 500; margin-top: 2px; }}
        .side-item-meta {{ font-size: 12px; color: #94a3b8; font-weight: 600; margin-top: 4px; }}

        .skill-cloud {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .skill-cloud span {{
            background: white;
            color: var(--primary);
            padding: 4px 10px;
            border-radius: 4px;
            font-size: 12px;
            font-weight: 600;
            border: 1px solid #e2e8f0;
        }}

        .toolbar {{
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            background: #0f172a;
            padding: 10px 20px;
            border-radius: 50px;
            display: flex;
            gap: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.3);
            z-index: 1000;
        }}
        .tool-btn {{
            background: #6366f1;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 50px;
            font-weight: 700;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .tool-btn:hover {{ transform: translateY(-2px); box-shadow: 0 5px 15px rgba(99, 102, 241, 0.4); }}
    </style>
</head>
<body>
    <div class="toolbar no-print">
        <button class="tool-btn" onclick="window.print()">📥 SAVE AS PDF</button>
        <button class="tool-btn" style="background: #10b981;" onclick="downloadHTML()">💾 DOWNLOAD HTML</button>
    </div>
    <script>
        function downloadHTML() {{
            const clone = document.documentElement.cloneNode(true);
            const toolbar = clone.querySelector('.toolbar');
            if (toolbar) toolbar.remove();
            const html = '<!DOCTYPE html>\\n' + clone.outerHTML;
            const blob = new Blob([html], {{ type: 'text/html' }});
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'resume.html';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        }}
    </script>
    <div class="page">
        <header>
            <h1>{cv_data.get('full_name', 'Your Name')}</h1>
            <div class="header-meta">
                <span>{cv_data.get('email', '')}</span>
                <span>{cv_data.get('phone', '')}</span>
                <span>{cv_data.get('address', '')}</span>
                <span>{cv_data.get('linkedin', '')}</span>
            </div>
        </header>

        <div class="grid">
            <div class="main-col">
                {summary_html}
                {experience_html}
            </div>
            <div class="side-col">
                {education_html}
                {skills_html}
            </div>
        </div>
    </div>
</body>
</html>
"""
    return html

