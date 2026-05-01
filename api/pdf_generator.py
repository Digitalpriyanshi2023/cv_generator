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

    # Meta section builder (avoid nested f-strings for better compatibility)
    meta_html = ""
    if cv_data.get("email"):
        meta_html += f'<div class="meta-item"><i data-lucide="mail"></i> {cv_data.get("email")}</div>'
    if cv_data.get("phone"):
        meta_html += f'<div class="meta-item"><i data-lucide="phone"></i> {cv_data.get("phone")}</div>'
    if cv_data.get("address"):
        meta_html += f'<div class="meta-item"><i data-lucide="map-pin"></i> {cv_data.get("address")}</div>'
    if cv_data.get("linkedin"):
        meta_html += f'<div class="meta-item"><i data-lucide="linkedin"></i> {cv_data.get("linkedin")}</div>'

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{cv_data.get('full_name', 'Resume')}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Outfit:wght@700;800&display=swap" rel="stylesheet">
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        :root {{
            --primary: {t['primary']};
            --secondary: {t['secondary']};
            --accent: {t['accent']};
            --header-text: {header_text_color};
            --text-dark: #1e293b;
            --text-light: #64748b;
            --border-light: #f1f5f9;
        }}
        * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; }}
        
        @page {{ size: A4; margin: 0; }}

        body {{
            background: #f1f5f9;
            font-family: 'Inter', sans-serif;
            color: var(--text-dark);
            margin: 0;
            padding: 20px 0;
            line-height: 1.5;
        }}

        .page {{
            width: 210mm;
            min-height: 297mm;
            margin: 0 auto;
            background: white;
            box-shadow: 0 20px 50px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
        }}

        @media print {{
            body {{ background: white; padding: 0; }}
            .page {{ box-shadow: none; margin: 0; width: 100%; }}
            .no-print {{ display: none !important; }}
        }}

        header {{
            padding: 40px 60px;
            background: {t['header_bg']};
            border-bottom: 1px solid var(--border-light);
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .header-content h1 {{
            margin: 0;
            font-family: 'Outfit', sans-serif;
            font-size: 36px;
            font-weight: 800;
            line-height: 1;
            letter-spacing: -1.5px;
            color: var(--primary);
            text-transform: uppercase;
        }}
        .header-meta {{
            margin-top: 15px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px 20px;
            font-size: 12px;
            font-weight: 600;
        }}
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            color: var(--text-light);
        }}
        .meta-item i {{
            width: 14px;
            height: 14px;
            color: var(--primary);
        }}

        .grid {{
            display: grid;
            grid-template-columns: 1.8fr 1fr;
            flex: 1;
        }}

        .main-col {{ padding: 40px 40px 40px 60px; }}
        .side-col {{
            background: {t['sidebar_bg']};
            padding: 40px 60px 40px 40px;
            border-left: 1px solid var(--border-light);
        }}

        .section {{ 
            margin-bottom: 35px; 
            padding: 20px;
            background: rgba(255, 255, 255, 0.5);
            border-radius: 12px;
            border: 1px solid var(--border-light);
            transition: 0.3s;
        }}
        .section-title {{
            font-size: 13px;
            font-weight: 900;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 15px;
        }}
        .section-title::after {{
            content: '';
            flex: 1;
            height: 2px;
            background: linear-gradient(to right, var(--accent), transparent);
        }}

        .summary-text {{ 
            font-size: 13.5px; 
            color: var(--text-dark); 
            line-height: 1.7; 
            text-align: justify; 
            padding-left: 10px;
            border-left: 3px solid var(--accent);
        }}
        
        .exp-item {{ 
            margin-bottom: 30px; 
            position: relative;
            padding-bottom: 20px;
            border-bottom: 1px dashed var(--border-light);
        }}
        .exp-item:last-child {{ border-bottom: none; padding-bottom: 0; }}

        .exp-header {{ display: flex; justify-content: space-between; align-items: flex-start; }}
        .job-title {{ font-size: 17px; font-weight: 800; color: var(--text-dark); letter-spacing: -0.5px; }}
        .company-name {{ 
            font-size: 14px; 
            font-weight: 700; 
            color: var(--primary); 
            margin-top: 4px;
            display: inline-block;
            padding: 2px 8px;
            background: var(--accent);
            border-radius: 4px;
        }}
        .exp-date {{ 
            font-size: 11px; 
            font-weight: 800; 
            color: var(--text-light); 
            text-transform: uppercase; 
            background: #f8fafc;
            padding: 4px 10px;
            border-radius: 20px;
            border: 1px solid var(--border-light);
        }}
        .exp-desc {{ font-size: 13px; color: var(--text-light); line-height: 1.6; margin-top: 12px; }}

        .side-section {{ 
            margin-bottom: 35px; 
            padding: 20px;
            background: white;
            border-radius: 12px;
            border: 1px solid rgba(0,0,0,0.03);
            box-shadow: 0 4px 12px rgba(0,0,0,0.02);
        }}
        .side-title {{
            font-size: 12px;
            font-weight: 900;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 20px;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--accent);
            display: flex;
            justify-content: space-between;
        }}
        .side-item {{ margin-bottom: 20px; }}
        .side-item:last-child {{ margin-bottom: 0; }}
        .side-item-title {{ font-size: 13.5px; font-weight: 700; color: var(--text-dark); }}
        .side-item-sub {{ font-size: 12.5px; color: var(--text-light); margin-top: 4px; font-weight: 500; }}
        .side-item-meta {{ 
            font-size: 11px; 
            color: var(--primary); 
            font-weight: 800; 
            margin-top: 6px; 
            display: inline-block;
            opacity: 0.8;
        }}

        .skill-cloud {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .skill-cloud span {{
            background: var(--accent);
            color: var(--primary);
            padding: 6px 14px;
            border-radius: 8px;
            font-size: 11px;
            font-weight: 800;
            border: 1px solid transparent;
            transition: 0.2s;
        }}
        .skill-cloud span:hover {{
            background: var(--primary);
            color: white;
        }}

        .toolbar {{
            position: fixed;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            background: #0f172a;
            padding: 10px 20px;
            border-radius: 50px;
            display: flex;
            gap: 12px;
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
            font-size: 12px;
            cursor: pointer;
            transition: 0.2s;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .tool-btn:hover {{ transform: translateY(-2px); }}
    </style>
</head>
<body>
    <div class="toolbar no-print">
        <button class="tool-btn" style="background: #6366f1;" onclick="triggerSave()"><i data-lucide="save"></i> SAVE</button>
        <button class="tool-btn" style="background: #4b5563;" onclick="window.print()"><i data-lucide="printer"></i> PDF</button>
        <button class="tool-btn" style="background: #10b981;" onclick="downloadHTML()"><i data-lucide="download"></i> HTML</button>
    </div>
    <script>
        function triggerSave() {{
            if (window.parent && typeof window.parent.saveCV === 'function') {{
                window.parent.saveCV();
            }} else {{
                alert("Save action is only available within the Resume Editor.");
            }}
        }}
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
        window.onload = () => {{ lucide.createIcons(); }};
    </script>
    <div class="page">
        <header>
            <div class="header-content">
                <h1>{cv_data.get('full_name', 'Your Name')}</h1>
                <div class="header-meta">
                    {meta_html}
                </div>
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

