from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import tiktoken
import os
import docx  # Import the python-docx library

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

    # Comprehensive list of supported file extensions
    supported_extensions = {
        # Existing extensions...
        '.docx',  # Add .docx support

        # (Rest of the supported extensions)
        '.py', '.pyw', '.pyx', '.pxd', '.pxi',  # Python
        '.js', '.jsx', '.mjs', '.cjs',  # JavaScript
        '.ts', '.tsx',  # TypeScript
        '.html', '.htm', '.xhtml',  # HTML
        '.css', '.scss', '.sass', '.less',  # CSS
        '.xml', '.xsl', '.xslt', '.svg',  # XML
        '.json', '.jsonl',  # JSON
        '.yaml', '.yml',  # YAML
        '.md', '.markdown',  # Markdown
        '.tex', '.ltx',  # LaTeX
        '.r', '.rmd',  # R
        '.rb', '.rake', '.gemspec',  # Ruby
        '.php', '.phtml', '.php3', '.php4', '.php5', '.phps',  # PHP
        '.java', '.jsp',  # Java
        '.c', '.cpp', '.cxx', '.h', '.hpp',  # C/C++
        '.cs',  # C#
        '.go',  # Go
        '.swift',  # Swift
        '.kt', '.kts',  # Kotlin
        '.scala', '.sc',  # Scala
        '.rs',  # Rust
        '.pl', '.pm', '.t',  # Perl
        '.lua',  # Lua
        '.sh', '.bash', '.zsh', '.fish',  # Shell scripts
        '.ps1', '.psm1', '.psd1',  # PowerShell
        '.sql',  # SQL

        # Web Development
        '.vue',  # Vue
        '.ng.html',  # Angular templates
        '.hbs', '.handlebars',  # Handlebars
        '.ejs',  # EJS
        '.pug',  # Pug

        # Configuration Files
        '.ini',  # INI
        '.toml',  # TOML
        '.properties',  # Properties
        '.env',  # Environment files
        'dockerfile', '.dockerignore',  # Docker files
        '.gitignore', '.gitattributes',  # Git config
        '.editorconfig',  # EditorConfig

        # Data Formats
        '.csv', '.tsv',  # CSV and TSV

        # Documentation
        '.txt',  # Plain text
        '.rst',  # reStructuredText
        '.adoc', '.asciidoc',  # AsciiDoc

        # Log Files
        '.log',  # Log files

        # Other
        'license', 'copying',  # License files
        'readme',  # README files
        'changelog',  # Change logs
        '.bat', '.cmd',  # Batch files (Windows)
        '.vbs'  # Visual Basic Script (Windows)
    }

    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        output_messages.append(f"Model '{model_name}' not recognized. Using default encoding.\n")
        encoding = tiktoken.get_encoding('cl100k_base')

    for file in uploaded_files:
        filename = file.filename.lower()
        file_extension = os.path.splitext(filename)[1]
        
        # Check if the file type is supported
        if file_extension not in supported_extensions and not any(filename.endswith(suffix) for suffix in supported_extensions):
            output_messages.append(f"Skipping unsupported file type: {filename}\n")
            continue

        # Check the file size before reading
        file.seek(0, os.SEEK_END)  # Move to the end of the file
        size = file.tell()
        file.seek(0)  # Reset to the beginning of the file
        if size > file_size_limit:
            output_messages.append(f"Skipping file (too large): {filename}\n")
            continue

        try:
            content_text = f"\n\n=== FILE: {filename} ===\n"
            if file_extension == '.docx':
                # Handle .docx files
                doc = docx.Document(file)
                file_data = '\n'.join([para.text for para in doc.paragraphs])
            else:
                # Handle other text-based files
                file_data = file.read().decode('utf-8', errors='ignore')
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
