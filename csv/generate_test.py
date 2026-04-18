import csv
import os
import time
from pylatex import Document, Section, Subsection, Command, Itemize, Tabular
from pylatex.utils import NoEscape

def create_test_report(data):
    # 1. Document Setup
    doc = Document(
        documentclass=NoEscape('../common/latex/delta_base_styles/delta_base_styles'),
        fontenc='T1',
        inputenc='utf8',
        lmodern=True
    )

    # 2. Preamble & Styles
    doc.preamble.append(Command('addbibresource', 'example_refs.bib'))
    doc.preamble.append(NoEscape(r'\subimport{../common/latex/delta_header/}{delta_header.tex}'))
    doc.preamble.append(NoEscape(r'\subimport{../common/latex/equipment_table/}{equipment_table.tex}'))
    doc.preamble.append(NoEscape(r'\subimport{../common/latex/signature_table/}{signature_table.tex}'))
    doc.preamble.append(NoEscape(r'\subimport{../common/latex/version_approval_table/}{version_approval_table.tex}'))
    # Aseguramos la ruta de las imágenes
    doc.preamble.append(NoEscape(r'\graphicspath{{../common/images/}{../common/latex/delta_header/}{./}}'))

    # Metadata
    doc.preamble.append(Command('doctitle', data['title']))
    doc.preamble.append(Command('docsubtitle', data['subtitle']))
    doc.preamble.append(Command('docid', data['doc_id']))
    doc.preamble.append(Command('version', data['version']))
    doc.preamble.append(Command('docdate', data['date']))
    doc.preamble.append(Command('preparedby', data['prepared_by']))
    doc.preamble.append(Command('approvedby', data['approved_by']))
    doc.preamble.append(Command('observations', 'Automated Generation'))

    # --- DOCUMENT BODY ---
    doc.append(NoEscape(r'\makedeltaheader'))
    # AJUSTE: Añadimos espacio vertical después del header
    doc.append(NoEscape(r'\par\vspace{0.5cm}'))

    # SECTION 1: Test plan summary (WITH TEST NAME)
    with doc.create(Section('Test plan summary')):
        doc.append(NoEscape(r'\textbf{Name of the test:} ' + data['test_name'] + r'\\[0.2cm]'))
        doc.append(NoEscape(r'\makeversionapprovaltable'))

    # SECTION 2: Purpose and scope
    with doc.create(Section('Purpose and scope')):
        doc.append(NoEscape(r'\textcolor{DarkCyan}{Explain why the test is being performed and what it consists of.}'))
        with doc.create(Itemize()) as item:
            item.add_item(NoEscape(r'\textbf{Main objective:} ' + data['purpose_obj']))
            item.add_item(NoEscape(r'\textbf{Limits:} ' + data['purpose_limits']))
            item.add_item(NoEscape(r'\textbf{Key focus areas:} ' + data['purpose_focus']))

    # SECTION 3: References
    with doc.create(Section('References')):
        with doc.create(Itemize()) as item:
            item.add_item(NoEscape(r'\textbf{Standards:} ' + data['ref_standards']))
        doc.append(NoEscape(r'\printbibliography[heading=none]'))

    # SECTION 4: Definitions and Abbreviations
    with doc.create(Section('Definitions and Abbreviations')):
        with doc.create(Itemize()) as item:
            item.append(NoEscape(data['definitions']))

    # SECTION 5: Test Item Identification
    with doc.create(Section('Test Item Identification')):
        doc.append(NoEscape(r'\renewcommand{\arraystretch}{1.3}'))
        with doc.create(Tabular('|p{2.9cm}|p{2.9cm}|p{2.9cm}|p{2.9cm}|p{3.2cm}|')) as table:
            table.add_hline()
            table.add_row((NoEscape(r'\textbf{Name / No.}'), NoEscape(r'\textbf{S/N / Rev}'), 
                           NoEscape(r'\textbf{Mfr}'), NoEscape(r'\textbf{Config}'), 
                           NoEscape(r'\textbf{Photos}')))
            table.add_hline()
            table.add_row((data['item_name'], data['item_sn'], data['item_mfr'], data['item_config'], "See Annex"))
            table.add_hline()

    # SECTION 6: Environment
    with doc.create(Section('Test Environment and Equipment')):
        doc.append(Subsection('Environmental Conditions'))
        with doc.create(Itemize()) as item:
            item.add_item(NoEscape(f"Ambient temperature: {data['temp']} °C"))
            item.add_item(NoEscape(f"Humidity: {data['humidity']} %"))
        
        doc.append(Subsection('Test Equipment'))
        doc.append(Command('equipmenttable', NoEscape(data['equip_data'] + r' \\ \hline')))

    # SECTION 7 & 8: Procedure
    with doc.create(Section('Test Inputs, Outputs, and Acceptance Criteria')):
        doc.append(NoEscape(r'\subsection{Test Inputs} ' + data['inputs']))
        doc.append(NoEscape(r'\subsection{Expected Outputs} ' + data['outputs']))
        doc.append(NoEscape(r'\subsection{Acceptance Criteria} ' + data['criteria']))

    with doc.create(Section('Test Procedure')):
        doc.append(NoEscape(r'\renewcommand{\arraystretch}{1.3}'))
        with doc.create(Tabular('|p{0.9cm}|p{3.5cm}|p{3.5cm}|p{3.5cm}|p{3.5cm}|')) as table:
            table.add_hline()
            table.add_row((NoEscape(r'\textbf{Step}'), NoEscape(r'\textbf{Input}'), 
                           NoEscape(r'\textbf{Expected}'), NoEscape(r'\textbf{Actual}'), 
                           NoEscape(r'\textbf{Pass/Fail}')))
            table.add_hline()
            table.append(NoEscape(data['proc_table']))
            table.append(NoEscape(r' \\ \hline'))

    # SECTION 9: Results
    with doc.create(Section('Results')):
        doc.append(Subsection('Raw Data'))
        doc.append(NoEscape(data['results_raw']))
        doc.append(Subsection('Analysis'))
        doc.append(NoEscape(data['results_analysis']))

    # SECTION 10: Conclusion
    with doc.create(Section('Conclusion')):
        with doc.create(Itemize()) as item:
            item.add_item(NoEscape(r'\textbf{Overall Result:} ' + data['conclusion_res']))
            item.add_item(NoEscape(r'\textbf{Key Observations:} ' + data['conclusion_obs']))

    # SECTION 11: Signatures
    with doc.create(Section('Signatures')):
        doc.append(NoEscape(r'\makeatletter'))
        doc.append(Command('signatureTable', NoEscape(r'\@approvedby & Approver & \@docdate & \\ \hline')))
        doc.append(NoEscape(r'\makeatother'))

    # SECTION 12: Annexes
    with doc.create(Section('Annexes')):
        with doc.create(Itemize()) as item:
            item.append(NoEscape(data['annexes_list']))

    # --- GENERATION ---
    file_name = f"Report_{data['doc_id']}"
    try:
        doc.generate_pdf(file_name, clean_tex=True, compiler='pdflatex')
        print(f"Success: {file_name}.pdf generated.")
    except Exception as e:
        print(f"Error in {file_name}: {e}")
    finally:
        time.sleep(1)
        garbage = ['.aux', '.log', '.out', '.toc', '.fdb_latexmk', '.fls', '.run.xml', '.bcf', '.blg', '.bbl','.tex','.bib']
        for ext in garbage:
            target = f"{file_name}{ext}"
            if os.path.exists(target):
                try: os.remove(target)
                except: pass

def run_automation(csv_file):
    if not os.path.exists(csv_file): return
    with open(csv_file, mode='r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            create_test_report({k.strip(): v.strip() for k, v in row.items()})

if __name__ == "__main__":
    run_automation('prueba.csv')