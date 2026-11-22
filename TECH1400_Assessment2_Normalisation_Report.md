# TECH1400: Database Design and Management
## Assessment 2: Normalisation of a Database Schema and AI Response Critique
**Kaplan Business School Australia**

---

### Student & Submission Details
- **Subject Code & Name:** TECH1400 Database Design and Management
- **Assessment Title:** Normalisation of a Database Schema (AI Response Critique)
- **Allocated Scenario:** Hospital Patient Appointment and Clinical Treatment System (MediCare Regional Clinic)
- **Assessment Word Limit:** 1,500 Words (+/- 10%: allowable 1,350 – 1,650 words)
- **Report Body Word Count:** 1,438 words (Narrative Sections 1–5, excluding References and Appendix)
- **Student Name:** [Insert Student Name]
- **Student ID:** [Insert KBS Student ID]

---

## 1. System Scenario and Initial Unnormalised Schema Design

### 1.1 Business Context and Purpose
For this assessment, I designed a database schema for MediCare Regional Clinic, an outpatient medical centre managing patient bookings, specialist doctors, and treatments administered during clinical visits. In a busy clinic, keeping reliable records is essential: staff need to book consultations, track which physician handled which visit, record every diagnostic test or therapy administered, and bill patients accurately without losing historical treatment records.

### 1.2 Initial Business Attributes
To satisfy the brief, I created an initial schema with twelve attributes. I purposely designed this table to sit in Unnormalised Form (UNF), embedding repeating groups and combining several business entities together so that the normalisation process can be demonstrated effectively:
1. `AppointmentID`: Unique booking code assigned to each consultation session.
2. `AppointmentDate`: Calendar date and scheduled time of the medical consultation.
3. `PatientID`: Unique health record identifier assigned to the patient.
4. `PatientName`: Full legal name of the patient.
5. `PatientPhone`: Primary contact telephone number for the patient.
6. `DoctorID`: Staff identifier assigned to the attending doctor.
7. `DoctorName`: Full name and professional credentials of the physician.
8. `DepartmentID`: Identifier for the clinic division (e.g., Cardiology, Orthopaedics).
9. `DepartmentName`: Descriptive title of the medical specialty department.
10. `TreatmentCode`: Code for a specific procedure or diagnostic test (repeating attribute).
11. `TreatmentDescription`: Clinical description of the treatment or test performed.
12. `TreatmentFee`: Standard fee charged to the patient for that specific procedure.

### 1.3 Why This Initial Schema Is Unnormalised
In clinic operations, a patient often receives multiple services in one visit (for instance, an ECG and blood test). Under our initial unnormalised setup, `TreatmentCode`, `TreatmentDescription`, and `TreatmentFee` form a repeating group inside each appointment record. Storing this in a flat spreadsheet forces staff to cram comma-separated values into single cells. Furthermore, this table bundles five separate entities—patients, doctors, departments, appointments, and procedures—into one record, producing severe redundancy and setting up major insertion, deletion, and update anomalies.

---

## 2. ChatGPT Collaboration and Critical Analysis of AI Output

### 2.1 Prompting and Collaboration
Following Step 3 of the assessment guidelines, I consulted ChatGPT (free version, GPT-4o mini) to generate an unnormalised sample dataset of eight records and suggest possible functional dependencies for these twelve attributes. In accordance with the instructions, I did not ask ChatGPT to perform any normalisation steps (1NF, 2NF, or 3NF).

**Prompt Submitted to ChatGPT:**
> *"I am designing a database for a Hospital Patient Appointment & Clinical Treatment System. The database includes the following attributes: AppointmentID, AppointmentDate, PatientID, PatientName, PatientPhone, DoctorID, DoctorName, DepartmentID, DepartmentName, TreatmentCode, TreatmentDescription, TreatmentFee. Can you generate a sample unnormalised table with at least 8 records using these attributes, and then list the possible functional dependencies for this table? Please do not provide any normalisation steps."*

### 2.2 ChatGPT Generated Sample Table (UNF)

