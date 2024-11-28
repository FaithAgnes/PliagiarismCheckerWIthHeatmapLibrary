from flask import Flask, request, jsonify, send_file
import os
from mymodule import plagiarism_checker, visualize_heatmap

app = Flask(__name__)

DOCUMENTS_DIR = '/app/documents'  # This will be the mounted directory

@app.route('/favicon.ico')
def favicon():
    return '', 204  # Serve an empty favicon

@app.route('/')
def home():
    return 'Welcome to the Plagiarism Checker API. Use /check_plagiarism to check documents.'

@app.route('/check_plagiarism', methods=['POST'])
def check_plagiarism():
    if 'doc1' not in request.files or 'doc2' not in request.files:
        return jsonify({'error': 'Please upload both documents'}), 400

    doc1 = request.files['doc1']
    doc2 = request.files['doc2']

    # Save uploaded files to a temporary location within the mounted directory
    doc1_path = os.path.join(DOCUMENTS_DIR, doc1.filename)
    doc2_path = os.path.join(DOCUMENTS_DIR, doc2.filename)
    doc1.save(doc1_path)
    doc2.save(doc2_path)

    try:
        # Call plagiarism checker function
        score, heatmap_data = plagiarism_checker(doc1_path, doc2_path)

        # Save the heatmap as an image
        save_path = "/tmp/heatmap.png"
        if heatmap_data:
            visualize_heatmap(heatmap_data, doc1_name=doc1.filename, doc2_name=doc2.filename, save_path=save_path)

        # Return result with score and heatmap
        return jsonify({'score': score, 'heatmap_url': '/download_heatmap'}), 200

    finally:
        # Remove temporary files from the container's perspective
        os.remove(doc1_path)
        os.remove(doc2_path)

@app.route('/download_heatmap', methods=['GET'])
def download_heatmap():
    return send_file("/tmp/heatmap.png", mimetype='image/png', as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)