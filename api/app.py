from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import tiktoken

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        model_name = request.form.get('model')
        files = request.files.getlist('files')
        
        if not files or not model_name:
            return jsonify({'error': 'Missing files or model selection'}), 400
        
        # Process the uploaded files in-memory
        result = process_files(files, model_name)
        
        return jsonify(result)
    else:
        return render_template('index.html')

def process_files(uploaded_files, model_name):
    file_size_limit = 500 * 1024  # 500 KB size limit for files to process
    total_content = []
    output_messages = []
    
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        output_messages.append(f"Model '{model_name}' not recognized. Using default encoding.\n")
        encoding = tiktoken.get_encoding('cl100k_base')
    
    for file in uploaded_files:
        filename = file.filename  # Use file.filename directly
        # Check file extension
        if filename.lower().endswith((
            '.py', '.js', '.jsx', '.ts', '.tsx', '.html', '.htm', '.css', '.scss',
            '.sass', '.less', '.md', '.txt', '.json', '.yaml', '.yml', '.ini', '.cfg',
            '.xml', '.xhtml', '.log', '.conf', '.toml', '.csv', '.tsv', '.properties',
            '.env', '.c', '.cpp', '.h', '.java', '.cs', '.rb', '.swift', '.php', '.sh', '.bat',
            '.pl', '.r', '.go', '.rs', '.dockerfile'
        )):
            # Check the file size before reading
            file.seek(0, 2)  # Move to the end of the file
            size = file.tell()
            file.seek(0)  # Reset to the beginning of the file
            if size > file_size_limit:
                output_messages.append(f"Skipping file (too large): {filename}\n")
                continue

            try:
                content_text = f"\n\n### {filename} ###\n"
                file_data = ""
                for line_number, line in enumerate(file.stream.readlines(), start=1):
                    line = line.decode('utf-8', errors='ignore')
                    # Check for SVG path data
                    if ' d="' in line or 'd="' in line:
                        file_data += f"[Skipped SVG path data at line {line_number}]\n"
                    else:
                        file_data += line
                total_content.append(content_text + file_data)
            except Exception as e:
                output_messages.append(f"Error reading {filename}: {e}\n")
    
    output_messages.append("Finished processing files.\n")
    combined_text = ''.join(total_content)
    token_count = len(encoding.encode(combined_text))
    
    return {
        'output_messages': ''.join(output_messages),
        'file_contents': combined_text,
        'token_count': token_count
    }

if __name__ == '__main__':
    app.run(debug=True)
