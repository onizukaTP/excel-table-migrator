# Excel & CSV → PostgreSQL Student Evaluation Migration Tool

A production-ready Python migration tool designed to parse student evaluation data from Excel (`.xlsx`) or CSV (`.csv`) formats (Semesters 2, 3, and 4) and migrate them into dedicated PostgreSQL tables (`student_track_evaluation_sem2`, `student_track_evaluation_sem3`, `student_track_evaluation_sem4`) with tailored `JSONB` data columns.

---

## Key Features

- **Dedicated Semester Tables:** Each semester's evaluation records are stored in its own table (`student_track_evaluation_sem2`, `student_track_evaluation_sem3`, `student_track_evaluation_sem4`).
- **Excel & CSV File Support:** Transparently handles both Excel workbooks (`.xlsx`) and CSV files (`.csv`).
- **Tailored Semester JSON Schemas:** Each semester maps its evaluation tree cleanly without forcing unnecessary null fields from other semesters.
- **Preservation over Calculation:** Raw scores, strings, and inputs are preserved as-is. No averages, tracks, or scores are recalculated.
- **Multi-Sheet Batch Auto-Discovery:** Automatically scans workbooks and processes all sheets matching batch naming patterns (e.g., `B1P1 - Section - A`).
- **Upsert Safety:** Uses `student_id` as the conflict target per semester table. Re-running a migration updates existing records instead of creating duplicates.
- **Robust Error Handling:** Logs row-level failures with sheet name and row numbers, continuing processing safely. Non-student rows (e.g. blank rows/footers) are cleanly skipped.

---

## 1. PostgreSQL Setup

Ensure PostgreSQL (v12+) is installed and running. Create a target database:

```sql
CREATE DATABASE student_db;
```

---

## 2. Database Table Creation

The migration tool automatically creates the appropriate semester table if it does not exist. For manual creation or reference, the DDL statements are:

```sql
-- Semester 2 Table
CREATE TABLE IF NOT EXISTS student_track_evaluation_sem2 (
    id             BIGSERIAL PRIMARY KEY,
    student_id     VARCHAR(100) NOT NULL UNIQUE,
    name           VARCHAR(255),
    email          VARCHAR(255),
    data           JSONB
);

-- Semester 3 Table
CREATE TABLE IF NOT EXISTS student_track_evaluation_sem3 (
    id             BIGSERIAL PRIMARY KEY,
    student_id     VARCHAR(100) NOT NULL UNIQUE,
    name           VARCHAR(255),
    email          VARCHAR(255),
    data           JSONB
);

-- Semester 4 Table
CREATE TABLE IF NOT EXISTS student_track_evaluation_sem4 (
    id             BIGSERIAL PRIMARY KEY,
    student_id     VARCHAR(100) NOT NULL UNIQUE,
    name           VARCHAR(255),
    email          VARCHAR(255),
    data           JSONB
);
```

---

## 3. Python Environment Setup

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

## 4. Installing Dependencies

Install required dependencies:

```bash
pip install -r requirements.txt
```

*Dependencies: `openpyxl`, `psycopg2-binary`, `python-dotenv`.*

---

## 5. Configuring `.env`

Copy `.env.example` to `.env` and fill in your database credentials:

```bash
cp .env.example .env
```

`.env` example content:

```env
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=student_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password_here
```

---

## 6. Running Semester 2 Migration

Run migration for Semester 2 (targets `student_track_evaluation_sem2`):

```bash
python excel_to_postgres/migrate.py --file path/to/semester_2.xlsx --semester 2
```

To test without modifying PostgreSQL, add `--dry-run`:

```bash
python excel_to_postgres/migrate.py --file path/to/semester_2.xlsx --semester 2 --dry-run
```

---

## 7. Running Semester 3 Migration

Run migration for Semester 3 (targets `student_track_evaluation_sem3`):

```bash
python excel_to_postgres/migrate.py --file path/to/semester_3.xlsx --semester 3
```

---

## 8. Running Semester 4 Migration

Run migration for Semester 4 (targets `student_track_evaluation_sem4`):

```bash
python excel_to_postgres/migrate.py --file path/to/semester_4.xlsx --semester 4
```

*Optional:* Filter to specific batch sheets using `--batch-filter`:

```bash
python excel_to_postgres/migrate.py --file path/to/semester_4.xlsx --semester 4 --batch-filter "^B1P"
```

---

## 9. Re-running a Migration Safely

The database uses PostgreSQL `ON CONFLICT (student_id) DO UPDATE` per table.

If you run the migration tool multiple times on the same Excel file or updated Excel data:
- **No duplicate rows will be created.**
- Existing records matching `student_id` in `student_track_evaluation_sem<N>` will have their `name`, `email`, and `data` JSON updated with the latest values.

---

## 10. Blank Values & Data Preservation

- Blank Excel cells, empty string cells (`""`), and `NaN` float values are converted to JSON `null`.
- Floating-point `NaN` is sanitized recursively before insertion to ensure strict PostgreSQL JSONB compliance.
- Scores, levels, and tracks are preserved exactly as present in input files without recalculation.
