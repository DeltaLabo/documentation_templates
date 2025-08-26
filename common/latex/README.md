# Reusable LaTeX code

This folder contains individual components (tables, headers, footers), document styles (fonts, headings. colors), classes, and class themes. 

Each folder contains LaTeX code meant to be imported
into instance documents by using `\documentclass` or `\input`, so it doesn't represent a standalone LaTeX document.

Each folder **must** contain:
* A main LaTeX file (`.tex` or `.cls`) with the same name as the folder that contains all the functionality of your template element
* `test.tex`: Minimum working example of an instance document 
* `README.md`: When and how to use the component or style

Each folder *may* contain:
* `manifest.json`: A list of dependencies (images, other components or styles) and a boolean value determining if this folder should be published in the repo releases. 

## Dependencies
**All** files apart from your main LaTeX file (the one with the same name as the folder) count as a dependency, even if it's in the same folder.

List the exact files you need, not the folder they're in.

```json
{
    "dependencies": [
        "common/images/example_image.png",
        "common/latex/example_component/example_component.tex"
    ],
    "publish": false
}
```

## The `publish` parameter
If and only if `publish` is set to `true` in your `manifest.json` file, your template element will be published in the repo releases. All your dependencies will be automatically bundled.

Folders without a `manifest.json` file will be ignored when generating releases.
Even if not listed in the dependencies, the main file of each published folder will be automatically included in the release
as long as it correctly has the same name as the folder.

**If unsure, set this parameter to `false`.**

## Testing
You can use the following example to test components or styles:

```latex
\documentclass{article}
\usepackage[left=2cm,right=2cm,top=2cm,bottom=2cm]{geometry}

% Import your custom components or styles here
\input(...)

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