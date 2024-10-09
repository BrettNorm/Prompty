from flask import Flask, render_template, request, jsonify
from werkzeug.utils import secure_filename
import tiktoken
import os
import docx  # Import the python-docx library
import PyPDF2

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        model_name = 'gpt-4'
        ignore_suffixes = request.form.get('ignore_suffixes', '')
        ignore_folders = request.form.get('ignore_folders', '')
        files = request.files.getlist('files')


        delimiter = request.form.get('delimiter', '=== FILE: {filename} ===')

        if '{filename}' not in delimiter:
            return jsonify({'error': "Delimiter must include '{filename}' placeholder."}), 400

        if not files:
            return jsonify({'error': 'Missing files'}), 400


        result = process_files(files, model_name, ignore_suffixes, ignore_folders, delimiter)

        if result is None:
            # This should no longer occur, but added as a safety net
            return jsonify({'error': 'No result returned from processing.'}), 500

        if 'error' in result:
            return jsonify({'error': result['error']}), 400

        return jsonify(result)
    else:
        return render_template('index.html')

def process_files(uploaded_files, model_name, ignore_suffixes, ignore_folders, delimiter):
    import os
    import re

    file_size_limit = 500 * 1024  # 500 KB size limit for files to process
    MAX_TOTAL_SIZE = 10 * 1024 * 1024
    total_content = []
    output_messages = []
    processed_files = set()

    # Calculate the total size of all uploaded files
    total_size = 0
    for file in uploaded_files:
        file.seek(0, os.SEEK_END)  # Move to the end of the file
        size = file.tell()
        file.seek(0)  # Reset to the beginning of the file
        total_size += size

    if total_size > MAX_TOTAL_SIZE:
        return {
            'error': f'Total upload size exceeds limit of {MAX_TOTAL_SIZE / (1024 * 1024)} MB.'
        }

    # Comprehensive list of supported file extensions
    supported_extensions = {
        # Existing extensions...
        '.docx',  # Add .docx support
        '.pdf', # Add .pdf support
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
        # Use the full path or unique identifier as the key
        file_path = file.filename.lower()  # Ensure consistent casing
        if file_path in processed_files:
            output_messages.append(f"Skipping duplicate file: {file_path}\n")
            continue  # Skip processing duplicates

        file_extension = os.path.splitext(file_path)[1]

        # Check if the file type is supported
        if file_extension not in supported_extensions and not any(file_path.endswith(suffix) for suffix in supported_extensions):
            output_messages.append(f"Skipping unsupported file type: {file_path}\n")
            continue

        # Check the file size before reading
        file.seek(0, os.SEEK_END)  # Move to the end of the file
        size = file.tell()
        file.seek(0)  # Reset to the beginning of the file
        if size > file_size_limit:
            output_messages.append(f"Skipping file (too large): {file_path}\n")
            continue

        # Mark this file as processed
        processed_files.add(file_path)

        try:
            # Replace {filename} with the actual filename
            formatted_delimiter = delimiter.replace('{filename}', file_path)
            content_text = f"\n\n{formatted_delimiter}\n"

            if file_extension == '.docx':
                # Handle .docx files
                doc = docx.Document(file)
                file_data = '\n'.join([para.text for para in doc.paragraphs])

            elif file_extension == '.pdf':
                # Handle .pdf files
                reader = PyPDF2.PdfReader(file)
                file_data = ''
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    text = page.extract_text()
                    if text:
                        file_data += text
                    else:
                        output_messages.append(f"No text found on page {page_num + 1} of {file_path}\n")

            else:
                # Handle other text-based files
                file_data = file.read().decode('utf-8', errors='ignore')

            total_content.append(content_text + file_data)
        except Exception as e:
            output_messages.append(f"Error reading {file_path}: {e}\n")

    output_messages.append("Finished processing files.\n")
    combined_text = ''.join(total_content)
    token_count = len(encoding.encode(combined_text))

    return {
        'output_messages': ''.join(output_messages),
        'file_contents': combined_text,
        'token_count': token_count
    }

if __name__ == '__main__':
    app.run()