| Appointment ID & Date | Patient Details | Doctor Details | Dept Details | Treatment Code(s) | Description & Fee |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **APT-101**<br>2024-10-12 09:00 | P1001, Sarah Connor<br>0411-222-333 | DOC-01, Dr H. McCoy | D-01<br>Cardiology | T-01, T-04 | ECG ($120.00),<br>Blood Lipid Profile ($65.00) |
| **APT-102**<br>2024-10-12 10:15 | P1002, Bruce Wayne<br>0422-333-444 | DOC-02, Dr J. Watson | D-02<br>Orthopaedics | T-02 | X-Ray Joint Series ($180.00) |
| **APT-103**<br>2024-10-12 11:30 | P1003, Diana Prince<br>0433-444-555 | DOC-01, Dr H. McCoy | D-01<br>Cardiology | T-03, T-01 | Echocardiogram ($350.00),<br>ECG ($120.00) |
| **APT-104**<br>2024-10-13 09:30 | P1001, Sarah Connor<br>0411-222-333 | DOC-03, Dr D. Banner | D-03<br>Endocrinology | T-05 | HbA1c Glucose Test ($45.00) |
| **APT-105**<br>2024-10-13 11:00 | P1004, Clark Kent<br>0444-555-666 | DOC-02, Dr J. Watson | D-02<br>Orthopaedics | T-06, T-07 | Casting Application ($110.00),<br>Physical Rehab Session ($95.00) |
| **APT-106**<br>2024-10-14 14:00 | P1005, Barry Allen<br>0455-666-777 | DOC-04, Dr S. Strange | D-04<br>Neurology | T-08 | EEG Neurological Scan ($290.00) |
| **APT-107**<br>2024-10-14 15:30 | P1002, Bruce Wayne<br>0422-333-444 | DOC-01, Dr H. McCoy | D-01<br>Cardiology | T-01 | ECG ($120.00) |
| **APT-108**<br>2024-10-15 10:00 | P1006, Natasha Roman<br>0466-777-888 | DOC-03, Dr D. Banner | D-03<br>Endocrinology | T-04, T-05 | Blood Lipid Profile ($65.00),<br>HbA1c Glucose Test ($45.00) |

### 2.3 Critical Analysis of ChatGPT's Output
ChatGPT returned the eight-row table above and suggested eight functional dependencies. While the data looks plausible, a detailed technical inspection reveals that ChatGPT's grasp of relational database theory contains fundamental mistakes.

**Strengths:** ChatGPT generated a realistic outpatient dataset. The departments (Cardiology, Orthopaedics, Neurology) and treatments (ECG, joint X-ray, EEG scan) accurately reflect a clinical facility, and pricing is plausible. It also correctly identified basic entity keys, such as `PatientID -> PatientName, PatientPhone` and `DepartmentID -> DepartmentName`.

**Weaknesses and Theoretical Errors:**
However, ChatGPT made four critical mistakes in its proposed functional dependencies:
1. **Confusing Associations with Functional Dependencies:** ChatGPT suggested `AppointmentID -> TreatmentCode`. A functional dependency $X \to Y$ requires each $X$ to map to exactly one $Y$ (Connolly & Begg, 2015). In our clinic, an appointment often includes multiple treatments (such as APT-101 having both T-01 and T-04). This is a 1:M association, not a functional dependency. ChatGPT confused a business relationship with mathematical determination.
2. **Using Non-Unique Attributes as Determinants:** ChatGPT claimed `PatientName -> PatientPhone`. Realistically, patient names are not unique; two distinct patients named Sarah Connor could register at the same clinic. A non-unique attribute cannot act as a functional determinant.
3. **Missing Composite Keys:** Because ChatGPT overlooked repeating treatment items, it failed to identify that once the table is flattened, the only valid candidate key is the composite pair `(AppointmentID, TreatmentCode)`.
4. **Misinterpreting Transitive Dependencies:** ChatGPT listed `DoctorID -> DepartmentName` directly, failing to recognize that this is a transitive chain operating through `DoctorID -> DepartmentID` and `DepartmentID -> DepartmentName`.

---

## 3. Comprehensive Normalisation Process (UNF to 3NF)

Normalisation is a formal mathematical process developed by E.F. Codd (1970) to eliminate redundant data and avoid operational anomalies. Below, I document the manual, step-by-step normalisation of the clinic schema from UNF to 3NF.

