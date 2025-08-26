# Signature Table

A reusable command for creating a table with document signatures.

This command, `\signaturetable`, takes one argument which is the body of the table.
The table body should be a series of rows, with each row ending in \\ \hline.

Example usage:
```latex
\signaturetable{
Name of the person & Role of the person & Date & \\ % Leave last field blank for physical signature
\hline
}
```