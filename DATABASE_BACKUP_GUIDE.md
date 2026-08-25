# MySQL Database Backup, Restoration & Verification Guide

This guide provides step-by-step instructions for managing, backing up, restoring, and querying the **`srm_db`** MySQL database housing all student track evaluation data (`student_track_evaluation_sem2`, `student_track_evaluation_sem3`, `student_track_evaluation_sem4`).

---

## 1. Live Data Verification Report

A full database verification was performed on your live MySQL instance (`srm_db`):

| Database Table | Total Records | Unique Student Register IDs (`id` PRIMARY KEY) | Data Health Status |
| :--- | :--- | :--- | :--- |
| **`student_track_evaluation_sem2`** | **5,798** | **5,798** | 100% Verified (0 Duplicates) |
| **`student_track_evaluation_sem3`** | **5,818** | **5,818** | 100% Verified (0 Duplicates) |
| **`student_track_evaluation_sem4`** | **5,771** | **5,771** | 100% Verified (0 Duplicates) |
| **TOTAL MIGRATED RECORDS** | **17,387** | **17,387** | **100% Integrity Verified** |

> [!NOTE]
> All student register numbers (e.g. `RA2411003010001`, `RA2411029010002`) are set as **PRIMARY KEYS**, guaranteeing zero duplicate rows across re-runs.

---

## 2. Quick Verification Script

You can verify table counts and sample records anytime by running this Python command in PowerShell:

```powershell
python -c "
import mysql.connector, os
from dotenv import load_dotenv
load_dotenv()

conn = mysql.connector.connect(
    host=os.getenv('MYSQL_HOST', 'localhost'),
    port=int(os.getenv('MYSQL_PORT', 3306)),
    database=os.getenv('MYSQL_DB', 'srm_db'),
    user=os.getenv('MYSQL_USER', 'root'),
    password=os.getenv('MYSQL_PASSWORD', 'root')
)
cursor = conn.cursor()

tables = ['student_track_evaluation_sem2', 'student_track_evaluation_sem3', 'student_track_evaluation_sem4']
for t in tables:
    cursor.execute(f'SELECT COUNT(*), COUNT(DISTINCT id) FROM `{t}`')
    total, distinct_id = cursor.fetchone()
    print(f'{t}: Total Rows = {total} | Unique PKs = {distinct_id}')

cursor.close()
conn.close()
"
```

---

## 3. How to Backup the Database

### Method A: Using `mysqldump` (Command Line)

`mysqldump` is the standard MySQL utility for generating a single `.sql` file containing all table structure DDLs and data INSERT statements.

#### 1. Full Database Backup (All Semesters)
Run in PowerShell / Command Prompt (replace password if necessary):

```powershell
mysqldump -u root -p srm_db > srm_db_backup_full.sql
```

#### 2. Compressed Full Backup (Recommended for Storage)
If PowerShell has `gzip` installed or using Command Prompt:

```powershell
mysqldump -u root -p srm_db | gzip > srm_db_backup_full.sql.gz
```

#### 3. Single Table Backup
To back up only a specific semester (e.g. Semester 2):

```powershell
mysqldump -u root -p srm_db student_track_evaluation_sem2 > srm_db_sem2_backup.sql
```

---

### Method B: Using MySQL Workbench (GUI)

1. Open **MySQL Workbench** and connect to your local instance (`localhost:3306`).
2. In the left navigation menu under **Management**, click **Data Export**.
3. Under **Tables to Export**, select **`srm_db`** and check all three semester tables:
   - `student_track_evaluation_sem2`
   - `student_track_evaluation_sem3`
   - `student_track_evaluation_sem4`
4. Choose **Export to Self-Contained File**.
5. Select file destination (e.g., `D:\Backups\srm_db_full_backup.sql`).
6. Click **Start Export**.

---

### Method C: Using DBeaver (GUI)

1. Open **DBeaver** and expand your `srm_db` MySQL connection.
2. Right-click on **`srm_db`** (or select all 3 tables), then click **Tools** → **Dump database**.
3. Select output folder and file format (`.sql`).
4. Click **Start**.

---

## 4. How to Restore a Database Backup

### Method A: Restoring via Command Line (`mysql` CLI)

If you need to restore your database from a `.sql` backup file (e.g., `srm_db_backup_full.sql`):

#### 1. Ensure Target Database Exists
Open MySQL shell or run:

```powershell
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS srm_db;"
```

#### 2. Execute Restoration Command
Run:

```powershell
mysql -u root -p srm_db < srm_db_backup_full.sql
```

---

### Method B: Restoring via MySQL Workbench (GUI)

1. Open **MySQL Workbench**.
2. Under **Management**, click **Data Import/Restore**.
3. Select **Import from Self-Contained File** and browse to your `.sql` file.
4. Select Target Schema: **`srm_db`**.
5. Click **Start Import**.

---

## 5. Querying & Analyzing the Database

Here are essential SQL queries to search and evaluate student data directly in MySQL:

### 1. Lookup Student Record by Register Number (`id`) Across All Semesters
```sql
SELECT 'Sem 2' AS Semester, id, full_name, core_total_score, logical_total_score, oop_total_score 
FROM student_track_evaluation_sem2 
WHERE id = 'RA2411003010001'

UNION ALL

SELECT 'Sem 3' AS Semester, id, full_name, string_total_score, oop_total_score, adv_oop_total_score 
FROM student_track_evaluation_sem3 
WHERE id = 'RA2411003010001'

UNION ALL

SELECT 'Sem 4' AS Semester, id, full_name, dsa_total_score, collections_total_score, java_adv_total_score 
FROM student_track_evaluation_sem4 
WHERE id = 'RA2411003010001';
```

### 2. Export Semester Data to CSV File via SQL
```sql
SELECT * FROM student_track_evaluation_sem4
INTO OUTFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/sem4_export.csv'
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';
```

---

## 6. Automating Daily Backups (Windows Task Scheduler)

You can set up automatic daily backups using a simple PowerShell script:

1. Create a script named `backup_db.ps1`:
   ```powershell
   $Date = Get-Date -Format "yyyy-MM-dd_HHmm"
   $BackupPath = "D:\Personal\Projects\migrator\backups\srm_db_backup_$Date.sql"
   New-Item -ItemType Directory -Force -Path "D:\Personal\Projects\migrator\backups"
   & "C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe" -u root -proot srm_db > $BackupPath
   ```
2. Schedule it to run daily in **Windows Task Scheduler** pointing to `powershell.exe -ExecutionPolicy Bypass -File D:\Personal\Projects\migrator\backup_db.ps1`.
