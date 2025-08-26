# LaTeX Documentation Templates

This repository serves two distinct groups of people:

1. **Template Maintainers**: Contributors who create and maintain LaTeX templates in this repository
2. **Template Users**: Users who select templates to create document instances for their specific needs, and then save the LaTex code and its output to a different repo

The recommended development environment uses **VS Code** with **LaTeX Workshop** extension and **MiKTeX** distribution.

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

### VS Code Configuration for LaTeX

Create or update your VS Code settings (`File` → `Preferences` → `Settings` → `Open Settings (JSON)`) to include the following content (**DO NOT** delete existing settings):

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

## For Template Users

### Setup instructions

1. **Browse available templates**:
   - Visit this repository to see available templates

3. **Clone the repo**:
   - Clone the repository and locate the template folder you need

4. **Create a new document instance**:
   - Copy all the contents of the folder that your desired template is located in to the location where you will work on the finalized document
   - Write your document in the repository of the project that the document belongs to, **NOT** in this repo (`documentation_templates`)
   - Apply Git best practices when writing your document, such as creating branches for important updates.

### Document Creation Workflow

1. **Open your project repo in VS Code**

3. **Customize the template**:
   - Edit the main `.tex` file with your content
   - Replace placeholder text and examples
   - Add your figures and tables, and reference them in your text
   - Add bibliographic references to `.bib` files, and load them to your LaTeX document

4. **Build and preview**:
   - Use `Ctrl+Alt+B` to compile your document
   - Use `Ctrl+Alt+V` to open the PDF viewer
   - LaTeX Workshop will automatically recompile on save

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

## For Template Maintainers

### Development workflow

1. If one doesn't exist yet, create an issue describng the template you will create, or the changes you will apply to an existing one
   - Assign the issue to yourself and create a new branch to work on the issue, if needed
2. Clone this repo, and checkout to the issue branch
3. Create a new folder for your template, if needed
4. Create a `README.md` file in your template folder (**DO NOT** modify the one at the repo root) explaining **when** and **how** to use your template
5. Start development, structuring your work as commits
   - Try to keep all your work in a single LaTeX file (`.tex` or `.cls`), that way it's easier for others to import and use.
   - If you need to use multiple `.tex`, link them together in a single main file.
   - Give your main file the same name as your folder.
7. Test your template by compiling it, and make sure there are no errors
   - If there are warnings, properly explain them in your `README.md` file
   - Commit the test file, named as `test.tex`
8. Create a `manifest.json` listing all files and assets needed to compile your template
9. Open a pull request once you have completed your changes, and ask someone else to review and merge it

### Repo folder structure

```
documentation_templates/
├── common/ # For elements shared across multiple templates
│   ├── images/
│   │   └── delta_logo.png
│   ├── bib/
│   │   └── shared_refs.bib
│   ├── data/
│   │   └── members_table.tex # e.g. a table with all lab members
│   └── latex/
│       └── example_class_name/
│           └── example_class.cls
│           ├── test.tex
│           ├── manifest.json # List of dependencies from common/
│           ├── README.md # When and how to use the template
│           └── themes/
│               └── example_theme_name/
│                   └── example_theme.sty
├── example_template/
│   ├── example_template.tex
│   ├── example_image.png
│   ├── test.tex # Only needed if template .tex can't be compiled on its own
│   ├── manifest.json # List of dependencies from common/
│   └── README.md # When and how to use the template
└── README.md # Project root README
```