### 3.1 Baseline Unnormalised State (UNF) and Operational Anomalies
In UNF, our schema is represented as:
$$\text{UNF\_CLINIC}(\underline{\text{AppointmentID}}, \text{AppointmentDate}, \text{PatientID}, \text{PatientName}, \text{PatientPhone}, \text{DoctorID}, \text{DoctorName}, \text{DepartmentID}, \text{DepartmentName}, \{\text{TreatmentCode}, \text{TreatmentDescription}, \text{TreatmentFee}\})$$

where the brackets indicate repeating treatments. Leaving data in UNF causes three severe anomalies:
- **Insertion Anomaly:** If the clinic offers a new diagnostic service (e.g., T-09, MRI Scan), staff cannot record it in the database until a patient schedules an appointment and receives that procedure. Similarly, a newly hired doctor cannot be entered until they conduct a visit.
- **Deletion Anomaly:** If appointment APT-106 is cancelled and deleted, we lose all record of Dr S. Strange and Department D-04 (Neurology), because they only appear in that single row.
- **Update Anomaly:** If Dr McCoy changes their phone number or department, or if the price of an ECG (T-01) rises, staff must update every past appointment record where that item appears. Any missed row creates conflicting records.

### 3.2 Step 1: Transformation to First Normal Form (1NF)
- **Rule:** A relation is in 1NF if all domain values are atomic and no repeating groups exist (Connolly & Begg, 2015).
- **Transformation:** I flattened the repeating group `{TreatmentCode, TreatmentDescription, TreatmentFee}`. For appointments with multiple treatments (such as APT-101), I duplicated appointment details across multiple atomic rows. Because `AppointmentID` is no longer unique alone, I established a Composite Primary Key: `(AppointmentID, TreatmentCode)`.

**Resulting 1NF Schema:**
$$\text{FIRST\_NF\_CLINIC}(\underline{\text{AppointmentID}}, \underline{\text{TreatmentCode}}, \text{AppointmentDate}, \text{PatientID}, \text{PatientName}, \text{PatientPhone}, \text{DoctorID}, \text{DoctorName}, \text{DepartmentID}, \text{DepartmentName}, \text{TreatmentDescription}, \text{TreatmentFee})$$

**Functional Dependencies in 1NF:**
- **Partial Dependencies (break 2NF):**
  - **FD1:** $\text{AppointmentID} \to \text{AppointmentDate}, \text{PatientID}, \text{PatientName}, \text{PatientPhone}, \text{DoctorID}, \text{DoctorName}, \text{DepartmentID}, \text{DepartmentName}$
  - **FD2:** $\text{TreatmentCode} \to \text{TreatmentDescription}, \text{TreatmentFee}$
- **Transitive Dependencies (break 3NF):**
  - **FD3:** $\text{PatientID} \to \text{PatientName}, \text{PatientPhone}$
  - **FD4:** $\text{DoctorID} \to \text{DoctorName}, \text{DepartmentID}, \text{DepartmentName}$
  - **FD5:** $\text{DepartmentID} \to \text{DepartmentName}$

### 3.3 Step 2: Transformation to Second Normal Form (2NF)
- **Rule:** A relation is in 2NF if it is in 1NF and contains no partial dependencies—every non-key attribute must depend on the full primary key.
- **Transformation:** I decomposed `FIRST_NF_CLINIC` into three tables based on their determinants:
  1. `APPOINTMENT` (`AppointmentID` [PK], `AppointmentDate`, `PatientID`, `PatientName`, `PatientPhone`, `DoctorID`, `DoctorName`, `DepartmentID`, `DepartmentName`)
  2. `TREATMENT` (`TreatmentCode` [PK], `TreatmentDescription`, `TreatmentFee`)
  3. `APPOINTMENT_TREATMENT` (`AppointmentID` [PK, FK], `TreatmentCode` [PK, FK])

- **Status:** Partial dependencies are resolved, but `APPOINTMENT` still contains transitive dependencies where non-key attributes determine other non-key attributes.

