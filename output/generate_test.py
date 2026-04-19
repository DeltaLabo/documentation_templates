import csv
import os
import time
import shutil # Needed to move the file
from pylatex import Document, Section, Subsection, Command, Itemize, Tabular, Enumerate
from pylatex.utils import NoEscape

def create_test_report(data):
    print(f"\n--- Processing Report ID: {data['doc_id']} ---")
    
    # 1. Folder Setup
    # We create the structure: output/PDF
    target_dir = os.path.join(data['doc_id'], 'PDF')
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    # 2. Document Setup
    doc = Document(
        documentclass=NoEscape('../common/latex/delta_base_styles/delta_base_styles'),
        fontenc='T1',
        inputenc='utf8',
        lmodern=True
    )

    # 3. Preamble & Styles (Paths remain relative to the script location)
    doc.preamble.append(Command('addbibresource', 'example_refs.bib'))
    doc.preamble.append(NoEscape(r'\subimport{../common/latex/delta_header/}{delta_header.tex}'))
    doc.preamble.append(NoEscape(r'\subimport{../common/latex/equipment_table/}{equipment_table.tex}'))
    doc.preamble.append(NoEscape(r'\subimport{../common/latex/signature_table/}{signature_table.tex}'))
    doc.preamble.append(NoEscape(r'\subimport{../common/latex/version_approval_table/}{version_approval_table.tex}'))
    
    doc.preamble.append(NoEscape(r'''\graphicspath{
      {../common/latex/delta_base_styles/}
      {../common/latex/delta_header/}
      {../common/latex/equipment_table/}
      {../common/latex/signature_table/}
      {../common/latex/version_approval_table/}
      {../common/images/}
    }'''))

    # Metadata mapping
    doc.preamble.append(Command('doctitle', data['title']))
    doc.preamble.append(Command('docsubtitle', data['subtitle']))
    doc.preamble.append(Command('docid', data['doc_id']))
    doc.preamble.append(Command('version', data['version']))
    doc.preamble.append(Command('docdate', data['date']))
    doc.preamble.append(Command('preparedby', data['prepared_by']))
    doc.preamble.append(Command('approvedby', data['approved_by']))
    doc.preamble.append(Command('observations', data['observations']))

    # --- DOCUMENT BODY ---
    doc.append(NoEscape(r'\makedeltaheader'))
    doc.append(NoEscape(r'\par\vspace{0.5cm}'))

    with doc.create(Section('Test plan summary')):
        doc.append(NoEscape(r'\textbf{Name of the test:} ' + data['test_name'] + r'\\[0.2cm]'))
        doc.append(NoEscape(r'\makeversionapprovaltable'))

    with doc.create(Section('Purpose and scope')):
        with doc.create(Itemize()) as item:
            item.add_item(NoEscape(r'\textbf{Main objective of the test:} ' + data['purpose_obj']))
            item.add_item(NoEscape(r'\textbf{Limits of the test:} ' + data['purpose_limits']))
            item.add_item(NoEscape(r'\textbf{Key focus areas:} ' + data['purpose_focus']))

    with doc.create(Section('References')):
        with doc.create(Itemize()) as item:
            item.add_item(NoEscape(r'\textbf{Standards:} ' + data['ref_standards']))
        doc.append(NoEscape(r'\nocite{ISO29119,IEC60068,ISO17025}'))
        doc.append(NoEscape(r'\printbibliography[heading=none]'))

    with doc.create(Section('Definitions and Abbreviations')):
        with doc.create(Itemize()) as item:
            item.append(NoEscape(data['definitions']))

    with doc.create(Section('Test Item Identification')):
        doc.append(NoEscape(r'\renewcommand{\arraystretch}{1.3}'))
        doc.append(NoEscape(r'\setlength{\tabcolsep}{3pt}'))
        fmt = r'|>{\centering\arraybackslash}m{2.9cm}|>{\centering\arraybackslash}m{2.9cm}|>{\centering\arraybackslash}m{2.9cm}|>{\centering\arraybackslash}m{2.9cm}|>{\centering\arraybackslash}m{3.2cm}|'
        with doc.create(Tabular(NoEscape(fmt))) as table:
            table.add_hline()
            table.add_row((NoEscape(r'\textbf{Name / Idem Number}'), NoEscape(r'\textbf{Serial Number / Revision}'), 
                           NoEscape(r'\textbf{Manufacturer}'), NoEscape(r'\textbf{Configuration (HW/SW)}'), 
                           NoEscape(r'\textbf{Photographs / Diagrams}')))
            table.add_hline()
            table.add_row((data['item_name'], data['item_sn'], data['item_mfr'], data['item_config'], "See Annexes"))
            table.add_hline()

    with doc.create(Section('Test Environment and Equipment')):
        doc.append(Subsection('Environmental Conditions'))
        with doc.create(Itemize()) as item:
            item.add_item(NoEscape(f"Ambient temperature: {data['temp']} °C"))
            item.add_item(NoEscape(f"Humidity: {data['humidity']} %"))
        
        doc.append(Subsection('Test Equipment'))
        # FIXED: Removed space before \hline to prevent "Misplaced \noalign" crash
        doc.append(Command('equipmenttable', NoEscape(data['equip_data'] + r'\\ \hline')))

    with doc.create(Section('Test Inputs, Outputs, and Acceptance Criteria')):
        doc.append(Subsection('Test Inputs'))
        doc.append(NoEscape(data['inputs']))
        doc.append(Subsection('Expected Outputs'))
        doc.append(NoEscape(data['outputs']))
        doc.append(Subsection('Acceptance Criteria'))
        doc.append(NoEscape(data['criteria']))

    with doc.create(Section('Test Procedure')):
        doc.append(NoEscape(r'\renewcommand{\arraystretch}{1.3}'))
        fmt_proc = r'|>{\centering\arraybackslash}m{0.9cm}|>{\centering\arraybackslash}m{3.5cm}|>{\centering\arraybackslash}m{3.5cm}|>{\centering\arraybackslash}m{3.5cm}|>{\centering\arraybackslash}m{3.5cm}|'
        with doc.create(Tabular(NoEscape(fmt_proc))) as table:
            table.add_hline()
            table.add_row((NoEscape(r'\textbf{Step}'), NoEscape(r'\textbf{Input Condition}'), 
                           NoEscape(r'\textbf{Expected Output}'), NoEscape(r'\textbf{Actual Output}'), 
                           NoEscape(r'\textbf{Pass/Fail}')))
            table.add_hline()
            table.append(NoEscape(data['proc_table']))
            # FIXED: Removed space before \hline to prevent "Misplaced \noalign" crash
            table.append(NoEscape(r'\\ \hline'))

    # ... (Rest of your sections remain exactly the same)
    with doc.create(Section('Results')):
        doc.append(Subsection('Raw Data'))
        doc.append(NoEscape(data['results_raw']))
        doc.append(Subsection('Analysis'))
        doc.append(NoEscape(data['results_analysis']))

    with doc.create(Section('Conclusion')):
        with doc.create(Itemize()) as item:
            item.add_item(NoEscape(r'\textbf{Overall Result:} ' + data['conclusion_res']))
            item.add_item(NoEscape(r'\textbf{Key Observations:} ' + data['conclusion_obs']))

    with doc.create(Section('Signatures')):
        doc.append(NoEscape(r'\makeatletter'))
        sig_row = NoEscape(data['approved_by'] + r' & Approver & ' + data['date'] + r' & \\ \hline')
        doc.append(Command('signatureTable', sig_row))
        doc.append(NoEscape(r'\makeatother'))

    with doc.create(Section('Annexes')):
        with doc.create(Itemize()) as item:
            item.append(NoEscape(data['annexes_list']))

    # --- GENERATION AND FILE MANAGEMENT ---
    file_base_name = f"Report_{data['doc_id']}"
    
    try:
        print(f"-> Generating PDF...")
        # Step 1: Generate locally so ../common paths work
        doc.generate_pdf(file_base_name, clean_tex=False, compiler='pdflatex')
        
        # Step 2: Define Move logic
        generated_pdf = file_base_name + ".pdf"
        final_destination = os.path.join(target_dir, generated_pdf)
        
        if os.path.exists(generated_pdf):
            if os.path.exists(final_destination):
                os.remove(final_destination)
            shutil.move(generated_pdf, final_destination)
            print(f"SUCCESS: Moved to {final_destination}")

    except Exception as e:
        print(f"LATEX ERROR: {e}")
        
    finally:
        # Cleanup LaTeX trash in the current directory
        time.sleep(1)
        garbage = ['.aux', '.log', '.out', '.toc', '.fdb_latexmk', '.fls', '.run.xml', '.bcf', '.blg', '.bbl', '.tex', '-blx.bib', '.bib']
        for ext in garbage:
            trash = file_base_name + ext
            if os.path.exists(trash):
                try: os.remove(trash)
                except: pass

def run_automation(csv_file):
    if not os.path.exists(csv_file):
        print(f"CSV Not Found: {csv_file}")
        return
    with open(csv_file, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            clean_row = {k.strip(): v.strip() for k, v in row.items()}
            create_test_report(clean_row)

if __name__ == "__main__":
    run_automation('test.csv')