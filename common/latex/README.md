# Reusable LaTeX code

This folder contains individual components (tables, headers, footers), document styles (fonts, headings. colors), classes, and class themes. 

Each folder contains LaTeX code meant to be imported
into instance documents by using `\documentclass` or `\subimport` (do not `\input` outside tests), so it doesn't represent a standalone LaTeX document..

Each folder **must** contain:
* A main LaTeX file (`.tex`, `.cls`, or `.sty`) that contains all the functionality or links together multiple submodule files.
* `test.tex`: Minimum working example of an instance document 
* `README.md`: When and how to use the component or style

Each folder *may* contain:
* `manifest.json`: A list of dependencies (images, other components or styles) and a boolean value determining if this folder should be published in the repo releases. The dependencies **must contain the main file itself**.

## Dependencies
**All** necessary files (including your main LaTeX file) count as a dependency, even if they're in the same folder. List the exact files you need, not the folder they're in.

Use relative paths from your template folder, not from the project root. Use `../` as many times as necessary. 

If you are unsure about this, just copy and paste the file paths you used in your main `.tex` file.
Know that if imports work on your tests without having to manually move files around or manipulate import paths, they will work on the releases.

```json
{
    "dependencies": [
        "../common/images/example_image.png",
        "../../common/latex/example_component/example_component.tex"
    ],
    "publish": false
}
```

## The `publish` parameter
If and only if `publish` is set to `true` in your `manifest.json` file, your template element will be published in the repo releases. All your dependencies will be automatically bundled.

Folders without a `manifest.json` file will be ignored when generating releases.

**If unsure, set this parameter to `false`.**

## Testing
You can use the following example to test components or styles:

```latex
\documentclass{article}
\usepackage[left=2cm,right=2cm,top=2cm,bottom=2cm]{geometry}

% Import your custom components or styles here
(...)

\title{Example Test}
\date{\vspace{-1.5cm}}

\begin{document}
\maketitle

% Add some content and check that it compiles without errors

\end{document}
```

You can use the following template to test classes and themes:

```latex
% Import your custom class here
\documentclass{...}
% Optionally, import a custom theme
\usetheme{...}

\title{Example Test}
\date{\vspace{-1.5cm}}

\begin{document}
\maketitle

% Add some content and check that it compiles without errors

\end{document}
```

## Imports
To import other LaTeX files safely, usely `\subimport`.
If you are using the `delta_base_class.cls` class, it's already included.
If not, just add `\usepackage{import}` to your preamble.
Afterwards, add the folder where you're importing the file from to `\graphicspath` so that image imports work properly.

See the following example:

```latex
\subimport{../path/to/}{file.tex}
\subimport{../../another/path/to/}{other_file.tex}
\graphicspath{{../path/to/}{../../another/path/to/}}
```