def get_web_html(cv_data):
    """Generates professional HTML resumes with 6 distinct design templates."""
    theme = cv_data.get('template', 'Classic')

    themes = {
        "Classic": {
            "primary": "#1e293b", "secondary": "#64748b", "accent": "#f1f5f9",
            "header_bg": "#ffffff", "sidebar_bg": "#f8fafc", "header_text": "#1e293b"
        },
        "Formal": {
            "primary": "#0f172a", "secondary": "#475569", "accent": "#e2e8f0",
            "header_bg": "#f1f5f9", "sidebar_bg": "#ffffff", "header_text": "#0f172a"
        },
        "Modern": {
            "primary": "#6366f1", "secondary": "#4f46e5", "accent": "#eef2ff",
            "header_bg": "#ffffff", "sidebar_bg": "#fafafa", "header_text": "#4f46e5"
        },
        "Colorful": {
            "primary": "#4f46e5", "secondary": "#7c3aed", "accent": "#f5f3ff",
            "header_bg": "#4f46e5", "sidebar_bg": "#f5f3ff", "header_text": "#ffffff"
        },
        "Executive": {
            "primary": "#ffffff", "secondary": "#cbd5e1", "accent": "#334155",
            "header_bg": "#0f172a", "sidebar_bg": "#1e293b", "header_text": "#ffffff",
            "body_bg": "#f8fafc", "main_bg": "#ffffff", "sidebar_text": "#e2e8f0"
        },
        "Creative": {
            "primary": "#0f766e", "secondary": "#0d9488", "accent": "#f0fdfa",
            "header_bg": "#ffffff", "sidebar_bg": "#f0fdfa", "header_text": "#0f766e"
        },
    }
    t = themes.get(theme, themes["Classic"])
    header_text_color = t.get('header_text', t['primary'])

    # ── Build section HTML blocks ──────────────────────────────────────────────
    summary_html = ""
    if cv_data.get('summary'):
        summary_html = f'''
        <div class="section">
            <h2 class="section-title">Professional Summary</h2>
            <div class="summary-text">{cv_data.get('summary', '')}</div>
        </div>'''

    experience_items = ""
    for exp in cv_data.get('experience', []):
        desc = exp.get('description', '').replace('\n', '<br>')
        experience_items += f"""
        <div class="exp-item">
            <div class="exp-header">
                <div class="exp-main">
                    <span class="job-title">{exp.get('job_title', '')}</span>
                    <span class="company-name">{exp.get('company', '')}</span>
                </div>
                <div class="exp-date">{exp.get('start_date', '')} — {exp.get('end_date', 'Present')}</div>
            </div>
            <div class="exp-desc">{desc}</div>
        </div>"""
    experience_html = f'''
        <div class="section">
            <h2 class="section-title">Work Experience</h2>
            {experience_items}
        </div>''' if experience_items else ''

    # Projects section
    project_items = ""
    for proj in cv_data.get('projects', []):
        desc = proj.get('description', '').replace('\n', '<br>')
        link_html = f'<a class="proj-link" href="{proj.get("link")}">{proj.get("link")}</a>' if proj.get('link') else ''
        project_items += f"""
        <div class="exp-item">
            <div class="exp-header">
                <div class="exp-main">
                    <span class="job-title">{proj.get('name', '')}</span>
                    {link_html}
                </div>
            </div>
            <div class="exp-desc">{desc}</div>
        </div>"""
    projects_html = f'''
        <div class="section">
            <h2 class="section-title">Key Projects</h2>
            {project_items}
        </div>''' if project_items else ''

    education_items = ""
    for edu in cv_data.get('education', []):
        education_items += f"""
        <div class="side-item">
            <div class="side-item-title">{edu.get('degree', '')}</div>
            <div class="side-item-sub">{edu.get('institution', '')}</div>
            <div class="side-item-meta">{edu.get('year', '')}</div>
        </div>"""
    education_html = f'''
        <div class="side-section">
            <h3 class="side-title">Education</h3>
            {education_items}
        </div>''' if education_items else ''

    skills_raw = cv_data.get('skills', [])
    if isinstance(skills_raw, str):
        skills_raw = [s.strip() for s in skills_raw.split(',') if s.strip()]
    skill_tags = "".join([f'<span>{s}</span>' for s in skills_raw])
    skills_html = f'''
        <div class="side-section">
            <h3 class="side-title">Skills</h3>
            <div class="skill-cloud">{skill_tags}</div>
        </div>''' if skill_tags else ''

    meta_html = ""
    if cv_data.get("email"):
        meta_html += f'<div class="meta-item"><i data-lucide="mail"></i> {cv_data.get("email")}</div>'
    if cv_data.get("phone"):
        meta_html += f'<div class="meta-item"><i data-lucide="phone"></i> {cv_data.get("phone")}</div>'
    if cv_data.get("address"):
        meta_html += f'<div class="meta-item"><i data-lucide="map-pin"></i> {cv_data.get("address")}</div>'
    if cv_data.get("linkedin"):
        meta_html += f'<div class="meta-item"><i data-lucide="linkedin"></i> {cv_data.get("linkedin")}</div>'

    # ── Per-theme CSS overrides ────────────────────────────────────────────────
    theme_css = ""

    if theme == "Classic":
        theme_css = """
        body { font-family: 'Georgia', 'Times New Roman', serif; }
        h1 { font-family: 'Georgia', serif; letter-spacing: 0; font-size: 32px; }
        .section { border-radius: 0; background: none; border: none; padding: 0;
                   border-top: 2px solid #1e293b; padding-top: 18px; margin-bottom: 28px; }
        .section-title { font-family: 'Georgia', serif; font-size: 14px; letter-spacing: 1px; }
        .section-title::after { display: none; }
        .side-section { border-radius: 0; background: none; box-shadow: none; border: none;
                        padding: 0; border-top: 2px solid #1e293b; padding-top: 18px; }
        header { border-bottom: 3px double #1e293b; justify-content: center; flex-direction: column; text-align: center; }
        .header-meta { grid-template-columns: repeat(4, auto); justify-content: center; gap: 8px 24px; }
        .skill-cloud span { border-radius: 0; border: 1px solid #1e293b; background: transparent; color: #1e293b; font-family: 'Georgia', serif; }
        .exp-date { background: transparent; border: none; font-family: 'Georgia', serif; color: #64748b; }
        .company-name { background: transparent; padding: 0; font-style: italic; color: #475569; }
        """

    elif theme == "Formal":
        theme_css = """
        body { font-family: 'Arial', 'Helvetica', sans-serif; }
        .section { border-radius: 2px; border: 1px solid #e2e8f0; background: #fafafa; padding: 20px; }
        .section-title { font-size: 12px; letter-spacing: 3px; border-bottom: 2px solid #0f172a;
                         padding-bottom: 6px; margin-bottom: 20px; }
        .section-title::after { display: none; }
        .side-section { border-radius: 2px; box-shadow: none; border: 1px solid #e2e8f0; background: white; }
        .skill-cloud span { border-radius: 0; background: #fff; border: 1px solid #94a3b8; color: #1e293b; font-weight: 600; }
        .exp-item { border-left: 3px solid #0f172a; padding-left: 16px; border-bottom: none; }
        .exp-date { background: #f1f5f9; border: none; color: #475569; border-radius: 2px; }
        header { background: #f1f5f9; border-bottom: 2px solid #0f172a; }
        .summary-text { border-left: none; padding-left: 0; border-top: 1px solid #e2e8f0; padding-top: 12px; }
        """

    elif theme == "Modern":
        theme_css = """
        .page { border-radius: 16px; overflow: hidden; box-shadow: 0 40px 100px rgba(99,102,241,0.15); }
        header { background: linear-gradient(135deg, #6366f1, #4f46e5); color: white; border-bottom: none; }
        .header-content h1 { color: white; text-shadow: 0 2px 10px rgba(0,0,0,0.2); }
        .meta-item { color: rgba(255,255,255,0.9); }
        .meta-item i { color: #a5b4fc; }
        .section { background: white; box-shadow: 0 2px 16px rgba(99,102,241,0.06); border: 1px solid #eef2ff; }
        .section-title { background: linear-gradient(135deg, #6366f1, #4f46e5);
                         -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
        .section-title::after { background: linear-gradient(to right, #6366f1, transparent); }
        .skill-cloud span { background: #eef2ff; color: #4f46e5; border-radius: 20px;
                            box-shadow: 0 2px 6px rgba(99,102,241,0.15); border: none; }
        .exp-date { background: linear-gradient(135deg, #6366f1, #4f46e5); color: white; border: none;
                    box-shadow: 0 4px 10px rgba(99,102,241,0.3); }
        .company-name { color: #6366f1; background: #eef2ff; }
        .side-section { border: 1px solid #eef2ff; box-shadow: 0 2px 12px rgba(99,102,241,0.05); }
        .side-title { border-bottom-color: #6366f1; }
        """

    elif theme == "Colorful":
        theme_css = """
        header { background: linear-gradient(135deg, #4f46e5, #7c3aed); color: white; border-bottom: none; }
        .header-content h1 { color: white; text-shadow: 2px 2px 8px rgba(0,0,0,0.25); }
        .meta-item { color: rgba(255,255,255,0.92); }
        .meta-item i { color: #facc15; }
        .section-title::after { background: linear-gradient(to right, #4f46e5, #7c3aed, transparent); height: 3px; }
        .exp-date { background: linear-gradient(135deg, #4f46e5, #7c3aed); color: white; border: none;
                    box-shadow: 0 4px 12px rgba(79,70,229,0.35); }
        .company-name { background: #ede9fe; color: #4f46e5; border-radius: 20px; padding: 3px 12px; }
        .skill-cloud span { background: linear-gradient(135deg, #4f46e5, #7c3aed); color: white;
                            border-radius: 8px; border: none; box-shadow: 0 4px 10px rgba(79,70,229,0.25); }
        .side-col { background: #f5f3ff; }
        .side-title { border-bottom-color: #7c3aed; color: #4f46e5; }
        .section { border: 1px solid #ede9fe; }
        """

    elif theme == "Executive":
        theme_css = """
        body { background: #f8fafc; font-family: 'Inter', sans-serif; }
        .page { display: grid; grid-template-rows: auto 1fr; min-height: 297mm; }
        header { background: #0f172a; color: white; border-bottom: 4px solid #6366f1; padding: 50px 60px; }
        .header-content h1 { color: white; font-size: 42px; letter-spacing: -2px; }
        .meta-item { color: #94a3b8; }
        .meta-item i { color: #6366f1; }
        .grid { flex: 1; }
        .main-col { background: white; }
        .side-col { background: #1e293b; border-left: none; }
        .side-title { color: #94a3b8; border-bottom-color: #334155; }
        .side-item-title { color: #e2e8f0; }
        .side-item-sub { color: #94a3b8; }
        .side-item-meta { color: #6366f1; }
        .side-section { background: transparent; box-shadow: none; border: none;
                        border-bottom: 1px solid #334155; border-radius: 0; padding: 0 0 20px 0; margin-bottom: 20px; }
        .skill-cloud span { background: #334155; color: #e2e8f0; border-radius: 6px; border: 1px solid #475569; }
        .section { border: none; background: none; border-radius: 0;
                   border-bottom: 1px solid #f1f5f9; padding: 0 0 24px 0; margin-bottom: 24px; }
        .section-title { color: #0f172a; }
        .section-title::after { background: linear-gradient(to right, #6366f1, transparent); height: 2px; }
        .exp-date { background: #f1f5f9; border: 1px solid #e2e8f0; color: #475569; }
        .exp-item { border-bottom: 1px dashed #f1f5f9; }
        """

    elif theme == "Creative":
        theme_css = """
        body { font-family: 'Inter', sans-serif; }
        header { background: white; border-bottom: none; border-left: 8px solid #0f766e; padding: 40px 50px; }
        .header-content h1 { font-size: 40px; color: #0f766e; letter-spacing: -2px; }
        .meta-item { color: #475569; }
        .meta-item i { color: #0d9488; }
        .section { border: none; background: none; border-radius: 0;
                   border-left: 4px solid #0f766e; padding: 0 0 24px 20px; margin-bottom: 24px; }
        .section-title { color: #0f766e; font-size: 11px; letter-spacing: 3px; }
        .section-title::after { background: linear-gradient(to right, #0f766e, transparent); height: 1px; }
        .summary-text { border-left: none; padding-left: 0; font-style: italic; color: #334155; }
        .exp-date { background: #f0fdfa; color: #0f766e; border: 1px solid #99f6e4; border-radius: 20px; }
        .company-name { color: #0d9488; background: #f0fdfa; border-radius: 4px; }
        .skill-cloud span { background: #f0fdfa; color: #0f766e; border: 1px solid #99f6e4; border-radius: 4px; }
        .side-col { background: #f0fdfa; border-left: 4px solid #0f766e; }
        .side-title { color: #0f766e; border-bottom-color: #99f6e4; }
        .side-section { background: white; border: 1px solid #99f6e4; border-radius: 8px; }
        .side-item-meta { color: #0d9488; }
        """

    # ── Main HTML Template ─────────────────────────────────────────────────────
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{cv_data.get('full_name', 'Resume')} — Resume</title>
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
        * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
        @page {{ size: A4; margin: 0; }}

        body {{
            background: #e2e8f0;
            font-family: 'Inter', sans-serif;
            color: var(--text-dark);
            margin: 0;
            padding: 24px 0;
            line-height: 1.55;
        }}
        .page {{
            width: 210mm;
            min-height: 297mm;
            margin: 0 auto;
            background: white;
            box-shadow: 0 25px 60px rgba(0,0,0,0.12);
            display: flex;
            flex-direction: column;
        }}
        @media print {{
            body {{ background: white; padding: 0; }}
            .page {{ box-shadow: none; margin: 0; width: 100%; border-radius: 0 !important; }}
            .no-print {{ display: none !important; }}
        }}

        /* ── Theme override injection ── */
        {theme_css}

        /* ── Base structural styles (overridable by theme_css) ── */
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
            font-size: 38px;
            font-weight: 800;
            line-height: 1;
            letter-spacing: -1.5px;
            color: {header_text_color};
            text-transform: uppercase;
        }}
        .header-meta {{
            margin-top: 16px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px 24px;
            font-size: 12px;
            font-weight: 600;
        }}
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 7px;
            color: var(--text-light);
        }}
        .meta-item i {{ width: 14px; height: 14px; color: var(--primary); }}

        .grid {{ display: grid; grid-template-columns: 1.8fr 1fr; flex: 1; }}
        .main-col {{ padding: 40px 40px 40px 60px; }}
        .side-col {{
            background: {t['sidebar_bg']};
            padding: 40px 40px 40px 32px;
            border-left: 1px solid var(--border-light);
        }}

        .section {{
            margin-bottom: 32px;
            padding: 20px;
            background: rgba(255,255,255,0.6);
            border-radius: 10px;
            border: 1px solid var(--border-light);
        }}
        .section-title {{
            font-size: 11px;
            font-weight: 900;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 2.5px;
            margin-bottom: 22px;
            display: flex;
            align-items: center;
            gap: 14px;
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
            line-height: 1.75;
            text-align: justify;
            border-left: 3px solid var(--accent);
            padding-left: 14px;
        }}

        .exp-item {{
            margin-bottom: 28px;
            padding-bottom: 20px;
            border-bottom: 1px dashed var(--border-light);
        }}
        .exp-item:last-child {{ border-bottom: none; padding-bottom: 0; margin-bottom: 0; }}
        .exp-header {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; }}
        .exp-main {{ flex: 1; }}
        .job-title {{ display: block; font-size: 16px; font-weight: 800; color: var(--text-dark); letter-spacing: -0.3px; }}
        .company-name {{
            display: inline-block;
            font-size: 13px;
            font-weight: 700;
            color: var(--primary);
            margin-top: 5px;
            padding: 2px 10px;
            background: var(--accent);
            border-radius: 5px;
        }}
        .proj-link {{
            display: inline-block;
            font-size: 12px;
            color: var(--secondary);
            margin-top: 5px;
            text-decoration: none;
        }}
        .exp-date {{
            font-size: 11px;
            font-weight: 800;
            color: var(--text-light);
            text-transform: uppercase;
            white-space: nowrap;
            background: var(--accent);
            padding: 5px 12px;
            border-radius: 20px;
            border: 1px solid var(--border-light);
        }}
        .exp-desc {{ font-size: 12.5px; color: var(--text-light); line-height: 1.65; margin-top: 12px; }}

        .side-section {{
            margin-bottom: 32px;
            padding: 18px;
            background: white;
            border-radius: 10px;
            border: 1px solid rgba(0,0,0,0.04);
            box-shadow: 0 2px 10px rgba(0,0,0,0.03);
        }}
        .side-title {{
            font-size: 11px;
            font-weight: 900;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 18px;
            padding-bottom: 8px;
            border-bottom: 2px solid var(--accent);
        }}
        .side-item {{ margin-bottom: 18px; }}
        .side-item:last-child {{ margin-bottom: 0; }}
        .side-item-title {{ font-size: 13px; font-weight: 700; color: var(--text-dark); }}
        .side-item-sub {{ font-size: 12px; color: var(--text-light); margin-top: 3px; font-weight: 500; }}
        .side-item-meta {{ font-size: 11px; color: var(--primary); font-weight: 800; margin-top: 5px; display: inline-block; opacity: 0.8; }}

        .skill-cloud {{ display: flex; flex-wrap: wrap; gap: 7px; }}
        .skill-cloud span {{
            background: var(--accent);
            color: var(--primary);
            padding: 5px 13px;
            border-radius: 7px;
            font-size: 11px;
            font-weight: 700;
            border: 1px solid transparent;
        }}

        /* ── Floating toolbar (editor preview only) ── */
        .toolbar {{
            position: fixed;
            bottom: 18px;
            left: 50%;
            transform: translateX(-50%);
            background: #0f172a;
            padding: 8px 16px;
            border-radius: 50px;
            display: flex;
            gap: 10px;
            box-shadow: 0 8px 28px rgba(0,0,0,0.35);
            z-index: 1000;
        }}
        .tool-btn {{
            background: #6366f1;
            color: white;
            border: none;
            padding: 8px 18px;
            border-radius: 50px;
            font-weight: 700;
            font-size: 11px;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 6px;
            transition: transform 0.15s ease;
        }}
        .tool-btn:hover {{ transform: translateY(-2px); }}
        .tool-btn.pdf  {{ background: #4b5563; }}
        .tool-btn.html {{ background: #10b981; }}
    </style>
</head>
<body>
    <div class="toolbar no-print">
        <button class="tool-btn" onclick="triggerSave()"><i data-lucide="save"></i> SAVE</button>
        <button class="tool-btn pdf" onclick="window.print()"><i data-lucide="printer"></i> PDF</button>
        <button class="tool-btn html" onclick="downloadHTML()"><i data-lucide="download"></i> HTML</button>
    </div>
    <script>
        function triggerSave() {{
            if (window.parent && typeof window.parent.saveCV === 'function') {{
                window.parent.saveCV();
            }} else {{
                alert("Save is only available inside the Resume Editor.");
            }}
        }}
        function downloadHTML() {{
            const clone = document.documentElement.cloneNode(true);
            const toolbar = clone.querySelector('.toolbar');
            if (toolbar) toolbar.remove();
            const blob = new Blob(['<!DOCTYPE html>\\n' + clone.outerHTML], {{ type: 'text/html' }});
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
                {projects_html}
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
