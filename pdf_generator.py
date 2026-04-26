def get_qt_html(cv_data):
    """Generates basic HTML compatible with QTextBrowser for live preview."""
    theme = cv_data.get('template', 'Classic')
    accent = "#6366f1" if theme == "Colorful" else "#0f172a"
    
    html = f"""
    <div style="font-family: 'Inter', sans-serif; padding: 25px; color: #1e293b; background: white;">
        <div style="border-left: 8px solid {accent}; padding-left: 20px; margin-bottom: 30px;">
            <h1 style="margin: 0; color: {accent}; font-size: 32px; font-weight: 900; text-transform: uppercase; letter-spacing: -1px;">{cv_data.get('full_name', 'Your Name') or 'Your Name'}</h1>
            <p style="margin: 8px 0 0 0; font-size: 14px; color: #64748b; font-weight: 600;">
                {cv_data.get('email', '')} &bull; {cv_data.get('phone', '')}
            </p>
        </div>
        <div style="font-size: 13px; line-height: 1.6; color: #334155;">
            {cv_data.get('summary', 'Start typing your profile summary...')}
        </div>
    </div>
    """
    return html


def get_web_html(cv_data):
    """Generates an ultra-premium, full-page designer HTML resume optimized for PDF export."""
    theme = cv_data.get('template', 'Classic')
    
    themes = {
        "Classic": {
            "primary": "#0f172a", "secondary": "#64748b", "accent": "#f8fafc",
            "font_main": "'Inter', sans-serif", "font_head": "'Playfair Display', serif",
            "header_bg": "#ffffff", "border_color": "#0f172a"
        },
        "Formal": {
            "primary": "#1a365d", "secondary": "#2d3748", "accent": "#f7fafc",
            "font_main": "'Inter', sans-serif", "font_head": "'Inter', sans-serif",
            "header_bg": "#f8fafc", "border_color": "#1a365d"
        },
        "Colorful": {
            "primary": "#4338ca", "secondary": "#6366f1", "accent": "#f5f3ff",
            "font_main": "'Plus Jakarta Sans', sans-serif", "font_head": "'Plus Jakarta Sans', sans-serif",
            "header_bg": "#f5f3ff", "border_color": "#4338ca"
        }
    }
    t = themes.get(theme, themes["Classic"])

    # Pre-build sections with more "Space Consumption" (larger margins/paddings)
    summary_html = f'''
    <div class="section">
        <h2 class="section-title">Professional Executive Summary</h2>
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
                    <span class="job-title">{exp.get('job_title', '')}</span>
                    <span class="company-name">{exp.get('company', '')}</span>
                </div>
                <div class="exp-date">{exp.get('start_date', '')} — {exp.get('end_date', '')}</div>
            </div>
            <div class="exp-desc">{desc}</div>
        </div>
        """
    experience_html = f'''
    <div class="section">
        <h2 class="section-title">Professional Work History</h2>
        {experience_items}
    </div>
    ''' if experience_items else ''

    education_items = ""
    for edu in cv_data.get('education', []):
        education_items += f"""
        <div class="side-item">
            <div class="side-item-title">{edu.get('degree', '')}</div>
            <div class="side-item-sub">{edu.get('institution', '')}</div>
            <div class="side-item-meta">{edu.get('year', '')}</div>
        </div>
        """
    education_html = f'''
    <div class="side-section">
        <h3 class="side-title">Education</h3>
        {education_items}
    </div>
    ''' if education_items else ''

    skill_tags = "".join([f'<span>{s}</span>' for s in cv_data.get('skills', [])])
    skills_html = f'''
    <div class="side-section">
        <h3 class="side-title">Technical Expertise</h3>
        <div class="skill-cloud">{skill_tags}</div>
    </div>
    ''' if skill_tags else ''

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{cv_data.get('full_name', 'Professional_Resume')}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Playfair+Display:wght@700;900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: {t['primary']};
            --secondary: {t['secondary']};
            --accent: {t['accent']};
        }}
        * {{ box-sizing: border-box; -webkit-print-color-adjust: exact; }}
        
        @page {{
            size: A4;
            margin: 0;
        }}

        body {{
            background: #f1f5f9;
            font-family: {t['font_main']};
            color: #1e293b;
            margin: 0;
            padding: 40px 0;
            line-height: 1.8;
        }}

        .page {{
            width: 210mm;
            min-height: 297mm;
            margin: 0 auto;
            background: white;
            box-shadow: 0 40px 100px rgba(0,0,0,0.15);
            display: flex;
            flex-direction: column;
            position: relative;
        }}

        @media print {{
            body {{ background: white; padding: 0; }}
            .page {{ box-shadow: none; margin: 0; width: 100%; border: none; }}
            .no-print {{ display: none !important; }}
        }}

        /* Header - Full Width & Bold */
        header {{
            padding: 80px 80px;
            background: {t['header_bg']};
            border-bottom: 12px solid var(--primary);
            position: relative;
        }}
        header::after {{
            content: '';
            position: absolute;
            right: 80px;
            bottom: -12px;
            width: 150px;
            height: 12px;
            background: #cbd5e1;
        }}
        header h1 {{
            margin: 0;
            font-family: {t['font_head']};
            font-size: 64px;
            font-weight: 900;
            color: var(--primary);
            line-height: 1;
            letter-spacing: -3px;
            text-transform: uppercase;
        }}
        .header-meta {{
            margin-top: 25px;
            display: flex;
            gap: 30px;
            font-size: 16px;
            font-weight: 700;
            color: var(--secondary);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        /* Main Content Grid */
        .grid {{
            display: grid;
            grid-template-columns: 2fr 1fr;
            flex-grow: 1;
        }}

        /* Left Column */
        .main-col {{
            padding: 60px 50px 60px 80px;
        }}
        .section {{ margin-bottom: 60px; break-inside: avoid; }}
        .section-title {{
            font-size: 20px;
            font-weight: 900;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 2px;
            margin-bottom: 30px;
            display: flex;
            align-items: center;
            gap: 20px;
        }}
        .section-title::after {{
            content: '';
            flex-grow: 1;
            height: 2px;
            background: #f1f5f9;
        }}

        .summary-text {{ font-size: 16px; color: #334155; text-align: justify; }}
        
        .exp-item {{ margin-bottom: 40px; }}
        .exp-header {{ display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px; }}
        .exp-main {{ display: flex; flex-direction: column; }}
        .job-title {{ font-size: 22px; font-weight: 800; color: #0f172a; line-height: 1.2; }}
        .company-name {{ font-size: 17px; font-weight: 600; color: var(--primary); margin-top: 5px; }}
        .exp-date {{ font-size: 14px; font-weight: 800; color: var(--secondary); white-space: nowrap; }}
        .exp-desc {{ font-size: 15.5px; color: #475569; line-height: 1.7; }}

        /* Right Column (Sidebar) */
        .side-col {{
            background: #f8fafc;
            padding: 60px 60px 60px 40px;
            border-left: 1px solid #e2e8f0;
        }}
        .side-section {{ margin-bottom: 50px; }}
        .side-title {{
            font-size: 16px;
            font-weight: 900;
            color: var(--primary);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 25px;
        }}
        .side-item {{ margin-bottom: 25px; }}
        .side-item-title {{ font-size: 16px; font-weight: 700; color: #0f172a; }}
        .side-item-sub {{ font-size: 15px; color: var(--secondary); font-weight: 500; margin-top: 2px; }}
        .side-item-meta {{ font-size: 13px; color: #94a3b8; font-weight: 600; margin-top: 4px; }}

        .skill-cloud {{ display: flex; flex-wrap: wrap; gap: 10px; }}
        .skill-cloud span {{
            background: white;
            color: var(--primary);
            padding: 8px 16px;
            border-radius: 8px;
            font-size: 14px;
            font-weight: 700;
            border: 1px solid #e2e8f0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
        }}

        /* Floating Tool Bar */
        .toolbar {{
            position: fixed;
            bottom: 40px;
            left: 50%;
            transform: translateX(-50%);
            background: #0f172a;
            padding: 12px 24px;
            border-radius: 100px;
            display: flex;
            gap: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.4);
            z-index: 9999;
        }}
        .tool-btn {{
            background: #6366f1;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 100px;
            font-weight: 800;
            font-size: 15px;
            cursor: pointer;
            transition: all 0.2s;
        }}
        .tool-btn:hover {{ transform: translateY(-2px); box-shadow: 0 10px 20px rgba(99, 102, 241, 0.4); }}
    </style>
</head>
<body>
    <div class="toolbar no-print">
        <button class="tool-btn" onclick="window.print()">📥 SAVE AS PDF / PRINT</button>
    </div>
    <div class="page">
        <header>
            <h1>{cv_data.get('full_name', 'Your Name')}</h1>
            <div class="header-meta">
                <span>{cv_data.get('email', '')}</span>
                <span>{cv_data.get('phone', '')}</span>
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
    <script>
        // Auto-trigger print dialog for a seamless "Save as PDF" experience
        window.onload = function() {{
            setTimeout(function() {{
                window.print();
            }}, 500);
        }};
    </script>
</body>
</html>
"""
    return html
