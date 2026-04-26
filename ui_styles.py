MAIN_STYLE = """
/* Global Config */
QMainWindow {
    background-color: #f1f5f9;
}

QWidget {
    font-family: 'Inter', 'Segoe UI', sans-serif;
    color: #334155;
}

/* Sidebar Styling */
#Sidebar {
    background-color: #0f172a;
    min-width: 240px;
    max-width: 240px;
    border-right: 1px solid #1e293b;
}

#Sidebar QLabel {
    color: #f8fafc;
    padding: 20px;
    font-weight: 800;
    font-size: 20px;
}

#Sidebar QPushButton {
    background-color: transparent;
    color: #94a3b8;
    text-align: left;
    padding: 15px 25px;
    border-radius: 0;
    font-weight: 500;
    font-size: 14px;
}

#Sidebar QPushButton:hover {
    background-color: #1e293b;
    color: #f8fafc;
}

#Sidebar QPushButton[active="true"] {
    background-color: #334155;
    color: #ffffff;
    border-left: 4px solid #6366f1;
}

/* Content Area */
#ContentArea {
    background-color: #f8fafc;
}

QLabel.h1 {
    font-size: 36px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -1px;
}

QLabel.section-header {
    font-size: 14px;
    font-weight: 700;
    color: #6366f1;
    text-transform: uppercase;
    letter-spacing: 1px;
}

/* Resume Cards */
#CardContainer {
    background-color: transparent;
}

.ResumeCard {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 20px;
}

.ResumeCard:hover {
    border-color: #6366f1;
    background-color: #ffffff;
}

.ResumeCard QLabel#CardTitle {
    font-size: 18px;
    font-weight: 700;
    color: #1e293b;
}

.ResumeCard QLabel#CardMeta {
    font-size: 13px;
    color: #64748b;
}

/* Modern Buttons */
QPushButton#PrimaryBtn {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #6366f1, stop:1 #8b5cf6);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 24px;
    font-weight: 700;
    font-size: 14px;
}

QPushButton#PrimaryBtn:hover {
    background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #4f46e5, stop:1 #7c3aed);
}

QPushButton#SecondaryBtn {
    background-color: #ffffff;
    color: #475569;
    border: 1px solid #e2e8f0;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 600;
}

QPushButton#SecondaryBtn:hover {
    background-color: #f8fafc;
    border-color: #cbd5e1;
}

QPushButton#DangerBtn {
    background-color: #fef2f2;
    color: #ef4444;
    border: 1px solid #fee2e2;
    border-radius: 8px;
    padding: 8px 16px;
    font-weight: 600;
}

QPushButton#DangerBtn:hover {
    background-color: #fee2e2;
}

/* Editor Specifics */
QTabWidget::pane {
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    background: #ffffff;
}

QTabBar::tab {
    background: transparent;
    color: #64748b;
    padding: 15px 30px;
    font-weight: 700;
    font-size: 13px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

QTabBar::tab:selected {
    color: #6366f1;
    border-bottom: 3px solid #6366f1;
}

/* Form Elements */
QLineEdit, QTextEdit, QComboBox {
    border: 2px solid #f1f5f9;
    border-radius: 10px;
    padding: 12px;
    background-color: #f8fafc;
    font-size: 14px;
    color: #1e293b;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border-color: #e2e8f0;
    background-color: #ffffff;
    border: 2px solid #6366f1;
}

/* Group Boxes */
QGroupBox {
    border: 1px solid #f1f5f9;
    border-radius: 16px;
    background-color: #ffffff;
    margin-top: 25px;
    padding: 25px;
    font-weight: 800;
}

/* ScrollBar */
QScrollBar:vertical {
    border: none;
    background: transparent;
    width: 10px;
}

QScrollBar::handle:vertical {
    background: #e2e8f0;
    border-radius: 5px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #cbd5e1;
}
"""
