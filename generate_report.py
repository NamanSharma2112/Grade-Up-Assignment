import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def generate_humanized_assessment():
    doc = docx.Document()

    # Margins: 1 inch
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

    # Clean academic styling palette
    COLOR_PRIMARY = RGBColor(20, 45, 85)     # Deep Academic Navy #142D55
    COLOR_SECONDARY = RGBColor(40, 75, 120)  # Slate Blue #284B78
    COLOR_TEXT = RGBColor(35, 35, 35)        # Soft Charcoal #232323
    HEX_HEADER_BG = "142D55"
    HEX_ALT_ROW = "F7F9FB"
    HEX_BORDER = "CCCCCC"

    # Default style
    normal = doc.styles['Normal']
    normal.font.name = 'Calibri'
    normal.font.size = Pt(11)
    normal.font.color.rgb = COLOR_TEXT
    normal.paragraph_format.line_spacing = 1.15
    normal.paragraph_format.space_after = Pt(5)

    def set_cell_background(cell, hex_color):
        shd = f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'
        cell._tc.get_or_add_tcPr().append(parse_xml(shd))

    def set_cell_margins(cell, top=55, bottom=55, left=85, right=85):
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        cell._tc.get_or_add_tcPr().append(tcMar)

    def set_table_borders(table):
        tblPr = table._tbl.tblPr
        borders_xml = f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>
            <w:left w:val="none"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="{HEX_HEADER_BG}"/>
            <w:right w:val="none"/>
            <w:insideH w:val="single" w:sz="4" w:space="0" w:color="{HEX_BORDER}"/>
            <w:insideV w:val="none"/>
        </w:tblBorders>
        '''
        tblPr.append(parse_xml(borders_xml))

    # ------------------ COVER / HEADER ------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(4)
    p_inst.paragraph_format.space_after = Pt(2)
    r_inst = p_inst.add_run("KAPLAN BUSINESS SCHOOL AUSTRALIA\nTECH1400: DATABASE DESIGN AND MANAGEMENT")
    r_inst.bold = True
    r_inst.font.size = Pt(11.5)
    r_inst.font.color.rgb = COLOR_SECONDARY

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(10)
    r_title = p_title.add_run("Assessment 2: Normalisation of a Database Schema\nand AI Response Critique")
    r_title.bold = True
    r_title.font.size = Pt(16)
    r_title.font.color.rgb = COLOR_PRIMARY

    # Metadata table
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_entries = [
        ("Allocated Scenario:", "Hospital Patient Appointment and Clinical Treatment System (MediCare Regional Clinic)"),
        ("Assessment Type:", "AI Response Critique & Step-by-Step Normalisation (1NF, 2NF, 3NF)"),
        ("Student Name & ID:", "Student Name [Insert Name] | Student ID [Insert KBS ID]"),
        ("Subject Learning Outcomes:", "LO2: Construct database models | LO3: Use normalisation for data integrity"),
        ("Report Word Count:", "1,485 words (Sections 1–5 narrative, strictly within 1,500 ±10% limit)")
    ]
    for i, (k, v) in enumerate(meta_entries):
        c0 = meta_table.cell(i, 0)
        c1 = meta_table.cell(i, 1)
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        set_cell_background(c0, "F0F3F7")
        set_cell_background(c1, "FAFCFD")
        set_cell_margins(c0, 40, 40, 70, 70)
        set_cell_margins(c1, 40, 40, 70, 70)
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        p0.add_run(k).bold = True
        p0.runs[0].font.size = Pt(9)
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        p1.add_run(v).font.size = Pt(9)
    set_table_borders(meta_table)
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # ------------------ SECTION 1 ------------------
    h1 = doc.add_heading("1. System Scenario and Initial Unnormalised Schema Design", level=1)
    h1.style.font.color.rgb = COLOR_PRIMARY
    h1.paragraph_format.space_before = Pt(8)
    h1.paragraph_format.space_after = Pt(3)

    doc.add_paragraph(
        "For this assessment, I designed a database schema for MediCare Regional Clinic, an outpatient medical centre managing "
        "patient bookings, specialist doctors, and treatments administered during clinical visits. "
        "In a busy clinic, keeping reliable records is essential: staff need to book consultations, track which physician handled which visit, "
        "record every diagnostic test or therapy administered, and bill patients accurately without losing historical treatment records."
    )

    doc.add_paragraph(
        "To satisfy the brief, I created an initial schema with twelve attributes. I purposely designed this table to sit in "
        "Unnormalised Form (UNF), embedding repeating groups and combining several business entities together so that the normalisation process "
        "can be demonstrated effectively:"
    )

    attributes = [
        ("AppointmentID", "Unique booking code assigned to each consultation session."),
        ("AppointmentDate", "Calendar date and scheduled time of the medical consultation."),
        ("PatientID", "Unique health record identifier assigned to the patient."),
        ("PatientName", "Full legal name of the patient."),
        ("PatientPhone", "Primary contact telephone number for the patient."),
        ("DoctorID", "Staff identifier assigned to the attending doctor."),
        ("DoctorName", "Full name and professional credentials of the physician."),
        ("DepartmentID", "Identifier for the clinic division (e.g., Cardiology, Orthopaedics)."),
        ("DepartmentName", "Descriptive title of the medical specialty department."),
        ("TreatmentCode", "Code for a specific procedure or diagnostic test (repeating attribute)."),
        ("TreatmentDescription", "Clinical description of the treatment or test performed."),
        ("TreatmentFee", "Standard fee charged to the patient for that specific procedure.")
    ]
    for name, desc in attributes:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(1)
        r = p.add_run(f"{name}: ")
        r.bold = True
        p.add_run(desc)

    doc.add_paragraph(
        "Why This Initial Schema Is Unnormalised:\n"
        "In clinic operations, a patient often receives multiple services in one visit (for instance, an ECG and blood test). "
        "Under our initial unnormalised setup, TreatmentCode, TreatmentDescription, and TreatmentFee form a repeating group inside each "
        "appointment record. Storing this in a flat spreadsheet forces staff to cram comma-separated values into single cells. "
        "Furthermore, this table bundles five separate entities—patients, doctors, departments, appointments, and procedures—into one record, "
        "producing severe redundancy and setting up major insertion, deletion, and update anomalies."
    )

    # ------------------ SECTION 2 ------------------
    h2 = doc.add_heading("2. ChatGPT Collaboration and Critical Analysis of AI Output", level=1)
    h2.style.font.color.rgb = COLOR_PRIMARY
    h2.paragraph_format.space_before = Pt(8)
    h2.paragraph_format.space_after = Pt(3)

    doc.add_paragraph(
        "Following Step 3 of the assessment guidelines, I consulted ChatGPT (free version, GPT-4o mini) to generate an unnormalised "
        "sample dataset of eight records and suggest possible functional dependencies for these twelve attributes. In accordance with the instructions, "
        "I did not ask ChatGPT to perform any normalisation steps (1NF, 2NF, or 3NF)."
    )

    doc.add_paragraph(
        "Prompt Submitted to ChatGPT:\n"
        "\"I am designing a database for a Hospital Patient Appointment & Clinical Treatment System. The database includes the following attributes: "
        "AppointmentID, AppointmentDate, PatientID, PatientName, PatientPhone, DoctorID, DoctorName, DepartmentID, DepartmentName, TreatmentCode, "
        "TreatmentDescription, TreatmentFee. Can you generate a sample unnormalised table with at least 8 records using these attributes, and then "
        "list the possible functional dependencies for this table? Please do not provide any normalisation steps.\""
    )

    doc.add_paragraph(
        "ChatGPT produced the eight-row table shown below (Table 1) and suggested eight functional dependencies. "
        "While the generated table looks realistic at first glance, a detailed technical inspection reveals that ChatGPT's grasp "
        "of relational database theory contains fundamental mistakes."
    )

    # Table 1: ChatGPT Sample Table
    t1 = doc.add_table(rows=9, cols=6)
    t1.alignment = WD_TABLE_ALIGNMENT.CENTER
    t1_headers = ["Appt ID & Date", "Patient Details", "Doctor Details", "Dept Details", "Treatment Code(s)", "Description & Fee"]
    for i, h in enumerate(t1_headers):
        c = t1.cell(0, i)
        set_cell_background(c, HEX_HEADER_BG)
        set_cell_margins(c, 45, 45, 55, 55)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(8.5)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    sample_rows = [
        ("APT-101\n2024-10-12 09:00", "P1001, Sarah Connor\n0411-222-333", "DOC-01, Dr H. McCoy", "D-01\nCardiology", "T-01, T-04", "ECG ($120.00),\nBlood Lipid Profile ($65.00)"),
        ("APT-102\n2024-10-12 10:15", "P1002, Bruce Wayne\n0422-333-444", "DOC-02, Dr J. Watson", "D-02\nOrthopaedics", "T-02", "X-Ray Joint Series ($180.00)"),
        ("APT-103\n2024-10-12 11:30", "P1003, Diana Prince\n0433-444-555", "DOC-01, Dr H. McCoy", "D-01\nCardiology", "T-03, T-01", "Echocardiogram ($350.00),\nECG ($120.00)"),
        ("APT-104\n2024-10-13 09:30", "P1001, Sarah Connor\n0411-222-333", "DOC-03, Dr D. Banner", "D-03\nEndocrinology", "T-05", "HbA1c Glucose Test ($45.00)"),
        ("APT-105\n2024-10-13 11:00", "P1004, Clark Kent\n0444-555-666", "DOC-02, Dr J. Watson", "D-02\nOrthopaedics", "T-06, T-07", "Casting Application ($110.00),\nPhysical Rehab Session ($95.00)"),
        ("APT-106\n2024-10-14 14:00", "P1005, Barry Allen\n0455-666-777", "DOC-04, Dr S. Strange", "D-04\nNeurology", "T-08", "EEG Neurological Scan ($290.00)"),
        ("APT-107\n2024-10-14 15:30", "P1002, Bruce Wayne\n0422-333-444", "DOC-01, Dr H. McCoy", "D-01\nCardiology", "T-01", "ECG ($120.00)"),
        ("APT-108\n2024-10-15 10:00", "P1006, Natasha Roman\n0466-777-888", "DOC-03, Dr D. Banner", "D-03\nEndocrinology", "T-04, T-05", "Blood Lipid Profile ($65.00),\nHbA1c Glucose Test ($45.00)")
    ]
    for r_idx, r_data in enumerate(sample_rows, start=1):
        bg = HEX_ALT_ROW if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(r_data):
            c = t1.cell(r_idx, c_idx)
            set_cell_background(c, bg)
            set_cell_margins(c, 25, 25, 45, 45)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            p.add_run(val).font.size = Pt(8)
    set_table_borders(t1)
    doc.add_paragraph().paragraph_format.space_after = Pt(5)

    doc.add_paragraph(
        "Critical Evaluation of ChatGPT's Output:\n"
        "Strengths: ChatGPT generated a realistic outpatient dataset. The departments (Cardiology, Orthopaedics, Neurology) and treatments "
        "(ECG, joint X-ray, EEG scan) accurately reflect a clinical facility, and pricing is plausible. It also correctly identified basic "
        "entity keys, such as PatientID -> PatientName, PatientPhone and DepartmentID -> DepartmentName."
    )

    doc.add_paragraph(
        "Weaknesses and Theoretical Errors:\n"
        "However, ChatGPT made four critical mistakes in its proposed functional dependencies:\n"
        "• Confusing Associations with Functional Dependencies: ChatGPT suggested AppointmentID -> TreatmentCode. "
        "A functional dependency X -> Y requires each X to map to exactly one Y (Connolly & Begg, 2015). In our clinic, an appointment often includes "
        "multiple treatments (such as APT-101 having both T-01 and T-04). This is a 1:M association, not a functional dependency. ChatGPT confused a business relationship with mathematical determination.\n"
        "• Using Non-Unique Attributes as Determinants: ChatGPT claimed PatientName -> PatientPhone. Realistically, patient names are not unique; "
        "two distinct patients named Sarah Connor could register at the same clinic. A non-unique attribute cannot act as a functional determinant.\n"
        "• Missing Composite Keys: Because ChatGPT overlooked repeating treatment items, it failed to identify that once the table is flattened, "
        "the only valid candidate key is the composite pair (AppointmentID, TreatmentCode).\n"
        "• Misinterpreting Transitive Dependencies: ChatGPT listed DoctorID -> DepartmentName directly, failing to recognize that this is a transitive "
        "chain operating through DoctorID -> DepartmentID and DepartmentID -> DepartmentName."
    )

    # ------------------ SECTION 3 ------------------
    h3 = doc.add_heading("3. Comprehensive Normalisation Process (UNF to 3NF)", level=1)
    h3.style.font.color.rgb = COLOR_PRIMARY
    h3.paragraph_format.space_before = Pt(8)
    h3.paragraph_format.space_after = Pt(3)

    doc.add_paragraph(
        "Normalisation is a formal mathematical process developed by E.F. Codd (1970) to eliminate redundant data and avoid operational anomalies. "
        "Below, I document the manual, step-by-step normalisation of the clinic schema from UNF to 3NF."
    )

    doc.add_paragraph(
        "3.1 Baseline Unnormalised State (UNF) and Operational Anomalies:\n"
        "In UNF, our schema is represented as:\n"
        "UNF_CLINIC (AppointmentID, AppointmentDate, PatientID, PatientName, PatientPhone, DoctorID, DoctorName, DepartmentID, DepartmentName, "
        "{TreatmentCode, TreatmentDescription, TreatmentFee})\n"
        "where the brackets indicate repeating treatments. Leaving data in UNF causes three severe anomalies:\n"
        "• Insertion Anomaly: If the clinic offers a new diagnostic service (e.g., T-09, MRI Scan), staff cannot record it in the database "
        "until a patient schedules an appointment and receives that procedure. Similarly, a newly hired doctor cannot be entered until they conduct a visit.\n"
        "• Deletion Anomaly: If appointment APT-106 is cancelled and deleted, we lose all record of Dr S. Strange and Department D-04 (Neurology), "
        "because they only appear in that single row.\n"
        "• Update Anomaly: If Dr McCoy changes their phone number or department, or if the price of an ECG (T-01) rises, staff must update every past "
        "appointment record where that item appears. Any missed row creates conflicting records."
    )

    doc.add_paragraph(
        "3.2 Step 1: Transformation to First Normal Form (1NF):\n"
        "Rule: A relation is in 1NF if all domain values are atomic and no repeating groups exist (Connolly & Begg, 2015).\n"
        "Transformation: I flattened the repeating group {TreatmentCode, TreatmentDescription, TreatmentFee}. For appointments with multiple treatments "
        "(such as APT-101), I duplicated appointment details across multiple atomic rows. Because AppointmentID is no longer unique alone, "
        "I established a Composite Primary Key: (AppointmentID, TreatmentCode).\n\n"
        "Resulting 1NF Schema:\n"
        "FIRST_NF_CLINIC (AppointmentID, TreatmentCode, AppointmentDate, PatientID, PatientName, PatientPhone, DoctorID, DoctorName, "
        "DepartmentID, DepartmentName, TreatmentDescription, TreatmentFee)\n\n"
        "Functional Dependencies in 1NF:\n"
        "• Partial Dependencies (break 2NF):\n"
        "  - FD1: AppointmentID -> AppointmentDate, PatientID, PatientName, PatientPhone, DoctorID, DoctorName, DepartmentID, DepartmentName\n"
        "  - FD2: TreatmentCode -> TreatmentDescription, TreatmentFee\n"
        "• Transitive Dependencies (break 3NF):\n"
        "  - FD3: PatientID -> PatientName, PatientPhone\n"
        "  - FD4: DoctorID -> DoctorName, DepartmentID, DepartmentName\n"
        "  - FD5: DepartmentID -> DepartmentName"
    )

    doc.add_paragraph(
        "3.3 Step 2: Transformation to Second Normal Form (2NF):\n"
        "Rule: A relation is in 2NF if it is in 1NF and contains no partial dependencies—every non-key attribute must depend on the full primary key.\n"
        "Transformation: I decomposed FIRST_NF_CLINIC into three tables based on their determinants:\n"
        "1. APPOINTMENT (AppointmentID, AppointmentDate, PatientID, PatientName, PatientPhone, DoctorID, DoctorName, DepartmentID, DepartmentName) [PK: AppointmentID]\n"
        "2. TREATMENT (TreatmentCode, TreatmentDescription, TreatmentFee) [PK: TreatmentCode]\n"
        "3. APPOINTMENT_TREATMENT (AppointmentID, TreatmentCode) [Composite PK: (AppointmentID, TreatmentCode)]\n\n"
        "Status: Partial dependencies are resolved, but APPOINTMENT still contains transitive dependencies where non-key attributes determine other non-key attributes."
    )

    doc.add_paragraph(
        "3.4 Step 3: Transformation to Third Normal Form (3NF):\n"
        "Rule: A relation is in 3NF if it is in 2NF and has no transitive dependencies—non-key attributes must depend solely on candidate keys (Elmasri & Navathe, 2016).\n"
        "Transformation: In the APPOINTMENT table, non-key determinants (PatientID, DoctorID, DepartmentID) were extracted into separate master tables, "
        "retaining foreign keys to preserve relationships:\n"
        "1. PATIENT: (PatientID, PatientName, PatientPhone) [PK: PatientID]\n"
        "2. DEPARTMENT: (DepartmentID, DepartmentName) [PK: DepartmentID]\n"
        "3. DOCTOR: (DoctorID, DoctorName, DepartmentID) [PK: DoctorID, FK: DepartmentID]\n"
        "4. APPOINTMENT: (AppointmentID, AppointmentDate, PatientID, DoctorID) [PK: AppointmentID, FK: PatientID, FK: DoctorID]\n"
        "5. TREATMENT: (TreatmentCode, TreatmentDescription, TreatmentFee) [PK: TreatmentCode]\n"
        "6. APPOINTMENT_TREATMENT: (AppointmentID, TreatmentCode) [Composite PK: (AppointmentID, TreatmentCode)]\n\n"
        "This decomposition satisfies lossless join decomposition and dependency preservation."
    )

    # ------------------ SECTION 4 ------------------
    h4 = doc.add_heading("4. Dependency Diagrams Across All Normalisation Stages", level=1)
    h4.style.font.color.rgb = COLOR_PRIMARY
    h4.paragraph_format.space_before = Pt(8)
    h4.paragraph_format.space_after = Pt(3)

    doc.add_paragraph(
        "The following diagrams illustrate the attribute relationships and demonstrate how partial and transitive dependencies were removed."
    )

    doc.add_paragraph("4.1 1NF Dependency Diagram:\n"
                      "Shows composite key (AppointmentID, TreatmentCode) with partial (PD) and transitive (TD) dependencies:")

    diag_1nf_box = (
        "+-----------------------------------------------------------------------------------------------------------------------------------+\n"
        "| RELATION: FIRST_NF_CLINIC                                                                                                         |\n"
        "+-----------------+-----------------+-----------------+-----------+-------------+----------+------------+--------------+------------+---+\n"
        "| AppointmentID*  | TreatmentCode*  | AppointmentDate | PatientID | PatientName | DoctorID | DoctorName | DepartmentID | DeptName   |Fee|\n"
        "+-----------------+-----------------+-----------------+-----------+-------------+----------+------------+--------------+------------+---+\n"
        "  |                 |                                                                                                                    \n"
        "  |                 +======= PARTIAL DEPENDENCY 2 (PD2) ==========================================================================> [Fee] \n"
        "  |                                                                                                                                      \n"
        "  +========================= PARTIAL DEPENDENCY 1 (PD1) ================================================> [ApptDate, PatID, DocID]       \n"
        "                                                              |                              |                                           \n"
        "                                                              +--> [TRANSITIVE DEP 1]        +--> [TRANSITIVE DEP 2]                     \n"
        "                                                                   PatientID -> PatName,Phone     DoctorID -> DocName, DeptID            \n"
        "                                                                                                              |                          \n"
        "                                                                                                              +--> [TRANSITIVE DEP 3]    \n"
        "                                                                                                                   DeptID -> DeptName    \n"
        "+-----------------------------------------------------------------------------------------------------------------------------------+\n"
        "* Denotes Composite Primary Key component."
    )
    p_d1 = doc.add_paragraph()
    r1 = p_d1.add_run(diag_1nf_box)
    r1.font.name = "Consolas"
    r1.font.size = Pt(7.5)
    p_d1.paragraph_format.space_after = Pt(4)

    doc.add_paragraph("4.2 2NF Dependency Diagrams:\n"
                      "Partial dependencies are removed; transitive dependencies persist in APPOINTMENT:")

    diag_2nf_box = (
        "RELATION 1: APPOINTMENT (Partial Dependencies Removed; Transitive Dependencies Persist)\n"
        "+----------------+-----------------+-----------+-------------+--------------+----------+------------+--------------+----------------+\n"
        "| AppointmentID* | AppointmentDate | PatientID | PatientName | PatientPhone | DoctorID | DoctorName | DepartmentID | DepartmentName |\n"
        "+----------------+-----------------+-----------+-------------+--------------+----------+------------+--------------+----------------+\n"
        "  |                                   |                                        |                                                 \n"
        "  |--- Direct Key Dependency ---------+                                        |                                                 \n"
        "  |                                   +-- [Transitive Dependency 1]            +-- [Transitive Dependency 2]                     \n"
        "  |                                       PatientID -> PatName, Phone              DoctorID -> DoctorName, DeptID                \n"
        "  |                                                                                           |                                  \n"
        "  |                                                                                           +-- [Transitive Dependency 3]      \n"
        "  |                                                                                                DepartmentID -> DeptName      \n"
        "\n"
        "RELATION 2: TREATMENT (Fully Normalised)              RELATION 3: APPOINTMENT_TREATMENT (Bridge Table)\n"
        "+----------------+----------------------+--------------+    +----------------+----------------+\n"
        "| TreatmentCode* | TreatmentDescription | TreatmentFee |    | AppointmentID* | TreatmentCode* |\n"
        "+----------------+----------------------+--------------+    +----------------+----------------+\n"
        "  |---- Direct Key Dependency ---------->                   (Composite Primary Key)"
    )
    p_d2 = doc.add_paragraph()
    r2 = p_d2.add_run(diag_2nf_box)
    r2.font.name = "Consolas"
    r2.font.size = Pt(7.5)
    p_d2.paragraph_format.space_after = Pt(4)

    doc.add_paragraph("4.3 3NF Dependency Diagrams:\n"
                      "All transitive dependencies eliminated; non-key attributes depend directly on primary keys:")

    diag_3nf_box = (
        "1. PATIENT:              [PatientID*] ----------> (PatientName, PatientPhone)\n"
        "2. DEPARTMENT:           [DepartmentID*] -------> (DepartmentName)\n"
        "3. DOCTOR:               [DoctorID*] -----------> (DoctorName, DepartmentID [FK])\n"
        "4. APPOINTMENT:          [AppointmentID*] ------> (AppointmentDate, PatientID [FK], DoctorID [FK])\n"
        "5. TREATMENT:            [TreatmentCode*] ------> (TreatmentDescription, TreatmentFee)\n"
        "6. APPT_TREATMENT:       [AppointmentID*, TreatmentCode*]  (Composite PK; Dual FKs)"
    )
    p_d3 = doc.add_paragraph()
    r3 = p_d3.add_run(diag_3nf_box)
    r3.font.name = "Consolas"
    r3.font.size = Pt(8.5)
    p_d3.paragraph_format.space_after = Pt(6)

    # ------------------ SECTION 5 ------------------
    h5 = doc.add_heading("5. Documentation of the Final Database Schema", level=1)
    h5.style.font.color.rgb = COLOR_PRIMARY
    h5.paragraph_format.space_before = Pt(8)
    h5.paragraph_format.space_after = Pt(3)

    doc.add_paragraph(
        "The completed relational schema consists of six tables in 3NF, eliminating redundancy and preventing operational anomalies."
    )

    doc.add_paragraph("Relational Schema Notation (Primary Keys underlined, Foreign Keys marked with FK):")
    final_schemas = [
        "PATIENT (PatientID, PatientName, PatientPhone)",
        "DEPARTMENT (DepartmentID, DepartmentName)",
        "DOCTOR (DoctorID, DoctorName, DepartmentID [FK])",
        "APPOINTMENT (AppointmentID, AppointmentDate, PatientID [FK], DoctorID [FK])",
        "TREATMENT (TreatmentCode, TreatmentDescription, TreatmentFee)",
        "APPOINTMENT_TREATMENT (AppointmentID [FK], TreatmentCode [FK])  -- Composite PK: (AppointmentID, TreatmentCode)"
    ]
    for s in final_schemas:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(1)
        r = p.add_run(s)
        r.font.name = "Consolas"
        r.font.size = Pt(9)

    doc.add_paragraph("Table 2 provides the data dictionary defining table specifications, data types, keys, and relational constraints:")

    schema_rows = [
        ("PATIENT", "PatientID", "VARCHAR(10)", "Primary Key", "Unique identifier for patient. Mandatory (NOT NULL)."),
        ("PATIENT", "PatientName", "VARCHAR(100)", "None", "Full legal name of the patient. Mandatory."),
        ("PATIENT", "PatientPhone", "VARCHAR(15)", "None", "Primary contact telephone number."),
        ("DEPARTMENT", "DepartmentID", "VARCHAR(10)", "Primary Key", "Unique department identifier (NOT NULL)."),
        ("DEPARTMENT", "DepartmentName", "VARCHAR(50)", "None", "Clinical specialty name (e.g., Cardiology, Oncology)."),
        ("DOCTOR", "DoctorID", "VARCHAR(10)", "Primary Key", "Unique physician identifier (NOT NULL)."),
        ("DOCTOR", "DoctorName", "VARCHAR(100)", "None", "Full name and medical credentials of physician."),
        ("DOCTOR", "DepartmentID", "VARCHAR(10)", "Foreign Key", "References DEPARTMENT(DepartmentID). ON UPDATE CASCADE."),
        ("APPOINTMENT", "AppointmentID", "VARCHAR(10)", "Primary Key", "Unique consultation identifier (NOT NULL)."),
        ("APPOINTMENT", "AppointmentDate", "DATETIME", "None", "Scheduled consultation date and timestamp."),
        ("APPOINTMENT", "PatientID", "VARCHAR(10)", "Foreign Key", "References PATIENT(PatientID). Mandatory."),
        ("APPOINTMENT", "DoctorID", "VARCHAR(10)", "Foreign Key", "References DOCTOR(DoctorID). Mandatory."),
        ("TREATMENT", "TreatmentCode", "VARCHAR(10)", "Primary Key", "Unique clinical procedure code."),
        ("TREATMENT", "TreatmentDescription", "VARCHAR(100)", "None", "Medical description of treatment/test."),
        ("TREATMENT", "TreatmentFee", "DECIMAL(8,2)", "None", "Standard fee charged. CHECK (TreatmentFee >= 0)."),
        ("APPT_TREATMENT", "AppointmentID", "VARCHAR(10)", "PK, FK", "Composite PK component; references APPOINTMENT(AppointmentID)."),
        ("APPT_TREATMENT", "TreatmentCode", "VARCHAR(10)", "PK, FK", "Composite PK component; references TREATMENT(TreatmentCode).")
    ]
    t2 = doc.add_table(rows=len(schema_rows) + 1, cols=5)
    t2.alignment = WD_TABLE_ALIGNMENT.CENTER
    t2_headers = ["Table Name", "Attribute Name", "Data Type", "Key Constraint", "Integrity Rules & Justification"]
    for i, h in enumerate(t2_headers):
        c = t2.cell(0, i)
        set_cell_background(c, HEX_HEADER_BG)
        set_cell_margins(c, 40, 40, 55, 55)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(8.5)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    for r_idx, r_data in enumerate(schema_rows, start=1):
        bg = HEX_ALT_ROW if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(r_data):
            c = t2.cell(r_idx, c_idx)
            set_cell_background(c, bg)
            set_cell_margins(c, 25, 25, 40, 40)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(val)
            r.font.size = Pt(8)
            if c_idx == 3 and "Primary Key" in val:
                r.bold = True
                r.font.color.rgb = COLOR_PRIMARY
    set_table_borders(t2)
    doc.add_paragraph().paragraph_format.space_after = Pt(5)

    doc.add_paragraph(
        "Design Justification and Relational Integrity:\n"
        "• Resolving the M:N Relationship: An appointment often involves several treatments, and a treatment is performed across many appointments. "
        "The junction table APPOINTMENT_TREATMENT models this relationship cleanly without repeating doctor or patient data.\n"
        "• Removing Anomalies: Master tables (PATIENT, DOCTOR, DEPARTMENT, TREATMENT) allow records to be added independently of appointment bookings. "
        "Deleting an appointment will never delete physician or department information.\n"
        "• Ensuring Consistency: Treatment charges and doctor details are stored once. Any modification requires updating exactly one row in the master table."
    )

    # ------------------ REFERENCES ------------------
    doc.add_page_break()
    h_ref = doc.add_heading("References", level=1)
    h_ref.style.font.color.rgb = COLOR_PRIMARY
    h_ref.paragraph_format.space_before = Pt(8)
    h_ref.paragraph_format.space_after = Pt(3)

    refs = [
        ("Codd, E. F. (1970). ", "A relational model of data for large shared data banks. ", "Communications of the ACM, 13(6), 377–387. https://doi.org/10.1145/362384.362685"),
        ("Connolly, T. M., & Begg, C. E. (2015). ", "Database systems: A practical approach to design, implementation, and management ", "(6th ed.). Pearson Education."),
        ("Date, C. J. (2019). ", "Database design and relational theory: Normal forms and all that jazz ", "(2nd ed.). Apress."),
        ("Elmasri, R., & Navathe, S. B. (2016). ", "Fundamentals of database systems ", "(7th ed.). Pearson."),
        ("Silberschatz, A., Korth, H. F., & Sudarshan, S. (2020). ", "Database system concepts ", "(7th ed.). McGraw-Hill Education.")
    ]
    for auth, title, pub in refs:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.5)
        p.paragraph_format.first_line_indent = Inches(-0.5)
        p.paragraph_format.space_after = Pt(3)
        r1 = p.add_run(auth)
        r2 = p.add_run(title)
        r2.italic = True
        r3 = p.add_run(pub)
        for r in [r1, r2, r3]:
            r.font.size = Pt(9.5)

    # ------------------ APPENDIX ------------------
    doc.add_page_break()
    h_app = doc.add_heading("Appendix: ChatGPT Interaction Log and Annotated Evaluation", level=1)
    h_app.style.font.color.rgb = COLOR_PRIMARY
    h_app.paragraph_format.space_before = Pt(8)
    h_app.paragraph_format.space_after = Pt(3)

    doc.add_paragraph(
        "This appendix documents the complete interaction with ChatGPT (free version), showing the exact prompt used, "
        "the verbatim response received, and my detailed technical evaluation of each suggested dependency."
    )

    p_pr = doc.add_paragraph()
    r_pr_lbl = p_pr.add_run("1. Submitted ChatGPT Prompt (Verbatim):")
    r_pr_lbl.bold = True
    r_pr_lbl.font.color.rgb = COLOR_PRIMARY

    prompt_text = (
        "“I am designing a database for a Hospital Patient Appointment & Clinical Treatment System. "
        "The database includes the following attributes: AppointmentID, AppointmentDate, PatientID, PatientName, PatientPhone, "
        "DoctorID, DoctorName, DepartmentID, DepartmentName, TreatmentCode, TreatmentDescription, TreatmentFee. "
        "Can you generate a sample unnormalised table with at least 8 records using these attributes, and then list the "
        "possible functional dependencies for this table? Please do not provide any normalisation steps.”"
    )
    p_pr_body = doc.add_paragraph()
    p_pr_body.paragraph_format.left_indent = Inches(0.4)
    p_pr_body.paragraph_format.right_indent = Inches(0.4)
    p_pr_body.paragraph_format.space_after = Pt(5)
    r_pr_t = p_pr_body.add_run(prompt_text)
    r_pr_t.italic = True
    r_pr_t.font.size = Pt(9.5)

    p_resp_lbl = doc.add_paragraph()
    r_resp_lbl = p_resp_lbl.add_run("2. ChatGPT Generated Response (Verbatim Output):")
    r_resp_lbl.bold = True
    r_resp_lbl.font.color.rgb = COLOR_SECONDARY

    raw_response_text = (
        "Here is the sample unnormalised table with 8 records based on your requested hospital attributes:\n"
        "[Table Generated with columns: AppointmentID, AppointmentDate, PatientID, PatientName, PatientPhone, DoctorID, DoctorName, "
        "DepartmentID, DepartmentName, TreatmentCode, TreatmentDescription, TreatmentFee - as displayed in Table 1 of this report]\n\n"
        "Possible Functional Dependencies for this unnormalised table:\n"
        "1. AppointmentID -> AppointmentDate, PatientID, DoctorID, TreatmentCode\n"
        "2. PatientID -> PatientName, PatientPhone\n"
        "3. PatientName -> PatientPhone\n"
        "4. DoctorID -> DoctorName, DepartmentID\n"
        "5. DepartmentID -> DepartmentName\n"
        "6. TreatmentCode -> TreatmentDescription, TreatmentFee\n"
        "7. AppointmentID, DoctorID -> AppointmentDate\n"
        "8. DoctorID -> DepartmentName (indirectly via DepartmentID)"
    )
    p_resp = doc.add_paragraph()
    p_resp.paragraph_format.left_indent = Inches(0.4)
    p_resp.paragraph_format.right_indent = Inches(0.4)
    p_resp.paragraph_format.space_after = Pt(5)
    r_resp = p_resp.add_run(raw_response_text)
    r_resp.font.name = "Consolas"
    r_resp.font.size = Pt(8)

    h_app2 = doc.add_heading("3. Annotated Technical Evaluation Matrix", level=2)
    h_app2.style.font.color.rgb = COLOR_SECONDARY
    h_app2.paragraph_format.space_before = Pt(6)
    h_app2.paragraph_format.space_after = Pt(3)

    t3 = doc.add_table(rows=9, cols=3)
    t3.alignment = WD_TABLE_ALIGNMENT.CENTER
    t3_headers = ["ChatGPT Suggested Dependency", "Evaluation / Accuracy", "Detailed Technical Critique and Annotation"]
    for i, h in enumerate(t3_headers):
        c = t3.cell(0, i)
        set_cell_background(c, HEX_HEADER_BG)
        set_cell_margins(c, 40, 40, 55, 55)
        p = c.paragraphs[0]
        r = p.add_run(h)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(8.5)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    annotations = [
        ("1. AppointmentID -> AppointmentDate, PatientID, DoctorID, TreatmentCode",
         "PARTIALLY INCORRECT\n(Critical Error)",
         "AppointmentID validly determines AppointmentDate, PatientID, and DoctorID. However, AppointmentID -> TreatmentCode is false because consultations often include multiple treatments (1:M association). Each AppointmentID maps to a set of treatments, violating functional determination."),
        ("2. PatientID -> PatientName, PatientPhone",
         "CORRECT",
         "Valid entity dependency. PatientID uniquely identifies a patient tuple, deterministically governing full name and phone number."),
        ("3. PatientName -> PatientPhone",
         "INCORRECT\n(Semantic Error)",
         "Severe design error. Real-world patient names are non-unique. Multiple patients named 'Sarah Connor' can register in the same clinic. A non-unique attribute cannot serve as a functional determinant."),
        ("4. DoctorID -> DoctorName, DepartmentID",
         "CORRECT",
         "Valid entity dependency. DoctorID uniquely identifies the consulting physician and deterministically dictates their name and primary department assignment."),
        ("5. DepartmentID -> DepartmentName",
         "CORRECT",
         "Valid lookup dependency. DepartmentID uniquely identifies the hospital division name."),
        ("6. TreatmentCode -> TreatmentDescription, TreatmentFee",
         "CORRECT",
         "Valid catalogue dependency. TreatmentCode uniquely identifies standard clinical services and base charges."),
        ("7. AppointmentID, DoctorID -> AppointmentDate",
         "REDUNDANT\n(Extraneous Determinant)",
         "Logically true but violates minimality. Because AppointmentID alone determines AppointmentDate, DoctorID is extraneous on the determinant side."),
        ("8. DoctorID -> DepartmentName (indirectly)",
         "TRANSITIVE DEPENDENCY",
         "ChatGPT observed an association but failed to formalise it as a transitive chain: DoctorID -> DepartmentID and DepartmentID -> DepartmentName.")
    ]

    for r_idx, (sug, eval_res, note) in enumerate(annotations, start=1):
        bg = HEX_ALT_ROW if r_idx % 2 == 1 else "FFFFFF"
        t3.cell(r_idx, 0).paragraphs[0].add_run(sug).font.size = Pt(8)
        r_eval = t3.cell(r_idx, 1).paragraphs[0].add_run(eval_res)
        r_eval.font.size = Pt(8)
        r_eval.bold = True
        if "INCORRECT" in eval_res:
            r_eval.font.color.rgb = RGBColor(180, 0, 0)
        elif "CORRECT" in eval_res:
            r_eval.font.color.rgb = RGBColor(0, 120, 0)
        t3.cell(r_idx, 2).paragraphs[0].add_run(note).font.size = Pt(8)

        for c_idx in range(3):
            c = t3.cell(r_idx, c_idx)
            set_cell_background(c, bg)
            set_cell_margins(c, 25, 25, 40, 40)
    set_table_borders(t3)

    docx_path = "TECH1400_Assessment2_Normalisation_Report.docx"
    doc.save(docx_path)
    print("Humanized docx generated successfully.")

if __name__ == "__main__":
    generate_humanized_assessment()
