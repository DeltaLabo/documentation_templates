# Version Approval Table

A standard document version approval table.

To use it, include this file in your main LaTeX document using `\subimport`
and then use the `\makeversionapprovaltable` command where you want the
table to appear.
 
This table looks best on single column document sections.

You can set the data for the table using the following commands in your
document's preamble:

```latex
\docid{XYZ-001}
\version{1.0}
\docdate{\today}
\preparedby{John Doe}
\approvedby{Peter Jones}
...
\begin{document}
\makeversionapprovaltable
...
```