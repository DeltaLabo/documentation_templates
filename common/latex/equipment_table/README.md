# Equipment Table

This directory contains a reusable LaTeX command for creating a table of equipment.

## Usage

To use the equipment table, you first need to include the `equipment_table.tex` file in your main LaTeX document:

```latex
\subimport{common/latex/equipment_table/}{equipment_table.tex}
```

Then, you can use the `\equipmenttable` command to create a table. This command takes one argument, which is the body of the table. The table body should be a series of rows, with each row ending in `\\ \hline`.

### Example

```latex
\equipmenttable{
  1 & Equipment name & Type or Model & Manufacturer & Calibration Date & Serial No. & Notes \\
  \hline
  2 & Oscilloscope & MSO-X 3054A & Keysight & 2024-11-15 & ABC456 & 500 MHz bandwidth \\
  \hline
}
```
