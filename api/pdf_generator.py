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
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        :root {{
            --primary: {t['primary']};
            --secondary: {t['secondary']};
            --accent: {t['accent']};
            --header-text: {header_text_color};
            --text-dark: #0f172a;
            --text-light: #64748b;
            --border-light: #e2e8f0;
        }}
        * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; }}
        
        @page {{ size: A4; margin: 0; }}

        body {{
            background: #cbd5e1;
            font-family: 'Inter', sans-serif;
            color: var(--text-dark);
            margin: 0;
            padding: 40px 0;
            line-height: 1.6;
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
            border-bottom: 6px solid var(--primary);
            color: var(--header-text);
        }}
        header h1 {{
            margin: 0;
            font-family: 'Outfit', sans-serif;
            font-size: 52px;
            font-weight: 800;
            line-height: 1;
            letter-spacing: -2px;
            text-transform: uppercase;
        }}
        .header-meta {{
            margin-top: 25px;
            display: flex;
            flex-wrap: wrap;
            gap: 24px;
            font-size: 13px;
            font-weight: 600;
        }}
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 8px;
            opacity: 0.9;
        }}
        .meta-item i {{
            width: 16px;
            height: 16px;
            color: var(--primary);
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
            border-left: 1px solid var(--border-light);
        }}

        .section {{ margin-bottom: 45px; position: relative; }}
        .section-title {{
            font-size: 15px;
            font-weight: 800;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .section-title::after {{
            content: '';
            flex: 1;
            height: 1px;
            background: var(--accent);
        }}

        .summary-text {{ font-size: 14.5px; color: var(--text-light); text-align: justify; line-height: 1.7; }}
        
        .exp-item {{ margin-bottom: 30px; position: relative; padding-left: 20px; border-left: 2px solid var(--accent); }}
        .exp-item::before {{
            content: '';
            position: absolute;
            left: -6px;
            top: 6px;
            width: 10px;
            height: 10px;
            background: var(--primary);
            border-radius: 50%;
        }}
        .exp-header {{ margin-bottom: 10px; }}
        .job-title {{ font-size: 19px; font-weight: 700; color: var(--text-dark); display: block; }}
        .company-name {{ font-size: 15px; font-weight: 600; color: var(--primary); margin-top: 2px; display: block; }}
        .exp-date {{ font-size: 12px; font-weight: 700; color: var(--text-light); text-transform: uppercase; letter-spacing: 0.5px; margin-top: 4px; display: block; }}
        .exp-desc {{ font-size: 13.5px; color: var(--text-light); line-height: 1.6; margin-top: 10px; }}

        .side-section {{ margin-bottom: 40px; }}
        .side-title {{
            font-size: 14px;
            font-weight: 800;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 20px;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--accent);
        }}
        .side-item {{ margin-bottom: 25px; }}
        .side-item-title {{ font-size: 14.5px; font-weight: 700; color: var(--text-dark); }}
        .side-item-sub {{ font-size: 13px; color: var(--text-light); font-weight: 500; margin-top: 4px; }}
        .side-item-meta {{ font-size: 12px; color: var(--text-light); font-weight: 600; margin-top: 6px; opacity: 0.8; }}

        .skill-cloud {{ display: flex; flex-wrap: wrap; gap: 8px; }}
        .skill-cloud span {{
            background: white;
            color: var(--primary);
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 700;
            border: 1px solid var(--border-light);
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }}

        .toolbar {{
            position: fixed;
            bottom: 30px;
            left: 50%;
            transform: translateX(-50%);
            background: #0f172a;
            padding: 12px 24px;
            border-radius: 50px;
            display: flex;
            gap: 15px;
            box-shadow: 0 20px 50px rgba(0,0,0,0.4);
            z-index: 1000;
        }}
        .tool-btn {{
            background: #6366f1;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 50px;
            font-weight: 700;
            font-size: 13px;
            cursor: pointer;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .tool-btn:hover {{ transform: translateY(-3px) scale(1.05); box-shadow: 0 10px 20px rgba(99, 102, 241, 0.4); }}
    </style>
</head>
<body>
    <div class="toolbar no-print">
        <button class="tool-btn" onclick="window.print()"><i data-lucide="file-down"></i> SAVE AS PDF</button>
        <button class="tool-btn" style="background: #10b981;" onclick="downloadHTML()"><i data-lucide="code"></i> DOWNLOAD HTML</button>
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
        window.onload = () => {{ lucide.createIcons(); }};
    </script>
    <div class="page">
        <header>
            <h1>{cv_data.get('full_name', 'Your Name')}</h1>
            <div class="header-meta">
                {f'<div class="meta-item"><i data-lucide="mail"></i> <span>{cv_data.get("email")}</span></div>' if cv_data.get("email") else ""}
                {f'<div class="meta-item"><i data-lucide="phone"></i> <span>{cv_data.get("phone")}</span></div>' if cv_data.get("phone") else ""}
                {f'<div class="meta-item"><i data-lucide="map-pin"></i> <span>{cv_data.get("address")}</span></div>' if cv_data.get("address") else ""}
                {f'<div class="meta-item"><i data-lucide="linkedin"></i> <span>{cv_data.get("linkedin")}</span></div>' if cv_data.get("linkedin") else ""}
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

