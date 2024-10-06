# Prompty

Prompty is a versatile web application designed to help you quickly pool multiple files into one place, making it easy to copy and paste everything into an AI for comprehensive, context-rich prompting. Whether you're working with code bases, markdown files for meeting notes, or any text-based content, Prompty simplifies the process of gathering and preparing your data for AI interactions.

Visit Prompty here: [https://prompty-flax.vercel.app/](https://prompty-flax.vercel.app/)

## Features

- Upload and process multiple files and folders
- Support for various AI models (GPT-3.5-turbo, GPT-4, etc.) for token count estimation
- Customizable ignore lists for file suffixes and folders
- Automatic file size limit (500KB) to prevent processing large files
- Real-time display of selected files
- Token count estimation based on the selected AI model
- Display of file contents for easy review and copying

## How to Use Prompty

1. Visit [https://prompty-flax.vercel.app/](https://prompty-flax.vercel.app/)
2. Select an AI model for token count estimation
3. Review and adjust the ignore lists for file suffixes and folders
4. Choose a folder to process
5. Upload and process your files
6. View the estimated token count and aggregated file contents
7. Copy the pooled content and paste it into your preferred AI tool for context-rich prompting

Prompty is ideal for:

- Developers who want to provide full context of their codebase to an AI
- Project managers collating meeting notes or documentation
- Researchers gathering multiple text sources for AI analysis
- Anyone looking to give AI a comprehensive view of their text-based data

## Important: Review Default Ignore Lists

Before using Prompty, it's crucial to review the default ignore lists for file suffixes and folders. These lists determine which files and folders are excluded from processing. To ensure that all desired files are included:

1. Check the "Ignore File Suffixes" field in the web interface.
2. Review the "Ignore Folders" field.
3. Remove any entries that you want to include in your processing.
4. Add any additional file types or folders you want to exclude.

Default ignored suffixes typically include:

```
.env, .log, .gitignore, .json, .npmrc, .prettierrc, .eslintrc, .babelrc, .pyc, .pyo, .pyd, .class
```

Default ignored folders typically include:

```
.git/, .svn/, .vscode/, .idea/, node_modules/, venv/, .venv/, build/, dist/, out/, .next/, coverage/
```

Adjust these lists according to your specific needs to ensure accurate processing of your desired files.

## Supported File Types

Prompty can process a wide range of text-based file types, including but not limited to:

### Programming and Markup Languages

- Python (.py, .pyw, .pyx, .pxd, .pxi)
- JavaScript (.js, .jsx, .mjs, .cjs)
- TypeScript (.ts, .tsx)
- HTML (.html, .htm, .xhtml)
- CSS (.css, .scss, .sass, .less)
- XML (.xml, .xsl, .xslt, .svg)
- JSON (.json, .jsonl)
- YAML (.yaml, .yml)
- Markdown (.md, .markdown)
- LaTeX (.tex, .ltx)
- R (.r, .R, .Rmd)
- Ruby (.rb, .rake, .gemspec)
- PHP (.php, .phtml, .php3, .php4, .php5, .phps)
- Java (.java, .jsp)
- C/C++ (.c, .cpp, .cxx, .h, .hpp)
- C# (.cs)
- Go (.go)
- Swift (.swift)
- Kotlin (.kt, .kts)
- Scala (.scala, .sc)
- Rust (.rs)
- Perl (.pl, .pm, .t)
- Lua (.lua)
- Shell scripts (.sh, .bash, .zsh, .fish)
- PowerShell (.ps1, .psm1, .psd1)
- SQL (.sql)

### Web Development

- JSX (.jsx)
- TSX (.tsx)
- Vue (.vue)
- Angular templates (.ng.html)
- Handlebars (.hbs, .handlebars)
- EJS (.ejs)
- Pug (.pug)

### Configuration Files

- INI (.ini)
- TOML (.toml)
- Properties (.properties)
- Environment files (.env)
- Docker files (Dockerfile, docker-compose.yml)
- Git config (.gitignore, .gitattributes)
- EditorConfig (.editorconfig)

### Data Formats

- CSV (.csv)
- TSV (.tsv)
- XML (.xml)
- JSON (.json)
- YAML (.yaml, .yml)

### Documentation

- Plain text (.txt)
- Markdown (.md, .markdown)
- reStructuredText (.rst)
- AsciiDoc (.adoc, .asciidoc)

### Log Files

- Log files (.log)
- Apache access logs
- Error logs

### Other

- License files (LICENSE, COPYING)
- README files (README, README.md)
- Change logs (CHANGELOG, CHANGELOG.md)
- Batch files (.bat, .cmd) - Windows
- Visual Basic Script (.vbs) - Windows

Note: While Prompty can technically process any text-based file, it's primarily designed for code, configuration, and documentation files. Binary files and very large text files (over 500KB) are automatically ignored to ensure optimal performance. The ability to extract text from some formats (like .docx or .pdf) may be limited and only include raw text content.

## Configuration

You can customize the following settings in the web interface:

- **AI Model**: Choose from various AI models to estimate token counts.
- **Ignore File Suffixes**: Comma-separated list of file extensions to ignore. Adjust this list to include or exclude specific file types.
- **Ignore Folders**: Comma-separated list of folder names to ignore. Modify this list to include or exclude specific folders from processing.

## Contributing

If you're interested in contributing to Prompty, please visit our GitHub repository and submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgements

- [Flask](https://flask.palletsprojects.com/) for the web framework
- [Bootstrap](https://getbootstrap.com/) for the front-end design
- [tiktoken](https://github.com/openai/tiktoken) for token counting

## Support

If you encounter any problems or have any questions, please open an issue in the GitHub repository.
