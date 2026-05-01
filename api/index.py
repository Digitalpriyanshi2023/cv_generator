import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, request, jsonify, Response, send_from_directory
import database
import pdf_generator
from flask_cors import CORS

app = Flask(__name__, static_folder='../public', static_url_path='')
CORS(app) 

# Initialize database on startup
database.init_db()

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "database": "sqlite"})

@app.route('/api/cvs', methods=['GET'])
def get_cvs():
    cvs = database.get_all_cvs()
    return jsonify(cvs)

@app.route('/api/cvs/<int:cv_id>', methods=['GET'])
def get_cv(cv_id):
    cv_data = database.get_cv(cv_id)
    if not cv_data:
        return jsonify({'error': 'CV not found'}), 404
    return jsonify(cv_data)

@app.route('/api/cvs', methods=['POST'])
def save_cv():
    data = request.json
    cv_id = database.save_cv(data)
    if cv_id:
        return jsonify({'status': 'success', 'cv_id': cv_id})
    return jsonify({'status': 'error', 'message': 'Failed to save to database'}), 500

@app.route('/api/cvs/<int:cv_id>', methods=['DELETE'])
def delete_cv(cv_id):
    success = database.delete_cv(cv_id)
    if success:
        return jsonify({'status': 'success'})
    return jsonify({'status': 'error'}), 500

@app.route('/api/cvs/preview-temp', methods=['POST'])
def preview_temp():
    data = request.json
    html = pdf_generator.get_web_html(data)
    return html

@app.route('/api/cvs/<int:cv_id>/preview')
def preview_cv(cv_id):
    cv_data = database.get_cv(cv_id)
    if not cv_data:
        return "CV not found", 404
    html = pdf_generator.get_web_html(cv_data)
    return html

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

