from flask import Flask, request, jsonify, Response
import database
import pdf_generator
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Enable CORS for frontend interaction

# Initialize database
database.init_db()

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

# Vercel handles static files, so we don't need index() or serve_static() here.
# But for local development, you might still want them. 
# However, to avoid 404s on Vercel, it's better to let Vercel handle routing.

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