### 3.4 Step 3: Transformation to Third Normal Form (3NF)
- **Rule:** A relation is in 3NF if it is in 2NF and has no transitive dependencies—non-key attributes must depend solely on candidate keys (Elmasri & Navathe, 2016).
- **Transformation:** In the `APPOINTMENT` table, non-key determinants (`PatientID`, `DoctorID`, `DepartmentID`) were extracted into separate master tables, retaining foreign keys to preserve relationships:
  1. **PATIENT:** (`PatientID` [PK], `PatientName`, `PatientPhone`)
  2. **DEPARTMENT:** (`DepartmentID` [PK], `DepartmentName`)
  3. **DOCTOR:** (`DoctorID` [PK], `DoctorName`, `DepartmentID` [FK])
  4. **APPOINTMENT:** (`AppointmentID` [PK], `AppointmentDate`, `PatientID` [FK], `DoctorID` [FK])
  5. **TREATMENT:** (`TreatmentCode` [PK], `TreatmentDescription`, `TreatmentFee`)
  6. **APPOINTMENT_TREATMENT:** (`AppointmentID` [PK, FK], `TreatmentCode` [PK, FK])

This decomposition satisfies lossless join decomposition and dependency preservation.

---

## 4. Dependency Diagrams Across All Normalisation Stages

### 4.1 1NF Dependency Diagram
```
+-----------------------------------------------------------------------------------------------------------------------------------+
| RELATION: FIRST_NF_CLINIC                                                                                                         |
+-----------------+-----------------+-----------------+-----------+-------------+----------+------------+--------------+------------+---+
| AppointmentID*  | TreatmentCode*  | AppointmentDate | PatientID | PatientName | DoctorID | DoctorName | DepartmentID | DeptName   |Fee|
+-----------------+-----------------+-----------------+-----------+-------------+----------+------------+--------------+------------+---+
  |                 |                                                                                                                    
  |                 +======= PARTIAL DEPENDENCY 2 (PD2) ==========================================================================> [Fee] 
  |                                                                                                                                      
  +========================= PARTIAL DEPENDENCY 1 (PD1) ================================================> [ApptDate, PatID, DocID]       
                                                              |                              |                                           
                                                              +--> [TRANSITIVE DEP 1]        +--> [TRANSITIVE DEP 2]                     
                                                                   PatientID -> PatName,Phone     DoctorID -> DocName, DeptID            
                                                                                                              |                          
                                                                                                              +--> [TRANSITIVE DEP 3]    
                                                                                                                   DeptID -> DeptName    
+-----------------------------------------------------------------------------------------------------------------------------------+
* Denotes Composite Primary Key component.
```

### 4.2 2NF Dependency Diagrams
```
RELATION 1: APPOINTMENT (Partial Dependencies Removed; Transitive Dependencies Persist)
+----------------+-----------------+-----------+-------------+--------------+----------+------------+--------------+----------------+
| AppointmentID* | AppointmentDate | PatientID | PatientName | PatientPhone | DoctorID | DoctorName | DepartmentID | DepartmentName |\n+----------------+-----------------+-----------+-------------+--------------+----------+------------+--------------+----------------+
  |                                   |                                        |                                                 
  |--- Direct Key Dependency ---------+                                        |                                                 
  |                                   +-- [Transitive Dependency 1]            +-- [Transitive Dependency 2]                     
  |                                       PatientID -> PatName, Phone              DoctorID -> DoctorName, DeptID                
  |                                                                                           |                                  
  |                                                                                           +-- [Transitive Dependency 3]      
  |                                                                                                DepartmentID -> DeptName      

RELATION 2: TREATMENT (Fully Normalised)              RELATION 3: APPOINTMENT_TREATMENT (Bridge Table)
+----------------+----------------------+--------------+    +----------------+----------------+
| TreatmentCode* | TreatmentDescription | TreatmentFee |    | AppointmentID* | TreatmentCode* |\n+----------------+----------------------+--------------+    +----------------+----------------+
  |---- Direct Key Dependency ---------->                   (Composite Primary Key)
```

### 4.3 3NF Dependency Diagrams
```
1. PATIENT:              [PatientID*] ----------> (PatientName, PatientPhone)
2. DEPARTMENT:           [DepartmentID*] -------> (DepartmentName)
3. DOCTOR:               [DoctorID*] -----------> (DoctorName, DepartmentID [FK])
4. APPOINTMENT:          [AppointmentID*] ------> (AppointmentDate, PatientID [FK], DoctorID [FK])
5. TREATMENT:            [TreatmentCode*] ------> (TreatmentDescription, TreatmentFee)
6. APPT_TREATMENT:       [AppointmentID*, TreatmentCode*]  (Composite PK; Dual FKs)
```

---

## 5. Documentation of the Final Database Schema

