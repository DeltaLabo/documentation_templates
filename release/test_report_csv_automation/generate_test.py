import csv
import os
import time
import shutil 
from pylatex import Document, Section, Subsection, Command, Itemize, Tabular
from pylatex.utils import NoEscape

def get_merged_data(target_id, csv_folder="."):
    # 1. Definimos todos los campos que el PDF necesita para que nunca de error 'KeyError'
    all_fields = [
        'title', 'subtitle', 'doc_id', 'version', 'date', 'prepared_by', 
        'approved_by', 'observations', 'test_name', 'purpose_obj', 
        'purpose_limits', 'purpose_focus', 'ref_standards', 'definitions', 
        'item_name', 'item_sn', 'item_mfr', 'item_config', 'temp', 
        'humidity', 'equip_data', 'inputs', 'outputs', 'criteria', 
        'proc_table', 'results_raw', 'results_analysis', 'conclusion_res', 
        'conclusion_obs', 'annexes_list'
    ]
    
    # Inicializamos todo con un espacio en blanco
    combined_row = {field: " " for field in all_fields}
    combined_row['doc_id'] = target_id
    
    csv_files = [
        "01_metadata.csv", 
        "02_scope.csv", 
        "03_item_environment.csv", 
        "04_procedure.csv", 
        "05_results.csv"
    ]
    
    print(f"\n[Analizando ID: {target_id}]")
    
    for filename in csv_files:
        path = os.path.join(csv_folder, filename)
        found_in_file = False
        
        if os.path.exists(path):
            with open(path, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('doc_id', '').strip() == target_id:
                        # Actualizamos los datos encontrados (limpiando espacios)
                        combined_row.update({k.strip(): v.strip() for k, v in row.items()})
                        found_in_file = True
                        break
            
            if not found_in_file:
                print(f"  >>> ERROR: El ID '{target_id}' NO se encontró en: {filename}")
            else:
                print(f"  OK: Datos cargados de {filename}")
        else:
            print(f"  ! ADVERTENCIA: El archivo {filename} no existe en la carpeta.")
            
    return combined_row

def create_test_report(data):
    print(f"-> Generando PDF para: {data['doc_id']}...")
    
    target_dir = os.path.join(data['doc_id'], 'PDF')
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    doc = Document(
        documentclass=NoEscape('../../common/latex/delta_base_styles/delta_base_styles'),
        fontenc='T1', inputenc='utf8', lmodern=True
    )
    
    # Preámbulo
    doc.preamble.append(Command('addbibresource', 'example_refs.bib'))
    doc.preamble.append(NoEscape(r'\subimport{../../common/latex/delta_header/}{delta_header.tex}'))
    doc.preamble.append(NoEscape(r'\subimport{../../common/latex/equipment_table/}{equipment_table.tex}'))
    doc.preamble.append(NoEscape(r'\subimport{../../common/latex/signature_table/}{signature_table.tex}'))
    doc.preamble.append(NoEscape(r'\subimport{../../common/latex/version_approval_table/}{version_approval_table.tex}'))
    doc.preamble.append(NoEscape(r'\graphicspath{{../../common/latex/delta_base_styles/}{../../common/latex/delta_header/}{../../common/images/}}'))

    # Mapeo de datos (Como inicializamos combined_row con espacios, esto no fallará)
    doc.preamble.append(Command('doctitle', data['title']))
    doc.preamble.append(Command('docsubtitle', data['subtitle']))
    doc.preamble.append(Command('docid', data['doc_id']))
    doc.preamble.append(Command('version', data['version']))
    doc.preamble.append(Command('docdate', data['date']))
    doc.preamble.append(Command('preparedby', data['prepared_by']))
    doc.preamble.append(Command('approvedby', data['approved_by']))
    doc.preamble.append(Command('observations', data['observations']))

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
            # Si definitions está vacío, ponemos un ítem vacío para que LaTeX no falle
            item.append(NoEscape(data['definitions'] if data['definitions'].strip() else r'\item '))

    with doc.create(Section('Test Item Identification')):
        doc.append(NoEscape(r'\renewcommand{\arraystretch}{1.3}'))
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
        # Aseguramos formato de tabla si equip_data está vacío
        equip = data['equip_data'] if data['equip_data'].strip() else " & & & & & & "
        doc.append(Command('equipmenttable', NoEscape(equip + r'\\ \hline')))

    with doc.create(Section('Test Inputs, Outputs, and Acceptance Criteria')):
        doc.append(Subsection('Test Inputs')); doc.append(NoEscape(data['inputs']))
        doc.append(Subsection('Expected Outputs')); doc.append(NoEscape(data['outputs']))
        doc.append(Subsection('Acceptance Criteria')); doc.append(NoEscape(data['criteria']))

    with doc.create(Section('Test Procedure')):
        doc.append(NoEscape(r'\renewcommand{\arraystretch}{1.3}'))
        fmt_proc = r'|>{\centering\arraybackslash}m{0.9cm}|>{\centering\arraybackslash}m{3.5cm}|>{\centering\arraybackslash}m{3.5cm}|>{\centering\arraybackslash}m{3.5cm}|>{\centering\arraybackslash}m{3.5cm}|'
        with doc.create(Tabular(NoEscape(fmt_proc))) as table:
            table.add_hline()
            table.add_row((NoEscape(r'\textbf{Step}'), NoEscape(r'\textbf{Input Condition}'), 
                           NoEscape(r'\textbf{Expected Output}'), NoEscape(r'\textbf{Actual Output}'), 
                           NoEscape(r'\textbf{Pass/Fail}')))
            table.add_hline()
            # Aseguramos formato si proc_table está vacío
            proc = data['proc_table'] if data['proc_table'].strip() else " & & & & "
            table.append(NoEscape(proc))
            table.append(NoEscape(r'\\ \hline'))

    with doc.create(Section('Results')):
        doc.append(Subsection('Raw Data')); doc.append(NoEscape(data['results_raw']))
        doc.append(Subsection('Analysis')); doc.append(NoEscape(data['results_analysis']))

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
            item.append(NoEscape(data['annexes_list'] if data['annexes_list'].strip() else r'\item '))

    file_name = f"Report_{data['doc_id']}"
    
    try:
        # Intentamos generar el PDF. clean_tex=False para que el borrado lo controlemos nosotros.
        doc.generate_pdf(file_name, clean_tex=False, compiler='pdflatex')
    except Exception as e:
        # Imprimimos el error de LaTeX pero NO detenemos el programa
        print(f"  ! Nota: LaTeX reportó una advertencia o error (ej. logo faltante).")

    # Verificamos si el archivo se creó (aunque LaTeX haya dado error de status 1)
    if os.path.exists(file_name + ".pdf"):
        final_pdf_path = os.path.join(target_dir, file_name + ".pdf")
        if os.path.exists(final_pdf_path): os.remove(final_pdf_path)
        shutil.move(file_name + ".pdf", final_pdf_path)
        print(f"  >>> ÉXITO: PDF guardado en {final_pdf_path}")
    else:
        print(f"  >>> ERROR CRÍTICO: No se pudo generar el PDF para {data['doc_id']}.")

    # Limpieza de archivos temporales
    time.sleep(0.5)
    extensions = ['.aux', '.log', '.out', '.toc', '.fdb_latexmk', '.fls', '.run.xml', '.bcf', '.blg', '.bbl', '.tex', '.bib', '-blx.bib']
    for ext in extensions:
        trash = file_name + ext
        if os.path.exists(trash):
            try: os.remove(trash)
            except: pass

def run_modular_automation():
    # Escaneamos todos los archivos para encontrar CUALQUIER ID
    csv_files = ["01_metadata.csv", "02_scope.csv", "03_item_environment.csv", "04_procedure.csv", "05_results.csv"]
    all_ids = set()
    
    for filename in csv_files:
        if os.path.exists(filename):
            with open(filename, mode='r', encoding='utf-8-sig') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('doc_id'):
                        all_ids.add(row['doc_id'].strip())
    
    if not all_ids:
        print("No se encontraron IDs en ningún CSV.")
        return

    for doc_id in sorted(list(all_ids)):
        full_data = get_merged_data(doc_id)
        create_test_report(full_data)

if __name__ == "__main__":
    run_modular_automation()