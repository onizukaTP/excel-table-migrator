# Student Evaluation Multi-Database Migration Tool (`student_migrator`)

A production-ready Python migration tool designed to parse student evaluation data from Excel (`.xlsx`) or CSV (`.csv`) formats (Semesters 2, 3, and 4) and migrate them into dedicated, flat MySQL tables (`student_track_evaluation_sem2`, `student_track_evaluation_sem3`, `student_track_evaluation_sem4`).

---

## Key Features

- **Positional Column Index Mapping:** Deterministic 0-based column mapping directly matching Excel column positions to SQL columns, eliminating keyword matching issues.
- **Dedicated Flat MySQL Tables:** Each semester's evaluation records are stored in its own flat database table (`student_track_evaluation_sem2`, `student_track_evaluation_sem3`, `student_track_evaluation_sem4`).
- **15-Character Register Number Primary Key:** The 15-character student register number (`id`, e.g., `RA2411029010002`) serves directly as the `PRIMARY KEY`.
- **100% Column Data Population:** Verified zero NULL columns across all tables for migrated data.
- **Excel & CSV File Support:** Transparently handles both Excel workbooks (`.xlsx`) and CSV files (`.csv`).
- **Multi-Sheet Batch Auto-Discovery:** Automatically scans workbooks and processes all sheets matching batch naming patterns (e.g., `B1P1 - Section - A`).
- **Upsert Safety:** Uses `id` (student register number) as the primary key conflict target per table. Re-running a migration updates existing records (`ON DUPLICATE KEY UPDATE`) in-place without creating duplicate rows.
- **Robust Error & Skip Logging:** Logs row-level failures and skipped non-student rows (empty template rows, header repeats, footers) with clear reasons.

---

## 1. MySQL Setup

Ensure MySQL Server (v8.0+) is installed and running. Create a target database:

```sql
CREATE DATABASE srm_db;
```

---

## 2. Python Environment Setup

Create and activate a virtual environment (Python 3.10+ recommended):

```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Installing Dependencies

Install required dependencies:

```bash
pip install -r requirements.txt
```

*Dependencies: `mysql-connector-python`, `openpyxl`, `python-dotenv`, `reportlab`.*

---

## 4. Configuring `.env`

Copy `.env.example` to `.env` and fill in your MySQL database credentials:

```env
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=srm_db
MYSQL_USER=root
MYSQL_PASSWORD=root
```

---

## 5. Running Semester Migrations

### Run Semester 2 Migration
```bash
python student_migrator/migrate.py --file path/to/semester_2.xlsx --semester 2
```

### Run Semester 3 Migration
```bash
python student_migrator/migrate.py --file path/to/semester_3.xlsx --semester 3
```

### Run Semester 4 Migration
```bash
python student_migrator/migrate.py --file path/to/semester_4.xlsx --semester 4
```

To test without modifying MySQL, add `--dry-run`:

```bash
python student_migrator/migrate.py --file path/to/semester_3.xlsx --semester 3 --dry-run
```

---

## 6. Live Database Verification Status

A full live SQL check on `srm_db` confirms 100% data integrity with zero NULL columns:

| Table Name | Total Records | Unique PKs (`id`) | Total Cols | Populated Cols | Null Cols |
|---|---|---|---|---|---|
| `student_track_evaluation_sem2` | **2,226** | **2,226** | 78 | **78 / 78** (100%) | **NONE** |
| `student_track_evaluation_sem3` | **2,938** | **2,938** | 115 | **115 / 115** (100%) | **NONE** |
| `student_track_evaluation_sem4` | **5,771** | **5,771** | 115 | **115 / 115** (100%) | **NONE** |
| **Total** | **10,935** | **10,935** | - | **100% Complete** | **NONE** |

---

## 7. Additional Documentation & Guides

- **Technical Schema Spec**: [structure.md](file:///d:/Personal/Projects/migrator/structure.md)
- **PDF Schema Specification**: [structure.pdf](file:///d:/Personal/Projects/migrator/structure.pdf)
- **Database Backup & Restoration Guide**: [DATABASE_BACKUP_GUIDE.md](file:///d:/Personal/Projects/migrator/DATABASE_BACKUP_GUIDE.md)
