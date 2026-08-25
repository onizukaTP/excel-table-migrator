import argparse
import os
import re
from pathlib import Path
from dotenv import load_dotenv

# Load .env if present
load_dotenv()

class Config:
    def __init__(self, args=None):
        # DB Credentials from environment variables
        self.db_host = os.getenv("POSTGRES_HOST", "localhost")
        self.db_port = int(os.getenv("POSTGRES_PORT", "5432"))
        self.db_name = os.getenv("POSTGRES_DB", "postgres")
        self.db_user = os.getenv("POSTGRES_USER", "postgres")
        self.db_password = os.getenv("POSTGRES_PASSWORD", "")

        # CLI settings
        if args:
            self.file_path = args.file
            self.semester = args.semester
            self.dry_run = args.dry_run
            self.batch_filter = args.batch_filter
        else:
            self.file_path = None
            self.semester = None
            self.dry_run = False
            self.batch_filter = r"^B\d+P\d+"

    @classmethod
    def parse_args(cls, sys_args=None):
        parser = argparse.ArgumentParser(
            description="Migrate student evaluation Excel files to PostgreSQL student_evaluations table."
        )
        parser.add_argument(
            "--file",
            required=True,
            help="Path to the Excel file (.xlsx)"
        )
        parser.add_argument(
            "--semester",
            type=int,
            required=True,
            choices=[2, 3, 4],
            help="Semester number (2, 3, or 4)"
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Parse and validate without inserting into PostgreSQL"
        )
        parser.add_argument(
            "--batch-filter",
            default=r"^B\d+P\d+",
            help="Regex pattern to match sheet names (default: '^B\\d+P\\d+')"
        )

        args = parser.parse_args(sys_args)
        
        # Validation
        file_p = Path(args.file)
        if not file_p.exists():
            parser.error(f"Excel file not found: {args.file}")
        
        try:
            re.compile(args.batch_filter)
        except re.error as e:
            parser.error(f"Invalid regex pattern for --batch-filter: {e}")

        return cls(args)
