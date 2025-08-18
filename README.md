# LaTeX Documentation Templates

This repository hosts LaTeX templates used for various purposes in an R&D laboratory environment. The templates are designed to provide consistent formatting and structure for academic papers, reports, presentations, and other documentation.

## Overview

This repository serves two distinct user roles:

1. **Template Developers**: Contributors who create and maintain LaTeX templates in this repository
2. **Document Writers**: Users who select templates to create document instances for their specific needs

The recommended development environment uses **VS Code** with **LaTeX Workshop** extension and **MiKTeX** distribution for optimal LaTeX development experience.

## Setup Instructions for Windows

### Prerequisites

1. **VS Code**: Download and install from [https://code.visualstudio.com/](https://code.visualstudio.com/)
2. **Git**: Download and install from [https://git-scm.com/download/win](https://git-scm.com/download/win)

### Installing MiKTeX

1. Download MiKTeX from [https://miktex.org/download](https://miktex.org/download)
2. Run the installer and choose "Complete MiKTeX" for full package installation
3. During installation, select:
   - Install for all users (recommended)
   - Set "Install missing packages on-the-fly" to "Yes"
4. After installation, open MiKTeX Console and update all packages:
   - Go to "Updates" tab
   - Click "Check for updates"
   - Install all available updates

### Setting up VS Code for LaTeX

1. Open VS Code
2. Install the **LaTeX Workshop** extension:
   - Press `Ctrl+Shift+X` to open Extensions
   - Search for "LaTeX Workshop" by James Yu
   - Click Install
3. Install additional helpful extensions:
   - **Code Spell Checker**: For spell checking in LaTeX documents
   - **GitLens**: For enhanced Git integration

### VS Code Configuration for LaTeX

Create or update your VS Code settings (`File` → `Preferences` → `Settings` → `Open Settings (JSON)`):

```json
{
    "latex-workshop.latex.tools": [
        {
            "name": "pdflatex",
            "command": "pdflatex",
            "args": [
                "-synctex=1",
                "-interaction=nonstopmode",
                "-file-line-error",
                "%DOC%"
            ]
        },
        {
            "name": "bibtex",
            "command": "bibtex",
            "args": ["%DOCFILE%"]
        }
    ],
    "latex-workshop.latex.recipes": [
        {
            "name": "pdflatex",
            "tools": ["pdflatex"]
        },
        {
            "name": "pdflatex → bibtex → pdflatex*2",
            "tools": ["pdflatex", "bibtex", "pdflatex", "pdflatex"]
        }
    ],
    "latex-workshop.view.pdf.viewer": "tab",
    "latex-workshop.latex.autoClean.run": "onBuilt"
}
```

## For Template Developers

### Getting Started

1. Clone this repository:
   ```bash
   git clone https://github.com/DeltaLabo/documentation_templates.git
   cd documentation_templates
   ```

2. Open the repository in VS Code:
   ```bash
   code .
   ```

### Development Workflow

1. **Create a new template**:
   - Create a new folder for your template (e.g., `research-paper-template/`)
   - Include a main `.tex` file and any necessary support files
   - Add a README within the template folder explaining its purpose and usage

2. **Template Structure**:
   - Use clear, semantic file names
   - Include comments in LaTeX files to guide users
   - Provide example content to demonstrate usage
   - Include any required style files, bibliography files, or figures

3. **Testing Templates**:
   - Always test your templates by compiling them
   - Use `Ctrl+Alt+B` in VS Code to build/compile LaTeX
   - Ensure the template compiles without errors
   - Test with sample content to verify formatting

4. **Documentation**:
   - Each template should include its own README.md
   - Document any special requirements or packages needed
   - Include examples of the expected output

5. **Committing Changes**:
   ```bash
   git add .
   git commit -m "Add/Update template: [template-name]"
   git push origin main
   ```

### Best Practices for Template Development

- Keep templates modular and reusable
- Use relative paths for included files
- Minimize external dependencies
- Include error handling for missing packages
- Provide clear examples and documentation
- Test templates on clean MiKTeX installations

## For Document Writers

### Getting Started

1. **Browse available templates**: Visit this repository to see available templates

2. **Clone or download a specific template**:
   - For Git users: Clone the repository and copy the template folder you need
   - For non-Git users: Download the repository as ZIP and extract the desired template

3. **Set up your document repository**:
   ```bash
   # Create a new repository for your document
   mkdir my-document-project
   cd my-document-project
   git init
   
   # Copy template files to your project
   cp -r /path/to/documentation_templates/[template-name]/* .
   ```

### Document Creation Workflow

1. **Open your document project in VS Code**:
   ```bash
   code .
   ```

2. **Customize the template**:
   - Edit the main `.tex` file with your content
   - Replace placeholder text and examples
   - Add your figures, tables, and references
   - Modify styling as needed for your specific requirements

3. **Build and preview**:
   - Use `Ctrl+Alt+B` to compile your document
   - Use `Ctrl+Alt+V` to open the PDF viewer
   - LaTeX Workshop will automatically recompile on save

4. **Version control your document**:
   ```bash
   git add .
   git commit -m "Initial document based on [template-name]"
   git remote add origin [your-document-repository-url]
   git push -u origin main
   ```

### Tips for Document Writers

- Don't modify the original template files; copy them to your own repository
- Keep a backup of your work in a separate Git repository
- Regularly commit your changes as you write
- Use meaningful commit messages to track your progress
- Consider using branches for different versions or sections

## Troubleshooting

### Common Issues

1. **"Package not found" errors**:
   - Open MiKTeX Console
   - Go to Packages tab
   - Search and install the missing package
   - Or ensure "Install packages on-the-fly" is enabled

2. **Compilation fails**:
   - Check the LaTeX Workshop output panel in VS Code
   - Look for syntax errors in your `.tex` file
   - Ensure all referenced files exist and paths are correct

3. **PDF not updating**:
   - Clear auxiliary files: `Ctrl+Alt+C` in VS Code
   - Rebuild: `Ctrl+Alt+B`
   - Check for compilation errors

4. **VS Code not recognizing LaTeX commands**:
   - Ensure LaTeX Workshop extension is installed and enabled
   - Check that your file has `.tex` extension
   - Restart VS Code if necessary

## Linux Setup Instructions

### Installing LaTeX Distribution

**Ubuntu/Debian**:
```bash
sudo apt update
sudo apt install texlive-full
```

**Fedora**:
```bash
sudo dnf install texlive-scheme-full
```

**Arch Linux**:
```bash
sudo pacman -S texlive-most texlive-lang
```

### Installing VS Code

**Ubuntu/Debian**:
```bash
wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > packages.microsoft.gpg
sudo install -o root -g root -m 644 packages.microsoft.gpg /etc/apt/trusted.gpg.d/
sudo sh -c 'echo "deb [arch=amd64,arm64,armhf signed-by=/etc/apt/trusted.gpg.d/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" > /etc/apt/sources.list.d/vscode.list'
sudo apt update
sudo apt install code
```

**Fedora**:
```bash
sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc
sudo sh -c 'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" > /etc/yum.repos.d/vscode.repo'
sudo dnf check-update
sudo dnf install code
```

### Linux-Specific Configuration

The VS Code configuration and workflow remain the same as Windows. The main differences are:

1. Package management is handled through your Linux distribution's package manager instead of MiKTeX Console
2. File paths use forward slashes instead of backslashes
3. Some LaTeX packages might have different names or locations

### Installing Additional Packages (Linux)

If you need additional LaTeX packages not included in the full installation:

**Ubuntu/Debian**:
```bash
sudo apt search texlive-latex-extra
sudo apt install [package-name]
```

**Fedora**:
```bash
sudo dnf search texlive
sudo dnf install [package-name]
```

## Contributing

We welcome contributions to improve existing templates or add new ones. Please:

1. Follow the template development guidelines above
2. Test your templates thoroughly
3. Include comprehensive documentation
4. Submit pull requests with clear descriptions

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
