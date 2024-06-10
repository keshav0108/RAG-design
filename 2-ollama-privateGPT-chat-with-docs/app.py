from flask import Flask, request, jsonify
import os
import shutil
from ingest import load_documents  # Ensure this import is correct
from privateGPT import main  # Ensure this import is correct

app = Flask(__name__)

# POST /rag/ingest
@app.route('/rag/ingest', methods=['POST'])
def ingest_documents():
    try:
        source_dir = request.json.get('source_dir', 'source_documents')
        load_documents(source_dir)
        return jsonify({"message": "Documents ingested successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# DELETE /rag/resetDB
@app.route('/rag/resetDB', methods=['DELETE'])
def reset_db():
    try:
        if os.path.exists('db'):
            shutil.rmtree('db')
        if os.path.exists('__pycache__'):
            shutil.rmtree('__pycache__')
        return jsonify({"message": "Database reset successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# POST /rag/source_documents (Optional)
@app.route('/rag/source_documents', methods=['POST'])
def source_documents():
    try:
        # Implement the logic to pull documents from cloud storage or other sources
        # For example:
        # download_from_cloud_storage()
        return jsonify({"message": "Documents sourced successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

# POST /rag/chat
@app.route('/rag/chat', methods=['POST'])
def chat():
    data = request.json
    prompt = data.get('prompt')
    try:
        response = main(prompt)
        return jsonify({"response": response}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
