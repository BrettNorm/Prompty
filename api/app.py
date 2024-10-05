from flask import Flask, render_template, request, jsonify
import os
import threading
import tiktoken
import shutil
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure the upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        model_name = request.form.get('model')
        files = request.files.getlist('files')
        
        if not files or not model_name:
            return jsonify({'error': 'Missing files or model selection'}), 400
        
        # Create a unique directory for this upload session
        session_folder = os.path.join(app.config['UPLOAD_FOLDER'], 'session')
        if os.path.exists(session_folder):
            shutil.rmtree(session_folder)
        os.makedirs(session_folder, exist_ok=True)
        
        # Save all uploaded files
        for file in files:
            # Preserve directory structure
            file_path = os.path.join(session_folder, file.filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            file.save(file_path)
        
        # Process the uploaded files
        result = process_folder(session_folder, model_name)
        
        # Clean up uploaded files
        shutil.rmtree(session_folder)
        
        return jsonify(result)
    else:
        return render_template('index.html')

def process_folder(folder_path, model_name):
    file_size_limit = 500 * 1024  # 500 KB size limit for files to process
    total_content = []
    output_messages = []
    file_contents = ""

    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        output_messages.append(f"Model '{model_name}' not recognized. Using default encoding.\n")
        encoding = tiktoken.get_encoding('cl100k_base')

    # Recursively read all files in the folder
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith((
                '.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.htm', '.css', '.scss',
                '.sass', '.less', '.md', '.txt', '.json', '.yaml', '.yml', '.ini', '.cfg',
                '.xml', '.xhtml', '.log', '.conf', '.toml', '.csv', '.tsv', '.properties',
                '.env', '.c', '.cpp', '.h', '.java', '.cs', '.rb', '.swift', '.php', '.sh', '.bat',
                '.pl', '.r', '.go', '.rs', '.dockerfile'
            )):
                file_path = os.path.join(root, file)
                try:
                    # Check the file size before reading
                    if os.path.getsize(file_path) > file_size_limit:
                        output_messages.append(f"Skipping file (too large): {file_path}\n")
                        continue

                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content_text = f"\n\n### {file} ###\n"
                        file_contents += content_text
                        file_data = ""
                        for line_number, line in enumerate(f, start=1):
                            # Check for SVG path data
                            if ' d="' in line or 'd="' in line:
                                file_data += f"[Skipped SVG path data at line {line_number}]\n"
                            else:
                                file_data += line
                        file_contents += file_data
                        total_content.append(content_text + file_data)
                except Exception as e:
                    output_messages.append(f"Error reading {file_path}: {e}\n")
    
    output_messages.append("Finished processing folder.\n")
    combined_text = ''.join(total_content)
    token_count = len(encoding.encode(combined_text))

    return {
        'output_messages': ''.join(output_messages),
        'file_contents': combined_text,
        'token_count': token_count
    }

if __name__ == '__main__':
    app.run(debug=True)
