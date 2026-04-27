import sys
import os
import tempfile
import webbrowser
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QLabel, QStackedWidget, QListWidget, QListWidgetItem,
    QLineEdit, QTextEdit, QFormLayout, QScrollArea, QTabWidget, QGroupBox,
    QMessageBox, QTextBrowser, QSplitter, QComboBox, QFrame
)
from PyQt6.QtCore import Qt, QSize

import database
from ui_styles import MAIN_STYLE
from pdf_generator import get_qt_html, get_web_html

class Sidebar(QFrame):
    def __init__(self, main_window):
        super().__init__()
        self.setObjectName("Sidebar")
        self.main_window = main_window
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        logo = QLabel("RESUME PRO")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo)
        layout.addSpacing(20)

        self.btn_home = QPushButton("  🏠  Dashboard")
        self.btn_home.setProperty("active", "true")
        self.btn_home.clicked.connect(self.main_window.open_dashboard)
        
        self.btn_new = QPushButton("  ➕  Create New")
        self.btn_new.clicked.connect(self.main_window.open_new_editor)

        layout.addWidget(self.btn_home)
        layout.addWidget(self.btn_new)
        
        layout.addStretch()
        
        settings = QPushButton("  ⚙️  Settings")
        layout.addWidget(settings)
        layout.addSpacing(20)

    def set_active(self, page_name):
        self.btn_home.setProperty("active", "true" if page_name == "home" else "false")
        self.btn_new.setProperty("active", "true" if page_name == "new" else "false")
        self.style().unpolish(self.btn_home)
        self.style().polish(self.btn_home)
        self.style().unpolish(self.btn_new)
        self.style().polish(self.btn_new)

class ResumeCard(QFrame):
    def __init__(self, cv_data, on_edit, on_export, on_delete):
        super().__init__()
        self.setObjectName("ResumeCard")
        self.setProperty("class", "ResumeCard")
        self.cv_id = cv_data['id']
        
        layout = QHBoxLayout(self)
        
        info_layout = QVBoxLayout()
        title = QLabel(cv_data['title'])
        title.setObjectName("CardTitle")
        
        meta = QLabel(f"👤 {cv_data.get('full_name', 'Unnamed')}  •  📄 Professional Resume")
        meta.setObjectName("CardMeta")
        
        info_layout.addWidget(title)
        info_layout.addWidget(meta)
        layout.addLayout(info_layout)
        
        layout.addStretch()
        
        actions = QHBoxLayout()
        
        edit_btn = QPushButton("✎ Edit")
        edit_btn.setObjectName("SecondaryBtn")
        edit_btn.clicked.connect(lambda: on_edit(self.cv_id))
        
        export_btn = QPushButton("📥 Download PDF")
        export_btn.setObjectName("PrimaryBtn")
        export_btn.clicked.connect(lambda: on_export(self.cv_id))
        
        delete_btn = QPushButton("🗑")
        delete_btn.setObjectName("DangerBtn")
        delete_btn.setFixedWidth(40)
        delete_btn.clicked.connect(lambda: on_delete(self.cv_id))
        
        actions.addWidget(edit_btn)
        actions.addWidget(export_btn)
        actions.addWidget(delete_btn)
        layout.addLayout(actions)

class DashboardPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(50, 50, 50, 50)
        self.layout.setSpacing(30)

        header = QHBoxLayout()
        title_box = QVBoxLayout()
        h1 = QLabel("Your Resumes")
        h1.setProperty("class", "h1")
        sub = QLabel("Elite-quality designer resumes for your career")
        sub.setStyleSheet("color: #64748b; font-size: 16px;")
        title_box.addWidget(h1)
        title_box.addWidget(sub)
        header.addLayout(title_box)
        
        header.addStretch()
        
        new_btn = QPushButton("+ Create New")
        new_btn.setObjectName("PrimaryBtn")
        new_btn.setMinimumHeight(50)
        new_btn.clicked.connect(self.main_window.open_new_editor)
        header.addWidget(new_btn)
        self.layout.addLayout(header)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("background: transparent; border: none;")
        
        self.container = QWidget()
        self.container.setObjectName("CardContainer")
        self.card_layout = QVBoxLayout(self.container)
        self.card_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.card_layout.setSpacing(15)
        
        self.scroll.setWidget(self.container)
        self.layout.addWidget(self.scroll)

    def load_cvs(self):
        for i in reversed(range(self.card_layout.count())): 
            self.card_layout.itemAt(i).widget().setParent(None)
            
        cvs = database.get_all_cvs()
        if not cvs:
            empty = QLabel("No resumes yet. Start by creating your first elite CV!")
            empty.setAlignment(Qt.AlignmentFlag.AlignCenter)
            empty.setStyleSheet("color: #94a3b8; font-size: 18px; margin-top: 100px;")
            self.card_layout.addWidget(empty)
            return

        for cv in cvs:
            card = ResumeCard(cv, self.main_window.open_editor, self.export_cv, self.delete_cv)
            self.card_layout.addWidget(card)

    def export_cv(self, cv_id):
        cv_data = database.get_cv(cv_id)
        if not cv_data: return
        html_content = get_web_html(cv_data)
        fd, path = tempfile.mkstemp(suffix=".html")
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            f.write(html_content)
        webbrowser.open('file://' + os.path.realpath(path))

    def delete_cv(self, cv_id):
        reply = QMessageBox.question(self, 'Delete Resume', 'Are you sure you want to delete this elite resume?',
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            database.delete_cv(cv_id)
            self.load_cvs()

class EditorPage(QWidget):
    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.cv_id = None
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(40, 40, 40, 40)
        
        # Studio Header
        header = QHBoxLayout()
        back_btn = QPushButton("← Back")
        back_btn.setObjectName("SecondaryBtn")
        back_btn.clicked.connect(self.main_window.open_dashboard)
        
        self.save_btn = QPushButton("💾 Save")
        self.save_btn.setObjectName("SecondaryBtn")
        self.save_btn.clicked.connect(lambda: self.save_cv(silent=False))

        self.print_btn = QPushButton("📥 Download PDF")
        self.print_btn.setObjectName("PrimaryBtn")
        self.print_btn.setMinimumWidth(160)
        self.print_btn.clicked.connect(self.print_cv)
        
        header.addWidget(back_btn)
        header.addStretch()
        header.addWidget(self.save_btn)
        header.addWidget(self.print_btn)
        self.layout.addLayout(header)
        
        self.layout.addSpacing(20)
        
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.layout.addWidget(self.splitter)
        
        self.tabs = QTabWidget()
        self.splitter.addWidget(self.tabs)
        
        preview_panel = QFrame()
        preview_panel.setStyleSheet("background: #e2e8f0; border-radius: 20px; padding: 2px;")
        prev_layout = QVBoxLayout(preview_panel)
        
        prev_header = QLabel("STUDIO PREVIEW")
        prev_header.setProperty("class", "section-header")
        prev_header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        prev_layout.addWidget(prev_header)
        
        self.preview_browser = QTextBrowser()
        self.preview_browser.setStyleSheet("border-radius: 15px; border: none; background: white;")
        prev_layout.addWidget(self.preview_browser)
        
        self.splitter.addWidget(preview_panel)
        self.splitter.setSizes([700, 500])
        
        self.setup_tabs()

    def setup_tabs(self):
        gen_tab = QWidget()
        gen_lay = QFormLayout(gen_tab)
        gen_lay.setContentsMargins(30, 30, 30, 30)
        gen_lay.setSpacing(20)
        
        self.inp_title = QLineEdit()
        self.inp_template = QComboBox()
        self.inp_template.addItems(["Classic", "Formal", "Colorful"])
        self.inp_template.currentIndexChanged.connect(self.update_preview)

        self.inp_name = QLineEdit()
        self.inp_email = QLineEdit()
        self.inp_phone = QLineEdit()
        self.inp_address = QLineEdit()
        self.inp_linkedin = QLineEdit()
        self.inp_summary = QTextEdit()
        
        for w in [self.inp_name, self.inp_email, self.inp_phone, self.inp_address, self.inp_linkedin]:
            w.textChanged.connect(self.update_preview)
        self.inp_summary.textChanged.connect(self.update_preview)
        
        gen_lay.addRow(QLabel("RESUME SETTINGS"), QLabel(""))
        gen_lay.addRow("Document Title", self.inp_title)
        gen_lay.addRow("Visual Theme", self.inp_template)
        gen_lay.addRow(QLabel("PERSONAL DETAILS"), QLabel(""))
        gen_lay.addRow("Full Name", self.inp_name)
        gen_lay.addRow("Email Address", self.inp_email)
        gen_lay.addRow("Phone Number", self.inp_phone)
        gen_lay.addRow("Location", self.inp_address)
        gen_lay.addRow("LinkedIn", self.inp_linkedin)
        gen_lay.addRow("Professional Profile", self.inp_summary)
        
        self.tabs.addTab(gen_tab, "Basic Info")

        self.exp_tab = QWidget()
        exp_lay = QVBoxLayout(self.exp_tab)
        add_exp = QPushButton("+ Add Work Experience")
        add_exp.setObjectName("SecondaryBtn")
        add_exp.clicked.connect(self.add_experience_widget)
        exp_lay.addWidget(add_exp)
        
        self.exp_scroll = QScrollArea()
        self.exp_scroll.setWidgetResizable(True)
        self.exp_cont = QWidget()
        self.exp_cont_lay = QVBoxLayout(self.exp_cont)
        self.exp_scroll.setWidget(self.exp_cont)
        exp_lay.addWidget(self.exp_scroll)
        self.exp_widgets = []
        self.tabs.addTab(self.exp_tab, "Experience")

        self.edu_tab = QWidget()
        edu_lay = QVBoxLayout(self.edu_tab)
        add_edu = QPushButton("+ Add Education")
        add_edu.setObjectName("SecondaryBtn")
        add_edu.clicked.connect(self.add_education_widget)
        edu_lay.addWidget(add_edu)
        
        self.edu_scroll = QScrollArea()
        self.edu_scroll.setWidgetResizable(True)
        self.edu_cont = QWidget()
        self.edu_cont_lay = QVBoxLayout(self.edu_cont)
        self.edu_scroll.setWidget(self.edu_cont)
        edu_lay.addWidget(self.edu_scroll)
        self.edu_widgets = []
        self.tabs.addTab(self.edu_tab, "Education")

        skill_tab = QWidget()
        sk_lay = QVBoxLayout(skill_tab)
        sk_lay.setContentsMargins(30,30,30,30)
        sk_lay.addWidget(QLabel("SKILLS & EXPERTISE"))
        self.inp_skills = QTextEdit()
        self.inp_skills.setPlaceholderText("Enter skills separated by commas...")
        self.inp_skills.textChanged.connect(self.update_preview)
        sk_lay.addWidget(self.inp_skills)
        self.tabs.addTab(skill_tab, "Skills")

    def update_preview(self):
        cv_data = self.get_current_data()
        html = get_qt_html(cv_data)
        self.preview_browser.setHtml(html)

    def get_current_data(self):
        cv_data = {
            'template': self.inp_template.currentText(),
            'full_name': self.inp_name.text().strip(),
            'email': self.inp_email.text().strip(),
            'phone': self.inp_phone.text().strip(),
            'address': self.inp_address.text().strip(),
            'linkedin': self.inp_linkedin.text().strip(),
            'summary': self.inp_summary.toPlainText().strip(),
            'experience': [], 'education': [], 'skills': []
        }
        for w in self.exp_widgets:
            cv_data['experience'].append({
                'job_title': w['job_title'].text(), 'company': w['company'].text(),
                'start_date': w['start'].text(), 'end_date': w['end'].text(),
                'description': w['desc'].toPlainText()
            })
        for w in self.edu_widgets:
            cv_data['education'].append({
                'degree': w['degree'].text(), 'institution': w['inst'].text(), 'year': w['year'].text()
            })
        cv_data['skills'] = [s.strip() for s in self.inp_skills.toPlainText().split(',') if s.strip()]
        return cv_data

    def add_experience_widget(self, data=None):
        gb = QGroupBox("Work Entry")
        lay = QFormLayout(gb)
        jt, comp, st, en, ds = QLineEdit(), QLineEdit(), QLineEdit(), QLineEdit(), QTextEdit()
        for w in [jt, comp, st, en]: w.textChanged.connect(self.update_preview)
        ds.textChanged.connect(self.update_preview)
        if data and isinstance(data, dict):
            jt.setText(data.get('job_title', '')); comp.setText(data.get('company', ''))
            st.setText(data.get('start_date', '')); en.setText(data.get('end_date', ''))
            ds.setPlainText(data.get('description', ''))
        lay.addRow("Position", jt); lay.addRow("Company", comp)
        lay.addRow("Start Date", st); lay.addRow("End Date", en); lay.addRow("Summary", ds)
        rem = QPushButton("Remove Entry")
        rem.setObjectName("DangerBtn")
        rem.clicked.connect(lambda: self.remove_widget(gb, self.exp_widgets, self.exp_cont_lay))
        lay.addRow(rem)
        self.exp_cont_lay.addWidget(gb)
        self.exp_widgets.append({'gb': gb, 'job_title': jt, 'company': comp, 'start': st, 'end': en, 'desc': ds})
        self.update_preview()

    def add_education_widget(self, data=None):
        gb = QGroupBox("Education Entry")
        lay = QFormLayout(gb)
        dg, inst, yr = QLineEdit(), QLineEdit(), QLineEdit()
        for w in [dg, inst, yr]: w.textChanged.connect(self.update_preview)
        if data and isinstance(data, dict):
            dg.setText(data.get('degree', '')); inst.setText(data.get('institution', '')); yr.setText(data.get('year', ''))
        lay.addRow("Degree", dg); lay.addRow("University", inst); lay.addRow("Year", yr)
        rem = QPushButton("Remove Entry")
        rem.setObjectName("DangerBtn")
        rem.clicked.connect(lambda: self.remove_widget(gb, self.edu_widgets, self.edu_cont_lay))
        lay.addRow(rem)
        self.edu_cont_lay.addWidget(gb)
        self.edu_widgets.append({'gb': gb, 'degree': dg, 'inst': inst, 'year': yr})
        self.update_preview()

    def remove_widget(self, gb, widget_list, layout):
        for item in widget_list:
            if item['gb'] == gb:
                widget_list.remove(item); break
        layout.removeWidget(gb); gb.deleteLater()
        self.update_preview()

    def clear_editor(self):
        self.cv_id = None
        for w in [self.inp_title, self.inp_name, self.inp_email, self.inp_phone, self.inp_address, self.inp_linkedin]: w.clear()
        self.inp_summary.clear(); self.inp_skills.clear(); self.inp_template.setCurrentIndex(0)
        for w in self.exp_widgets: w['gb'].deleteLater()
        for w in self.edu_widgets: w['gb'].deleteLater()
        self.exp_widgets, self.edu_widgets = [], []
        self.update_preview()

    def load_cv(self, cv_id):
        self.clear_editor()
        self.cv_id = cv_id
        cv = database.get_cv(cv_id)
        if not cv: return
        self.inp_title.setText(cv.get('title', ''))
        idx = self.inp_template.findText(cv.get('template', 'Classic'))
        if idx >= 0: self.inp_template.setCurrentIndex(idx)
        self.inp_name.setText(cv.get('full_name', ''))
        self.inp_email.setText(cv.get('email', ''))
        self.inp_phone.setText(cv.get('phone', ''))
        self.inp_address.setText(cv.get('address', ''))
        self.inp_linkedin.setText(cv.get('linkedin', ''))
        self.inp_summary.setPlainText(cv.get('summary', ''))
        for exp in cv.get('experience', []): self.add_experience_widget(exp)
        for edu in cv.get('education', []): self.add_education_widget(edu)
        if cv.get('skills'): self.inp_skills.setPlainText(", ".join(cv.get('skills')))
        self.update_preview()

    def save_cv(self, silent=False):
        try:
            data = self.get_current_data()
            data['id'], data['title'] = self.cv_id, self.inp_title.text().strip() or 'Untitled Resume'
            self.cv_id = database.save_cv(data)
            if not silent:
                QMessageBox.information(self, "Saved", "Your progress has been securely saved.")
            return True
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save: {str(e)}")
            return False

    def print_cv(self):
        if self.save_cv(silent=True):
            cv_data = database.get_cv(self.cv_id)
            if not cv_data: return
            html_content = get_web_html(cv_data)
            fd, path = tempfile.mkstemp(suffix=".html")
            with os.fdopen(fd, 'w', encoding='utf-8') as f:
                f.write(html_content)
            webbrowser.open('file://' + os.path.realpath(path))

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Resume Pro Studio")
        self.resize(1350, 950)
        self.setStyleSheet(MAIN_STYLE)
        database.init_db()
        
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        self.main_layout = QHBoxLayout(main_widget)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        
        self.sidebar = Sidebar(self)
        self.main_layout.addWidget(self.sidebar)
        
        self.content_stack = QStackedWidget()
        self.content_stack.setObjectName("ContentArea")
        self.main_layout.addWidget(self.content_stack)
        
        self.dash = DashboardPage(self)
        self.edit = EditorPage(self)
        self.content_stack.addWidget(self.dash)
        self.content_stack.addWidget(self.edit)
        
        self.open_dashboard()

    def open_dashboard(self):
        self.sidebar.set_active("home")
        self.dash.load_cvs()
        self.content_stack.setCurrentWidget(self.dash)

    def open_new_editor(self):
        self.sidebar.set_active("new")
        self.edit.clear_editor()
        self.content_stack.setCurrentWidget(self.edit)

    def open_editor(self, cv_id):
        self.sidebar.set_active("none")
        self.edit.load_cv(cv_id)
        self.content_stack.setCurrentWidget(self.edit)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    win = App()
    win.show()
    sys.exit(app.exec())