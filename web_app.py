from flask import Flask, render_template, request, redirect, url_for, jsonify, Response
import database
import pdf_generator
import os

app = Flask(__name__)

# Initialize database
database.init_db()

@app.route('/')
def dashboard():
    print("Fetching CVs from Supabase...")
    cvs = database.get_all_cvs()
    return render_template('dashboard.html', cvs=cvs)

@app.route('/editor')
@app.route('/editor/<int:cv_id>')
def editor(cv_id=None):
    cv_data = {}
    if cv_id:
        print(f"Loading CV ID: {cv_id}")
        cv_data = database.get_cv(cv_id)
        if not cv_data:
            print(f"CV {cv_id} not found, redirecting...")
            return redirect(url_for('dashboard'))
    return render_template('editor.html', cv=cv_data, cv_id=cv_id)

@app.route('/save', methods=['POST'])
def save():
    data = request.json
    print(f"Saving CV: {data.get('title')}")
    cv_id = database.save_cv(data)
    if cv_id:
        return jsonify({'status': 'success', 'cv_id': cv_id})
    return jsonify({'status': 'error', 'message': 'Failed to save to database'}), 500

@app.route('/preview/<int:cv_id>')
def preview(cv_id):
    cv_data = database.get_cv(cv_id)
    if not cv_data:
        return "CV not found", 404
    html = pdf_generator.get_web_html(cv_data)
    return html

@app.route('/delete/<int:cv_id>', methods=['POST'])
def delete(cv_id):
    print(f"Deleting CV ID: {cv_id}")
    success = database.delete_cv(cv_id)
    if success:
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 500

if __name__ == '__main__':
    # Run on all interfaces so it can be accessed from mobile/other laptops
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting server on port {port}...")
    app.run(host='0.0.0.0', port=port, debug=True)