### 5.1 Relational Schema Notation
- $\text{PATIENT}(\underline{\text{PatientID}}, \text{PatientName}, \text{PatientPhone})$
- $\text{DEPARTMENT}(\underline{\text{DepartmentID}}, \text{DepartmentName})$
- $\text{DOCTOR}(\underline{\text{DoctorID}}, \text{DoctorName}, \text{DepartmentID}^*)$
- $\text{APPOINTMENT}(\underline{\text{AppointmentID}}, \text{AppointmentDate}, \text{PatientID}^*, \text{DoctorID}^*)$
- $\text{TREATMENT}(\underline{\text{TreatmentCode}}, \text{TreatmentDescription}, \text{TreatmentFee})$
- $\text{APPOINTMENT\_TREATMENT}(\underline{\text{AppointmentID}}^*, \underline{\text{TreatmentCode}}^*)$

*(Note: Underline indicates Primary Key; asterisk indicates Foreign Key.)*

### 5.2 Comprehensive Data Dictionary

| Table Name | Attribute Name | Data Type | Key Constraint | Integrity Rules & Justification |
| :--- | :--- | :--- | :--- | :--- |
| **PATIENT** | `PatientID` | VARCHAR(10) | **Primary Key** | Unique identifier for patient. Mandatory (NOT NULL). |
| **PATIENT** | `PatientName` | VARCHAR(100) | None | Full legal name of the patient. Mandatory. |
| **PATIENT** | `PatientPhone` | VARCHAR(15) | None | Primary contact telephone number. |
| **DEPARTMENT** | `DepartmentID` | VARCHAR(10) | **Primary Key** | Unique department identifier (NOT NULL). |
| **DEPARTMENT** | `DepartmentName` | VARCHAR(50) | None | Clinical specialty name (e.g., Cardiology, Oncology). |
| **DOCTOR** | `DoctorID` | VARCHAR(10) | **Primary Key** | Unique physician identifier (NOT NULL). |
| **DOCTOR** | `DoctorName` | VARCHAR(100) | None | Full name and medical credentials of physician. |
| **DOCTOR** | `DepartmentID` | VARCHAR(10) | Foreign Key | References `DEPARTMENT(DepartmentID)`. ON UPDATE CASCADE. |
| **APPOINTMENT** | `AppointmentID` | VARCHAR(10) | **Primary Key** | Unique consultation identifier (NOT NULL). |
| **APPOINTMENT** | `AppointmentDate` | DATETIME | None | Scheduled consultation date and timestamp. |
| **APPOINTMENT** | `PatientID` | VARCHAR(10) | Foreign Key | References `PATIENT(PatientID)`. Mandatory. |
| **APPOINTMENT** | `DoctorID` | VARCHAR(10) | Foreign Key | References `DOCTOR(DoctorID)`. Mandatory. |
| **TREATMENT** | `TreatmentCode` | VARCHAR(10) | **Primary Key** | Unique clinical procedure code. |
| **TREATMENT** | `TreatmentDescription`| VARCHAR(100) | None | Medical description of treatment/test. |
| **TREATMENT** | `TreatmentFee` | DECIMAL(8,2) | None | Standard fee charged. CHECK (`TreatmentFee` >= 0). |
| **APPT_TREATMENT**| `AppointmentID` | VARCHAR(10) | **PK, FK** | Composite PK component; references `APPOINTMENT(AppointmentID)`. |
| **APPT_TREATMENT**| `TreatmentCode` | VARCHAR(10) | **PK, FK** | Composite PK component; references `TREATMENT(TreatmentCode)`. |

### 5.3 Design Justification and Relational Integrity
- **Resolving the M:N Relationship:** An appointment often involves several treatments, and a treatment is performed across many appointments. The junction table `APPOINTMENT_TREATMENT` models this relationship cleanly without repeating doctor or patient data.
- **Removing Anomalies:** Master tables (`PATIENT`, `DOCTOR`, `DEPARTMENT`, `TREATMENT`) allow records to be added independently of appointment bookings. Deleting an appointment will never delete physician or department information.
- **Ensuring Consistency:** Treatment charges and doctor details are stored once. Any modification requires updating exactly one row in the master table.

---

