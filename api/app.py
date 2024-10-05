from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import tiktoken
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        model_name = request.form.get('model')
        ignore_suffixes = request.form.get('ignore_suffixes', '')
        ignore_folders = request.form.get('ignore_folders', '')
        files = request.files.getlist('files')
        
        if not files or not model_name:
            return jsonify({'error': 'Missing files or model selection'}), 400
        
        # Process the uploaded files in-memory
        result = process_files(files, model_name, ignore_suffixes, ignore_folders)
        
        return jsonify(result)
    else:
        return render_template('index.html')

def process_files(uploaded_files, model_name, ignore_suffixes, ignore_folders):
    import os
    import re

    file_size_limit = 500 * 1024  # 500 KB size limit for files to process
    total_content = []
    output_messages = []

    # Parse the ignore lists
    ignore_suffixes_list = [suffix.strip().lower() for suffix in re.split(r'[\n,]+', ignore_suffixes) if suffix.strip()]
    ignore_folders_list = [folder.strip().lower().strip('/\\') for folder in re.split(r'[\n,]+', ignore_folders) if folder.strip()]

    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        output_messages.append(f"Model '{model_name}' not recognized. Using default encoding.\n")
        encoding = tiktoken.get_encoding('cl100k_base')

    for file in uploaded_files:
        filename = file.filename.lower()
        
        # Stringent check for .git files and folders
        if '.git' in filename.split(os.sep) or filename.endswith('.git'):
            output_messages.append(f"Skipping .git file/folder: {filename}\n")
            continue

        # Check if the file is in any ignored folder
        if any(ignored_folder in filename.split(os.sep) for ignored_folder in ignore_folders_list):
            output_messages.append(f"Skipping file in ignored folder: {filename}\n")
            continue

        # Check file extension
        if any(filename.endswith(suffix) for suffix in ignore_suffixes_list):
            output_messages.append(f"Skipping file (ignored suffix): {filename}\n")
            continue

        # Check the file size before reading
        file.seek(0, os.SEEK_END)  # Move to the end of the file
        size = file.tell()
        file.seek(0)  # Reset to the beginning of the file
        if size > file_size_limit:
            output_messages.append(f"Skipping file (too large): {filename}\n")
            continue

        try:
            content_text = f"\n\n### {filename} ###\n"
            file_data = file.read().decode('utf-8', errors='ignore')
            total_content.append(content_text + file_data)
        except Exception as e:
            output_messages.append(f"Error reading {filename}: {e}\n")

    output_messages.append("Finished processing files.\nNote: Files over 500KB are ignored.\n")
    combined_text = ''.join(total_content)
    token_count = len(encoding.encode(combined_text))

    return {
        'output_messages': ''.join(output_messages),
        'file_contents': combined_text,
        'token_count': token_count
    }

if __name__ == '__main__':
    app.run(debug=True)
