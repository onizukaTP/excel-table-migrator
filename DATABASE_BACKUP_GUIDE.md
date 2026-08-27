# MySQL Database Backup, Restoration & Verification Guide

This guide provides step-by-step instructions for managing, backing up, restoring, and querying the **`srm_db`** MySQL database housing all student track evaluation data (`student_track_evaluation_sem2`, `student_track_evaluation_sem3`, `student_track_evaluation_sem4`).

---

## 1. Database Specifications Summary

- **Database Engine**: MySQL 8.0+
- **Database Name**: `srm_db`
- **Primary Key**: `id` (`VARCHAR(50)` storing 15-character student register number e.g. `RA2411029010002`)
- **Live Record Counts**:
  - `student_track_evaluation_sem2`: **2,226 records** (78/78 columns populated, 100% complete)
  - `student_track_evaluation_sem3`: **2,938 records** (115/115 columns populated, 100% complete)
  - `student_track_evaluation_sem4`: **5,771 records** (115/115 columns populated, 100% complete)
  - **Total Records**: **10,935 records**

---

## 2. Quick Backup Commands (`mysqldump`)

### A. Full Database Backup (All Semesters)
```bash
mysqldump -u root -p srm_db > srm_db_full_backup.sql
```

### B. Compressed Backup (Recommended for Storage)
```bash
mysqldump -u root -p srm_db | gzip > srm_db_full_backup.sql.gz
```

### C. Backup Specific Semester Table
```bash
# Semester 2 table backup
mysqldump -u root -p srm_db student_track_evaluation_sem2 > sem2_backup.sql

# Semester 3 table backup
mysqldump -u root -p srm_db student_track_evaluation_sem3 > sem3_backup.sql

# Semester 4 table backup
mysqldump -u root -p srm_db student_track_evaluation_sem4 > sem4_backup.sql
```

---

## 3. Database Restoration Commands

### A. Restore Full Database from SQL Dump
```bash
mysql -u root -p srm_db < srm_db_full_backup.sql
```

### B. Restore Compressed Backup
```bash
gunzip < srm_db_full_backup.sql.gz | mysql -u root -p srm_db
```

---

## 4. Live Data Integrity Verification Routine

Run the following Python one-liner to verify record counts, unique primary key integrity, and column population stats across all flat tables:

```python
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

for sem in (2, 3, 4):
    table = f'student_track_evaluation_sem{sem}'
    cursor.execute(f'SELECT COUNT(*), COUNT(DISTINCT id) FROM `{table}`')
    total, distinct_pks = cursor.fetchone()
    print(f'{table}: Total={total} | Unique PKs={distinct_pks}')

conn.close()
"
```

---

## 5. Helpful SQL Query Examples

### A. Query Student Record by Register Number Across Semesters
```sql
SELECT id, full_name, college_email_id, final_average 
FROM student_track_evaluation_sem2 
WHERE id = 'RA2411003010006';

SELECT id, full_name, college_email_id, final_avg_track 
FROM student_track_evaluation_sem3 
WHERE id = 'RA2411003010006';

SELECT id, full_name, college_email_id, final_avg_track 
FROM student_track_evaluation_sem4 
WHERE id = 'RA2411003010006';
```

### B. Export Semester Data to CSV directly from MySQL
```sql
SELECT * FROM student_track_evaluation_sem2 
INTO OUTFILE '/var/lib/mysql-files/sem2_export.csv' 
FIELDS TERMINATED BY ',' ENCLOSED BY '"' LINES TERMINATED BY '\n';
```
