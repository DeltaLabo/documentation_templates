# Release Generator

This Python script automatically generates standalone release packages for LaTeX templates that are marked for publication.

## Overview

The release generator:

1. **Finds publishable templates**: Scans for all `manifest.json` files in the repository where `publish` is set to `true`
2. **Creates release folders**: Makes a release folder for each publishable template 
3. **Resolves dependencies**: Recursively finds and copies all dependencies listed in manifest files
4. **Preserves structure**: Maintains the original folder structure for dependencies under a `common/` folder
5. **Modifies imports**: Updates relative import paths in main files to use the release folder as root

## Usage

The script uses `uv` for dependency management and can be run with:

```bash
uv run --script generate_releases.py
```

Or if you have Python 3.8+ installed:

```bash
python3 generate_releases.py
```

## Output Structure

For each publishable template, the generator creates:

```
releases/
├── template_name/
│   ├── template_name.tex      # Main template file (with modified imports)
│   ├── common/                # All dependencies preserving folder structure
│   │   ├── latex/
│   │   │   └── delta_base_styles/
│   │   │       └── delta_base_styles.cls
│   │   └── images/
│   │       └── delta_logo.png
│   ├── README.md              # Copied from source folder
│   ├── test.tex               # Copied from source folder (with modified imports)
│   └── example_refs.bib       # Same-folder dependencies copied to root
```

## How it Works

### Dependency Resolution

The script:
1. Parses each `manifest.json` file to get the dependency list
2. Resolves each dependency path relative to the manifest's folder
3. If a dependency has its own `manifest.json`, recursively resolves its dependencies
4. Copies all resolved files to the appropriate location in the release folder

### Import Path Modification

For main template files and test files, the script updates:
- `\documentclass{../common/path/file}` → `\documentclass{common/path/file}`
- `\subimport{../common/path/}{file}` → `\subimport{common/path/}{file}`
- `\input{../common/path/file}` → `\input{common/path/file}`
- `\graphicspath` entries to use `common/` as the base path

### File Placement Rules

- **Main template files**: Always copied to release folder root
- **Same-folder dependencies**: Copied to release folder root (e.g., beamer theme files)
- **Dependencies from `common/`**: Copied to `common/` with preserved folder structure
- **Other dependencies**: Copied to release folder root
- **README.md and test.tex**: Always copied to release folder root if they exist

## Example

Given this repository structure:
```
test_report/
├── manifest.json          # "publish": true
├── test_report.tex
└── test.tex

common/latex/delta_header/
├── manifest.json          # "publish": false, but used as dependency
├── delta_header.tex
└── dependency.png
```

The generator creates:
```
releases/test_report/
├── test_report.tex         # Modified imports
├── test.tex               # Modified imports  
├── common/
│   └── latex/
│       └── delta_header/
│           ├── delta_header.tex
│           └── dependency.png
```

## Requirements

- Python 3.8 or higher
- `uv` package manager (or use standard Python)
- `manifest.json` files must be valid JSON with `dependencies` array and `publish` boolean

## Manifest File Format

```json
{
    "dependencies": [
        "../common/latex/delta_base_styles/delta_base_styles.cls",
        "../common/images/logo.png",
        "same_folder_file.sty"
    ],
    "publish": true
}
```

Dependencies should be specified as relative paths from the folder containing the manifest file.