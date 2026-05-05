# Automated Test Report Template

This is a standardized, **fully automated** template for generating test reports. The template is compliant with **ISO/IEC/IEEE 29119**, **IEC 60068**, and **ISO/IEC 17025**.

## Workflow

To create a document instance, follow these steps:

### 1. Data Input (Modular CSVs)

Data is organized into **five specific CSV files**. You can edit these files using Excel, Google Sheets, or any text editor.

**Crucial:** Ensure the `doc_id` (e.g., `TEST-001`) is identical across all five files to link the information correctly. If an ID is missing in one file, the script will skip that section but still attempt to generate the PDF with blank spaces.

### 2. Build Report

Run the main automation script to scan the CSV files, merge the data by ID, and compile the PDF:
python generate_test.py

### 3. Review Output

The script will automatically create a folder named after your doc_id and place the compiled PDF inside. Temporary LaTeX files (.log, .aux, .tex) are automatically removed after generation.

#### Repo Folder Structure

```text
.
├── 01_metadata.csv           # General document info
├── 02_scope.csv              # Objectives and standards
├── 03_item_environment.csv   # DUT info and lab conditions
├── 04_procedure.csv          # Equipment and test steps
├── 05_results.csv            # Analysis and conclusions
├── generate_test.py          # Main automation script
└── [Doc_ID]/                 # Directory created automatically
    └── PDF/
        └── Report_[Doc_ID].pdf # The finalized, compiled report
```

## Prerequisites

1. Python 3.x
2. PyLaTeX library: Install it using pip install pylatex
3. MiKTeX: Ensure pdflatex is installed and added to your system PATH.

## Troubleshooting

- Missing ID Error: If the console shows ERROR: The ID was not found in: [filename], check that the doc_id column in that specific CSV matches exactly (check for extra spaces, casing, or typos).
- LaTeX Warning (Logo): If the log shows a "pdftex.def Error" regarding a missing logo, the script will still attempt to generate the PDF. Ensure your image assets are located in the ../../common/images/ path.
- File in Use: Ensure the CSV files are not open in Excel while running the script to avoid "Permission Denied" errors.

## Data Entry Guide: How to fill the CSVs

Each CSV file handles a specific section of the report. Follow these formatting rules:

1. **metadata.csv**

    General report information.
    - doc_id: Unique identifier (e.g., TEST-001).
    - title: Main title of the report.
    - subtitle: Subtitle or standards reference.
    - version: Document version (e.g., 1.0).
    - date: YYYY-MM-DD format.
    - prepared_by: Name of the author.
    - approved_by: Name of the approver.
    - observations: General notes or "None".
2. **scope.csv**

    Goals and standards.
    - test_name: Specific name of the test performed.
    - purpose_obj: Main objective of the test.
    - purpose_limits: Boundaries or exclusions of the test.
    - purpose_focus: Key areas of interest or critical points.
    - ref_standards: List of standards (e.g., ISO 17025; IEC 60068).
    - definitions: LaTeX formatted list.
    - Example: \item \textbf{DUT}: Device Under Test \item \textbf{EUT}: - Equipment Under Test
3. **item_environment.csv**

    The object being tested (DUT) and the environment.
    - item_name: Name of the device.
    - item_sn: Serial number or revision.
    - item_mfr: Manufacturer name.
    - item_config: Hardware/Software configuration.
    - temp: Temperature in Celsius (numbers only).
    - humidity: Humidity percentage (numbers only).
4. **procedure.csv**

    Tools and the execution steps.
    - equip_data: LaTeX table row for equipment.
        - Example: 1 & Multimeter & 34401A & Keysight & 2024-01-01 & SN123 & High Precision
    - inputs: Defined input conditions (e.g., 12V DC).
    - outputs: Expected output behavior.
    - criteria: Acceptance limits (e.g., +/- 5%).
    - proc_table: The actual test steps in LaTeX format.
        - Example: 1 & Setup & 5V In & 5.01V & Pass \\ \hline 2 & Load & 5V/1A & 4.98V & Pass
5. **results.csv**

    Final verdict and annexes.
    - results_raw: Reference to raw data logs or attachments.
    - results_analysis: Summary of the data findings.
    - conclusion_res: Final status (PASSED or FAILED).
    - conclusion_obs: Final remarks or special observations.
    - annexes_list: LaTeX list of attached documents.
        - Example: \item Calibration Certificates \item Raw Data Logs