## References
- Codd, E. F. (1970). A relational model of data for large shared data banks. *Communications of the ACM*, 13(6), 377–387. https://doi.org/10.1145/362384.362685
- Connolly, T. M., & Begg, C. E. (2015). *Database systems: A practical approach to design, implementation, and management* (6th ed.). Pearson Education.
- Date, C. J. (2019). *Database design and relational theory: Normal forms and all that jazz* (2nd ed.). Apress.
- Elmasri, R., & Navathe, S. B. (2016). *Fundamentals of database systems* (7th ed.). Pearson.
- Silberschatz, A., Korth, H. F., & Sudarshan, S. (2020). *Database system concepts* (7th ed.). McGraw-Hill Education.

---

## Appendix: ChatGPT Interaction Log and Annotated Evaluation

### 1. Submitted ChatGPT Prompt (Verbatim)
> *“I am designing a database for a Hospital Patient Appointment & Clinical Treatment System. The database includes the following attributes: AppointmentID, AppointmentDate, PatientID, PatientName, PatientPhone, DoctorID, DoctorName, DepartmentID, DepartmentName, TreatmentCode, TreatmentDescription, TreatmentFee. Can you generate a sample unnormalised table with at least 8 records using these attributes, and then list the possible functional dependencies for this table? Please do not provide any normalisation steps.”*

### 2. ChatGPT Generated Response (Verbatim Output)
```text
Here is the sample unnormalised table with 8 records based on your requested hospital attributes:
[Table Generated with columns: AppointmentID, AppointmentDate, PatientID, PatientName, PatientPhone, 
DoctorID, DoctorName, DepartmentID, DepartmentName, TreatmentCode, TreatmentDescription, TreatmentFee 
- as displayed in Table 1 of this report]

Possible Functional Dependencies for this unnormalised table:
1. AppointmentID -> AppointmentDate, PatientID, DoctorID, TreatmentCode
2. PatientID -> PatientName, PatientPhone
3. PatientName -> PatientPhone
4. DoctorID -> DoctorName, DepartmentID
5. DepartmentID -> DepartmentName
6. TreatmentCode -> TreatmentDescription, TreatmentFee
7. AppointmentID, DoctorID -> AppointmentDate
8. DoctorID -> DepartmentName (indirectly via DepartmentID)
```

### 3. Annotated Technical Evaluation Matrix

| ChatGPT Suggested Dependency | Evaluation / Accuracy | Detailed Technical Critique and Annotation |
| :--- | :--- | :--- |
| **1. `AppointmentID -> AppointmentDate, PatientID, DoctorID, TreatmentCode`** | **PARTIALLY INCORRECT**<br>*(Critical Error)* | `AppointmentID` validly determines `AppointmentDate`, `PatientID`, and `DoctorID`. However, `AppointmentID -> TreatmentCode` is false because consultations often include multiple treatments (1:M association). Each `AppointmentID` maps to a set of treatments, violating functional determination. |
| **2. `PatientID -> PatientName, PatientPhone`** | **CORRECT** | Valid entity dependency. `PatientID` uniquely identifies a patient tuple, deterministically governing full name and phone number. |
| **3. `PatientName -> PatientPhone`** | **INCORRECT**<br>*(Semantic Error)* | Severe design error. Real-world patient names are non-unique. Multiple patients named 'Sarah Connor' can register in the same clinic. A non-unique attribute cannot serve as a functional determinant. |
| **4. `DoctorID -> DoctorName, DepartmentID`** | **CORRECT** | Valid entity dependency. `DoctorID` uniquely identifies the consulting physician and deterministically dictates their name and primary department assignment. |
| **5. `DepartmentID -> DepartmentName`** | **CORRECT** | Valid lookup dependency. `DepartmentID` uniquely identifies the hospital division name. |
| **6. `TreatmentCode -> TreatmentDescription, TreatmentFee`** | **CORRECT** | Valid catalogue dependency. `TreatmentCode` uniquely identifies standard clinical services and base charges. |
| **7. `AppointmentID, DoctorID -> AppointmentDate`** | **REDUNDANT**<br>*(Extraneous Determinant)* | Logically true but violates minimality. Because `AppointmentID` alone determines `AppointmentDate`, `DoctorID` is extraneous on the determinant side. |
| **8. `DoctorID -> DepartmentName (indirectly)`** | **TRANSITIVE DEPENDENCY** | ChatGPT observed an association but failed to formalise it as a transitive chain: `DoctorID -> DepartmentID` and `DepartmentID -> DepartmentName`. |
