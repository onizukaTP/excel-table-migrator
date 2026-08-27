import sys
import logging
import json
from pathlib import Path

# Add project root to sys.path if needed
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from excel_to_postgres.config import Config
from excel_to_postgres.db import Database, get_table_name
from excel_to_postgres.excel_reader import ExcelReader
from excel_to_postgres.json_builder import RecordBuilder

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("migrator")

def run_migration(config: Config):
    target_table = get_table_name(config.semester)
    print("=" * 60)
    print(f"Starting Migration: Semester {config.semester}")
    print(f"Target MySQL Database Table: {target_table}")
    print(f"File: {config.file_path}")
    print(f"Dry Run: {config.dry_run}")
    print(f"Batch Filter: {config.batch_filter}")
    print("=" * 60)

    reader = ExcelReader(
        file_path=config.file_path,
        batch_filter_pattern=config.batch_filter,
        header_rows=2
    )

    builder = RecordBuilder(semester=config.semester)

    db = None
    if not config.dry_run:
        try:
            db = Database(config)
            db.connect()
            db.ensure_table(config.semester)
        except Exception as e:
            logger.error("Database connection or initialization failed: %s", e)
            sys.exit(1)

    total_rows = 0
    successfully_migrated = 0
    updated_existing = 0
    failed_rows = 0
    skipped_rows = 0

    try:
        for sheet_name, row_idx, row_dict, row_list in reader.read_workbook():
            total_rows += 1
            try:
                student_id, name, email, record_dict = builder.process_row(sheet_name, row_dict, row_list)

                if not student_id and not name:
                    skipped_rows += 1
                    non_empty = [str(cell).strip() for cell in row_list if cell is not None and str(cell).strip() != ""]
                    if not non_empty:
                        reason = "Entirely blank row"
                        preview = ""
                    else:
                        reason = "No student register number or name found in row"
                        preview = f" | Values: {non_empty[:4]}"
                    logger.info("[SKIPPED] [Sheet: %s | Row: %d] %s%s", sheet_name, row_idx, reason, preview)
                    continue

                if not record_dict.get("id"):
                    record_dict["id"] = student_id or name or f"UNKNOWN_{sheet_name}_{row_idx}"

                if config.dry_run:
                    successfully_migrated += 1
                    print(f"[DRY-RUN] [Sheet: {sheet_name} | Row: {row_idx}] Student ID: {record_dict['id']} | Name: {name} | Email: {email}")
                    if successfully_migrated == 1:
                        print("\nSample Flat Record preview:")
                        non_null_fields = {k: v for k, v in record_dict.items() if v is not None}
                        print(json.dumps(non_null_fields, indent=2))
                        print("-" * 60)
                else:
                    is_insert = db.upsert_row(
                        semester=config.semester,
                        record_dict=record_dict
                    )
                    if is_insert:
                        successfully_migrated += 1
                    else:
                        updated_existing += 1

            except Exception as row_err:
                failed_rows += 1
                logger.error("[Sheet: %s | Row: %d] Migration failed: %s", sheet_name, row_idx, row_err)

        if db and not config.dry_run:
            db.commit()
            logger.info("Committed transaction to MySQL database '%s' table '%s' successfully.", config.db_name, target_table)

    except Exception as fatal_err:
        if db and not config.dry_run:
            db.rollback()
        logger.error("Fatal migration error: %s", fatal_err)
        sys.exit(1)
    finally:
        if db:
            db.close()

    # Final Migration Summary
    print("\n" + "=" * 60)
    print(f"MIGRATION SUMMARY (Table: {target_table})")
    print("=" * 60)
    print(f"Total rows processed     : {total_rows}")
    print(f"Successfully inserted    : {successfully_migrated}")
    print(f"Updated existing records : {updated_existing}")
    print(f"Failed rows              : {failed_rows}")
    print(f"Skipped rows             : {skipped_rows}")
    print("=" * 60 + "\n")

def main():
    config = Config.parse_args()
    run_migration(config)

if __name__ == "__main__":
    main()
