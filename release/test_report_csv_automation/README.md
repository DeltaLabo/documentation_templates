# Automated Test Report Template

This is a standarized, **fully automated** template for generating test reports. The template is compliant with **ISO/IEC/IEEE 29119**, **IEC 60068** and **ISO/IEC 17025**.

## Workflow

To create a document instance, follow these three steps:

### Data input

Open the file "generate_csv.py" and modify the variables within the configuration section. Follow the comments provided in the code to insert the metadata. **Do not modify the LaTeX or CSV logic, only update the content values**.

### Generate CSV

Run the data entry script to create the intermediate CSV file.

### Build report and organize files

Run the main automation script ("generate_test.py") to compile the PDF and organize the output.

### Repo folder structure

[Doc_ID]/

├── PDF/

│   └── Report_[Doc_ID].pdf     # The finalized, compiled report

└── CSV/

    └── test_data.csv           # A copy of the source data for traceability

## Prerequisites

- Python 3.x
- PyLaTeX library: Install it using *pip install pylatex*
- MiKTeX

## Troubleshooting

- WinError32: Ensure the csv is not open in any program while running the scripts.
- LaTeX Error: If the compilation fails, check the output folder. Ensure all relative paths to the common/ folder are preserved.
