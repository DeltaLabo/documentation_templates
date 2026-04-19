import csv
import os

def generate_csv_data():
    # =========================================================
    # 1. DOCUMENT IDENTIFICATION (Input data here)
    # =========================================================
    
    # ### DOC ID HERE ###
    doc_id = "TEST-001"
    
    # ### DOC TITLE HERE ###
    doc_title = "Testing and Verification Report"
    
    # ### DOC SUBTITLE HERE ###
    doc_subtitle = "Based on ISO/IEC 17025 and IEC 60068"
    
    # ### DOCUMENT VERSION ###
    version = "1.0"
    
    # ### DOCUMENT DATE ###
    date = "2024-06-01"
    
    # ### PERSONNEL RESPONSIBLE ###
    prepared_by = "John Doe"
    approved_by = "Jane Smith"
    
    # ### GENERAL OBSERVATIONS ###
    observations = "None"

    # =========================================================
    # 2. TEST CASE DETAILS
    # =========================================================
    
    # ### TEST NAME (This will be the folder name) ###
    test_name = "Load Regulation Verification for DUT"
    
    # ### PURPOSE AND SCOPE ###
    purpose_obj = "Verify electrical stability under full load"
    purpose_limits = "Limited to the secondary power stage"
    purpose_focus = "Focus on ripple voltage and calibration traceability"
    
    # ### STANDARDS AND DEFINITIONS ###
    ref_standards = "ISO 29119-3; IEC 60068"
    # Use r'' for LaTeX items to avoid backslash issues
    definitions = r"\item \textbf{DUT:} Device Under Test \item \textbf{EUT:} Equipment Under Test"

    # =========================================================
    # 3. ITEM AND ENVIRONMENT
    # =========================================================
    
    # ### ITEM UNDER TEST (DUT) ###
    item_name = "DUT Power Module"
    item_sn = "DUT-SN-12345"
    item_mfr = "DeltaLabo"
    item_config = "HW v2.1"
    
    # ### ENVIRONMENTAL CONDITIONS ###
    temp = "25.0"
    humidity = "50.0"
    
    # ### EQUIPMENT USED (Table format: Id & Name & Model & etc.) ###
    equip_data = "1 & Multimeter & 34465A & Keysight & 2024-02-15 & XYZ123 & High precision"

    # =========================================================
    # 4. TEST EXECUTION AND RESULTS
    # =========================================================
    
    # ### PARAMETERS ###
    inputs = "12V DC Input / 5A Load"
    outputs = "Sinusoidal output response"
    criteria = "Tolerance +/- 0.5V"
    
    # ### PROCEDURE TABLE (LaTeX rows syntax) ###
    # Important: No spaces allowed before \hline
    proc_table = r"1 & Startup & 12V In / 0A Out & 12.01V & Pass \\ \hline 2 & Full Load & 12V In / 5A Out & 11.95V & Pass"
    
    # ### DATA ANALYSIS ###
    results_raw = "Data logs attached in Annex A"
    results_analysis = "The DUT showed excellent stability under full load."
    
    # ### FINAL CONCLUSION ###
    conclusion_res = "PASSED"
    conclusion_obs = "No thermal drifting observed."
    
    # ### ANNEXES LIST ###
    annexes_list = r"\item Test circuit diagrams \item Calibration certificates"

    # =========================================================
    # 5. CSV FILE GENERATION LOGIC
    # =========================================================

    # Dictionary mapping following the provided CSV structure
    data_row = {
        'doc_id': doc_id,
        'title': doc_title,
        'subtitle': doc_subtitle,
        'version': version,
        'date': date,
        'prepared_by': prepared_by,
        'approved_by': approved_by,
        'observations': observations,
        'test_name': test_name,
        'purpose_obj': purpose_obj,
        'purpose_limits': purpose_limits,
        'purpose_focus': purpose_focus,
        'ref_standards': ref_standards,
        'definitions': definitions,
        'item_name': item_name,
        'item_sn': item_sn,
        'item_mfr': item_mfr,
        'item_config': item_config,
        'temp': temp,
        'humidity': humidity,
        'equip_data': equip_data,
        'inputs': inputs,
        'outputs': outputs,
        'criteria': criteria,
        'proc_table': proc_table,
        'results_raw': results_raw,
        'results_analysis': results_analysis,
        'conclusion_res': conclusion_res,
        'conclusion_obs': conclusion_obs,
        'annexes_list': annexes_list
    }

    # Create directory named after the test
    folder_name = "output"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    # Save the CSV file inside the folder
    csv_file_path = os.path.join(folder_name, "test.csv")
    
    try:
        with open(csv_file_path, mode='w', encoding='utf-8-sig', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data_row.keys())
            writer.writeheader()
            writer.writerow(data_row)
        print(f"Successfully generated CSV at: {csv_file_path}")
    except Exception as e:
        print(f"Error generating CSV: {e}")

if __name__ == "__main__":
    generate_csv_data()