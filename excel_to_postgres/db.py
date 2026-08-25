import json
import logging
from contextlib import contextmanager
import psycopg2
from psycopg2.extras import Json

logger = logging.getLogger(__name__)

def get_table_name(semester: int) -> str:
    if semester in (2, 3, 4):
        return f"student_track_evaluation_sem{semester}"
    raise ValueError(f"Invalid semester {semester}. Expected 2, 3, or 4.")

class Database:
    def __init__(self, config):
        self.config = config
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.config.db_host,
                port=self.config.db_port,
                dbname=self.config.db_name,
                user=self.config.db_user,
                password=self.config.db_password
            )
            logger.info("Connected to PostgreSQL database '%s' at %s:%s", 
                        self.config.db_name, self.config.db_host, self.config.db_port)
        except Exception as e:
            logger.error("Failed to connect to PostgreSQL database: %s", e)
            raise

    def close(self):
        if self.conn:
            self.conn.close()
            logger.info("Closed PostgreSQL database connection.")

    def ensure_table(self, semester: int):
        """Creates table student_track_evaluation_sem<semester> if not exists."""
        table_name = get_table_name(semester)
        create_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            id             BIGSERIAL PRIMARY KEY,
            student_id     VARCHAR(100) NOT NULL UNIQUE,
            name           VARCHAR(255),
            email          VARCHAR(255),
            data           JSONB
        );
        """
        with self.conn.cursor() as cur:
            cur.execute(create_sql)
        self.conn.commit()
        logger.info("Ensured table '%s' exists.", table_name)

    def upsert_row(self, semester: int, student_id: str, name: str, email: str, data: dict) -> bool:
        """
        Upserts a row into student_track_evaluation_sem<semester> using student_id as conflict target.
        Returns True if a new row was inserted, False if an existing row was updated.
        """
        table_name = get_table_name(semester)
        upsert_sql = f"""
        INSERT INTO {table_name} (student_id, name, email, data)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (student_id)
        DO UPDATE SET
            name  = EXCLUDED.name,
            email = EXCLUDED.email,
            data  = EXCLUDED.data
        RETURNING (xmax = 0) AS is_insert;
        """
        with self.conn.cursor() as cur:
            cur.execute(upsert_sql, (student_id, name, email, Json(data)))
            result = cur.fetchone()
            is_insert = result[0] if result else False
            return is_insert

    def commit(self):
        if self.conn:
            self.conn.commit()

    def rollback(self):
        if self.conn:
            self.conn.rollback()

@contextmanager
def get_db(config):
    db = Database(config)
    db.connect()
    try:
        yield db
    finally:
        db.close()
