import logging
from contextlib import contextmanager
import mysql.connector

logger = logging.getLogger(__name__)

def get_table_name(semester: int) -> str:
    if semester in (2, 3, 4):
        return f"student_track_evaluation_sem{semester}"
    raise ValueError(f"Invalid semester {semester}. Expected 2, 3, or 4.")

DDL_SEM2 = """
CREATE TABLE IF NOT EXISTS student_track_evaluation_sem2 (
    id VARCHAR(50) PRIMARY KEY,
    sn INT,
    full_name VARCHAR(255),
    college_email_id VARCHAR(255),
    assignment_submission VARCHAR(255),
    engagement_status VARCHAR(255),

    core_level TEXT,
    core_class_practice VARCHAR(255),
    core_assignment VARCHAR(255),
    core_tech_input_t1 DECIMAL(5,2),
    core_tech_input_t2 DECIMAL(5,2),
    core_tech_input_t3 DECIMAL(5,2),
    core_tech_input_t4 DECIMAL(5,2),
    core_learn_input_l1 DECIMAL(5,2),
    core_learn_input_l2 DECIMAL(5,2),
    core_learn_input_l3 DECIMAL(5,2),
    core_learn_input_l4 DECIMAL(5,2),
    core_comm_input_c1 DECIMAL(5,2),
    core_comm_input_c2 DECIMAL(5,2),
    core_comm_input_c3 DECIMAL(5,2),
    core_comm_input_c4 DECIMAL(5,2),
    core_tech_score_t1 DECIMAL(5,2),
    core_tech_score_t2 DECIMAL(5,2),
    core_tech_score_t3 DECIMAL(5,2),
    core_tech_score_t4 DECIMAL(5,2),
    core_learn_score_l1 DECIMAL(5,2),
    core_learn_score_l2 DECIMAL(5,2),
    core_learn_score_l3 DECIMAL(5,2),
    core_learn_score_l4 DECIMAL(5,2),
    core_learn_score_combined DECIMAL(5,2),
    core_level_computed TEXT,
    core_comm_score_c1 DECIMAL(5,2),
    core_comm_score_c2 DECIMAL(5,2),
    core_comm_score_c3 DECIMAL(5,2),
    core_comm_score_c4 DECIMAL(5,2),
    core_summary_t DECIMAL(5,2),
    core_summary_l DECIMAL(5,2),
    core_summary_c DECIMAL(5,2),
    core_total_score DECIMAL(5,2),
    core_help_status VARCHAR(255),
    core_coding_level TEXT,
    core_review_comments TEXT,

    logical_level TEXT,
    logical_class_practice VARCHAR(255),
    logical_assignment VARCHAR(255),
    logical_tech_input_t1 DECIMAL(5,2),
    logical_tech_input_t2 DECIMAL(5,2),
    logical_tech_input_t3 DECIMAL(5,2),
    logical_tech_input_t4 DECIMAL(5,2),
    logical_learn_input_l1 DECIMAL(5,2),
    logical_learn_input_l2 DECIMAL(5,2),
    logical_learn_input_l3 DECIMAL(5,2),
    logical_learn_input_l4 DECIMAL(5,2),
    logical_comm_input_c1 DECIMAL(5,2),
    logical_comm_input_c2 DECIMAL(5,2),
    logical_comm_input_c3 DECIMAL(5,2),
    logical_comm_input_c4 DECIMAL(5,2),
    logical_tech_score_t1 DECIMAL(5,2),
    logical_tech_score_t2 DECIMAL(5,2),
    logical_tech_score_t3 DECIMAL(5,2),
    logical_tech_score_t4 DECIMAL(5,2),
    logical_learn_score_l1 DECIMAL(5,2),
    logical_learn_score_l2 DECIMAL(5,2),
    logical_learn_score_l3 DECIMAL(5,2),
    logical_learn_score_l4 DECIMAL(5,2),
    logical_learn_score_combined DECIMAL(5,2),
    logical_level_computed TEXT,
    logical_comm_score_c1 DECIMAL(5,2),
    logical_comm_score_c2 DECIMAL(5,2),
    logical_comm_score_c3 DECIMAL(5,2),
    logical_comm_score_c4 DECIMAL(5,2),
    logical_summary_t DECIMAL(5,2),
    logical_summary_l DECIMAL(5,2),
    logical_summary_c DECIMAL(5,2),
    logical_total_score DECIMAL(5,2),
    logical_help_status VARCHAR(255),
    logical_coding_level TEXT,
    logical_review_comments TEXT,

    oop_level TEXT,
    oop_class_practice VARCHAR(255),
    oop_assignment VARCHAR(255),
    oop_tech_input_t1 DECIMAL(5,2),
    oop_tech_input_t2 DECIMAL(5,2),
    oop_tech_input_t3 DECIMAL(5,2),
    oop_tech_input_t4 DECIMAL(5,2),
    oop_learn_input_l1 DECIMAL(5,2),
    oop_learn_input_l2 DECIMAL(5,2),
    oop_learn_input_l3 DECIMAL(5,2),
    oop_learn_input_l4 DECIMAL(5,2),
    oop_comm_input_c1 DECIMAL(5,2),
    oop_comm_input_c2 DECIMAL(5,2),
    oop_comm_input_c3 DECIMAL(5,2),
    oop_comm_input_c4 DECIMAL(5,2),
    oop_tech_score_t1 DECIMAL(5,2),
    oop_tech_score_t2 DECIMAL(5,2),
    oop_tech_score_t3 DECIMAL(5,2),
    oop_tech_score_t4 DECIMAL(5,2),
    oop_learn_score_l1 DECIMAL(5,2),
    oop_learn_score_l2 DECIMAL(5,2),
    oop_learn_score_l3 DECIMAL(5,2),
    oop_learn_score_l4 DECIMAL(5,2),
    oop_learn_score_combined DECIMAL(5,2),
    oop_level_computed TEXT,
    oop_comm_score_c1 DECIMAL(5,2),
    oop_comm_score_c2 DECIMAL(5,2),
    oop_comm_score_c3 DECIMAL(5,2),
    oop_comm_score_c4 DECIMAL(5,2),
    oop_summary_t DECIMAL(5,2),
    oop_summary_l DECIMAL(5,2),
    oop_summary_c DECIMAL(5,2),
    oop_total_score DECIMAL(5,2),
    oop_help_status VARCHAR(255),
    oop_coding_level TEXT,
    oop_review_comments TEXT,

    core_final VARCHAR(255),
    logical_final VARCHAR(255),
    oop_final VARCHAR(255),
    final_avg_track VARCHAR(255)
);
"""

DDL_SEM3 = """
CREATE TABLE IF NOT EXISTS student_track_evaluation_sem3 (
    id VARCHAR(50) PRIMARY KEY,
    sn INT,
    full_name VARCHAR(255),
    college_email_id VARCHAR(255),
    assignment_submission VARCHAR(255),
    engagement_status VARCHAR(255),

    string_level TEXT,
    string_class_practice VARCHAR(255),
    string_assignment VARCHAR(255),
    string_tech_input_t1 DECIMAL(5,2),
    string_tech_input_t2 DECIMAL(5,2),
    string_tech_input_t3 DECIMAL(5,2),
    string_tech_input_t4 DECIMAL(5,2),
    string_learn_input_l1 DECIMAL(5,2),
    string_learn_input_l2 DECIMAL(5,2),
    string_learn_input_l3 DECIMAL(5,2),
    string_learn_input_l4 DECIMAL(5,2),
    string_comm_input_c1 DECIMAL(5,2),
    string_comm_input_c2 DECIMAL(5,2),
    string_comm_input_c3 DECIMAL(5,2),
    string_comm_input_c4 DECIMAL(5,2),
    string_tech_score_t1 DECIMAL(5,2),
    string_tech_score_t2 DECIMAL(5,2),
    string_tech_score_t3 DECIMAL(5,2),
    string_tech_score_t4 DECIMAL(5,2),
    string_learn_score_l1 DECIMAL(5,2),
    string_learn_score_l2 DECIMAL(5,2),
    string_learn_score_l3 DECIMAL(5,2),
    string_learn_score_l4 DECIMAL(5,2),
    string_learn_score_combined DECIMAL(5,2),
    string_level_computed TEXT,
    string_comm_score_c1 DECIMAL(5,2),
    string_comm_score_c2 DECIMAL(5,2),
    string_comm_score_c3 DECIMAL(5,2),
    string_comm_score_c4 DECIMAL(5,2),
    string_summary_t DECIMAL(5,2),
    string_summary_l DECIMAL(5,2),
    string_summary_c DECIMAL(5,2),
    string_total_score DECIMAL(5,2),
    string_help_status VARCHAR(255),
    string_coding_level TEXT,
    string_review_comments TEXT,

    oop_level TEXT,
    oop_class_practice VARCHAR(255),
    oop_assignment VARCHAR(255),
    oop_tech_input_t1 DECIMAL(5,2),
    oop_tech_input_t2 DECIMAL(5,2),
    oop_tech_input_t3 DECIMAL(5,2),
    oop_tech_input_t4 DECIMAL(5,2),
    oop_learn_input_l1 DECIMAL(5,2),
    oop_learn_input_l2 DECIMAL(5,2),
    oop_learn_input_l3 DECIMAL(5,2),
    oop_learn_input_l4 DECIMAL(5,2),
    oop_comm_input_c1 DECIMAL(5,2),
    oop_comm_input_c2 DECIMAL(5,2),
    oop_comm_input_c3 DECIMAL(5,2),
    oop_comm_input_c4 DECIMAL(5,2),
    oop_tech_score_t1 DECIMAL(5,2),
    oop_tech_score_t2 DECIMAL(5,2),
    oop_tech_score_t3 DECIMAL(5,2),
    oop_tech_score_t4 DECIMAL(5,2),
    oop_learn_score_l1 DECIMAL(5,2),
    oop_learn_score_l2 DECIMAL(5,2),
    oop_learn_score_l3 DECIMAL(5,2),
    oop_learn_score_l4 DECIMAL(5,2),
    oop_learn_score_combined DECIMAL(5,2),
    oop_level_computed TEXT,
    oop_comm_score_c1 DECIMAL(5,2),
    oop_comm_score_c2 DECIMAL(5,2),
    oop_comm_score_c3 DECIMAL(5,2),
    oop_comm_score_c4 DECIMAL(5,2),
    oop_summary_t DECIMAL(5,2),
    oop_summary_l DECIMAL(5,2),
    oop_summary_c DECIMAL(5,2),
    oop_total_score DECIMAL(5,2),
    oop_help_status VARCHAR(255),
    oop_coding_level TEXT,
    oop_review_comments TEXT,

    adv_oop_level TEXT,
    adv_oop_class_practice VARCHAR(255),
    adv_oop_assignment VARCHAR(255),
    adv_oop_tech_input_t1 DECIMAL(5,2),
    adv_oop_tech_input_t2 DECIMAL(5,2),
    adv_oop_tech_input_t3 DECIMAL(5,2),
    adv_oop_tech_input_t4 DECIMAL(5,2),
    adv_oop_learn_input_l1 DECIMAL(5,2),
    adv_oop_learn_input_l2 DECIMAL(5,2),
    adv_oop_learn_input_l3 DECIMAL(5,2),
    adv_oop_learn_input_l4 DECIMAL(5,2),
    adv_oop_comm_input_c1 DECIMAL(5,2),
    adv_oop_comm_input_c2 DECIMAL(5,2),
    adv_oop_comm_input_c3 DECIMAL(5,2),
    adv_oop_comm_input_c4 DECIMAL(5,2),
    adv_oop_tech_score_t1 DECIMAL(5,2),
    adv_oop_tech_score_t2 DECIMAL(5,2),
    adv_oop_tech_score_t3 DECIMAL(5,2),
    adv_oop_tech_score_t4 DECIMAL(5,2),
    adv_oop_learn_score_l1 DECIMAL(5,2),
    adv_oop_learn_score_l2 DECIMAL(5,2),
    adv_oop_learn_score_l3 DECIMAL(5,2),
    adv_oop_learn_score_l4 DECIMAL(5,2),
    adv_oop_learn_score_combined DECIMAL(5,2),
    adv_oop_level_computed TEXT,
    adv_oop_comm_score_c1 DECIMAL(5,2),
    adv_oop_comm_score_c2 DECIMAL(5,2),
    adv_oop_comm_score_c3 DECIMAL(5,2),
    adv_oop_comm_score_c4 DECIMAL(5,2),
    adv_oop_summary_t DECIMAL(5,2),
    adv_oop_summary_l DECIMAL(5,2),
    adv_oop_summary_c DECIMAL(5,2),
    adv_oop_total_score DECIMAL(5,2),
    adv_oop_help_status VARCHAR(255),
    adv_oop_coding_level TEXT,
    adv_oop_review_comments TEXT,

    string_final VARCHAR(255),
    oop_final VARCHAR(255),
    adv_oop_final VARCHAR(255),
    final_avg_track VARCHAR(255)
);
"""

DDL_SEM4 = """
CREATE TABLE IF NOT EXISTS student_track_evaluation_sem4 (
    id VARCHAR(50) PRIMARY KEY,
    sn INT,
    full_name VARCHAR(255),
    college_email_id VARCHAR(255),
    assignment_submission VARCHAR(255),
    engagement_status VARCHAR(255),

    dsa_level TEXT,
    dsa_class_practice VARCHAR(255),
    dsa_assignment VARCHAR(255),
    dsa_tech_input_t1 DECIMAL(5,2),
    dsa_tech_input_t2 DECIMAL(5,2),
    dsa_tech_input_t3 DECIMAL(5,2),
    dsa_tech_input_t4 DECIMAL(5,2),
    dsa_learn_input_l1 DECIMAL(5,2),
    dsa_learn_input_l2 DECIMAL(5,2),
    dsa_learn_input_l3 DECIMAL(5,2),
    dsa_learn_input_l4 DECIMAL(5,2),
    dsa_comm_input_c1 DECIMAL(5,2),
    dsa_comm_input_c2 DECIMAL(5,2),
    dsa_comm_input_c3 DECIMAL(5,2),
    dsa_comm_input_c4 DECIMAL(5,2),
    dsa_tech_score_t1 DECIMAL(5,2),
    dsa_tech_score_t2 DECIMAL(5,2),
    dsa_tech_score_t3 DECIMAL(5,2),
    dsa_tech_score_t4 DECIMAL(5,2),
    dsa_learn_score_l1 DECIMAL(5,2),
    dsa_learn_score_l2 DECIMAL(5,2),
    dsa_learn_score_l3 DECIMAL(5,2),
    dsa_learn_score_l4 DECIMAL(5,2),
    dsa_learn_score_combined DECIMAL(5,2),
    dsa_level_computed TEXT,
    dsa_comm_score_c1 DECIMAL(5,2),
    dsa_comm_score_c2 DECIMAL(5,2),
    dsa_comm_score_c3 DECIMAL(5,2),
    dsa_comm_score_c4 DECIMAL(5,2),
    dsa_summary_t DECIMAL(5,2),
    dsa_summary_l DECIMAL(5,2),
    dsa_summary_c DECIMAL(5,2),
    dsa_total_score DECIMAL(5,2),
    dsa_help_status VARCHAR(255),
    dsa_coding_level TEXT,
    dsa_review_comments TEXT,

    collections_level TEXT,
    collections_class_practice VARCHAR(255),
    collections_assignment VARCHAR(255),
    collections_tech_input_t1 DECIMAL(5,2),
    collections_tech_input_t2 DECIMAL(5,2),
    collections_tech_input_t3 DECIMAL(5,2),
    collections_tech_input_t4 DECIMAL(5,2),
    collections_learn_input_l1 DECIMAL(5,2),
    collections_learn_input_l2 DECIMAL(5,2),
    collections_learn_input_l3 DECIMAL(5,2),
    collections_learn_input_l4 DECIMAL(5,2),
    collections_comm_input_c1 DECIMAL(5,2),
    collections_comm_input_c2 DECIMAL(5,2),
    collections_comm_input_c3 DECIMAL(5,2),
    collections_comm_input_c4 DECIMAL(5,2),
    collections_tech_score_t1 DECIMAL(5,2),
    collections_tech_score_t2 DECIMAL(5,2),
    collections_tech_score_t3 DECIMAL(5,2),
    collections_tech_score_t4 DECIMAL(5,2),
    collections_learn_score_l1 DECIMAL(5,2),
    collections_learn_score_l2 DECIMAL(5,2),
    collections_learn_score_l3 DECIMAL(5,2),
    collections_learn_score_l4 DECIMAL(5,2),
    collections_learn_score_combined DECIMAL(5,2),
    collections_level_computed TEXT,
    collections_comm_score_c1 DECIMAL(5,2),
    collections_comm_score_c2 DECIMAL(5,2),
    collections_comm_score_c3 DECIMAL(5,2),
    collections_comm_score_c4 DECIMAL(5,2),
    collections_summary_t DECIMAL(5,2),
    collections_summary_l DECIMAL(5,2),
    collections_summary_c DECIMAL(5,2),
    collections_total_score DECIMAL(5,2),
    collections_help_status VARCHAR(255),
    collections_coding_level TEXT,
    collections_review_comments TEXT,

    java_adv_level TEXT,
    java_adv_class_practice VARCHAR(255),
    java_adv_assignment VARCHAR(255),
    java_adv_tech_input_t1 DECIMAL(5,2),
    java_adv_tech_input_t2 DECIMAL(5,2),
    java_adv_tech_input_t3 DECIMAL(5,2),
    java_adv_tech_input_t4 DECIMAL(5,2),
    java_adv_learn_input_l1 DECIMAL(5,2),
    java_adv_learn_input_l2 DECIMAL(5,2),
    java_adv_learn_input_l3 DECIMAL(5,2),
    java_adv_learn_input_l4 DECIMAL(5,2),
    java_adv_comm_input_c1 DECIMAL(5,2),
    java_adv_comm_input_c2 DECIMAL(5,2),
    java_adv_comm_input_c3 DECIMAL(5,2),
    java_adv_comm_input_c4 DECIMAL(5,2),
    java_adv_tech_score_t1 DECIMAL(5,2),
    java_adv_tech_score_t2 DECIMAL(5,2),
    java_adv_tech_score_t3 DECIMAL(5,2),
    java_adv_tech_score_t4 DECIMAL(5,2),
    java_adv_learn_score_l1 DECIMAL(5,2),
    java_adv_learn_score_l2 DECIMAL(5,2),
    java_adv_learn_score_l3 DECIMAL(5,2),
    java_adv_learn_score_l4 DECIMAL(5,2),
    java_adv_learn_score_combined DECIMAL(5,2),
    java_adv_level_computed TEXT,
    java_adv_comm_score_c1 DECIMAL(5,2),
    java_adv_comm_score_c2 DECIMAL(5,2),
    java_adv_comm_score_c3 DECIMAL(5,2),
    java_adv_comm_score_c4 DECIMAL(5,2),
    java_adv_summary_t DECIMAL(5,2),
    java_adv_summary_l DECIMAL(5,2),
    java_adv_summary_c DECIMAL(5,2),
    java_adv_total_score DECIMAL(5,2),
    java_adv_help_status VARCHAR(255),
    java_adv_coding_level TEXT,
    java_adv_review_comments TEXT,

    dsa_final VARCHAR(255),
    collections_final VARCHAR(255),
    java_adv_final VARCHAR(255),
    final_avg_track VARCHAR(255)
);
"""

DDLS = {
    2: DDL_SEM2,
    3: DDL_SEM3,
    4: DDL_SEM4
}

class Database:
    def __init__(self, config):
        self.config = config
        self.conn = None

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.config.db_host,
                port=self.config.db_port,
                database=self.config.db_name,
                user=self.config.db_user,
                password=self.config.db_password
            )
            logger.info("Connected to MySQL database '%s' at %s:%s", 
                        self.config.db_name, self.config.db_host, self.config.db_port)
        except Exception as e:
            logger.error("Failed to connect to MySQL database: %s", e)
            raise

    def close(self):
        if self.conn and self.conn.is_connected():
            self.conn.close()
            logger.info("Closed MySQL database connection.")

    def ensure_table(self, semester: int):
        """Creates flat table student_track_evaluation_sem<semester> with `id` (student register number) as PRIMARY KEY."""
        table_name = get_table_name(semester)
        ddl = DDLS.get(semester)
        if not ddl:
            raise ValueError(f"No DDL defined for semester {semester}")

        cursor = self.conn.cursor()
        
        # Check if table has old surrogate student_id column and drop if needed to re-create with id PRIMARY KEY
        try:
            cursor.execute(f"SHOW COLUMNS FROM `{table_name}` LIKE 'student_id';")
            if cursor.fetchone():
                logger.info("Recreating table '%s' to set 'id' (register number) as PRIMARY KEY...", table_name)
                cursor.execute(f"DROP TABLE IF EXISTS `{table_name}`;")
                self.conn.commit()
        except Exception:
            pass

        cursor.execute(ddl)
        self.conn.commit()
        cursor.close()
        logger.info("Ensured MySQL table '%s' exists with 'id' (15-char register number) as PRIMARY KEY.", table_name)

    def upsert_row(self, semester: int, record_dict: dict) -> bool:
        """
        Upserts a flat record dict into student_track_evaluation_sem<semester>.
        Uses ON DUPLICATE KEY UPDATE based on `id` (15-char student register number PRIMARY KEY).
        Returns True if a new row was inserted, False if an existing row was updated.
        """
        table_name = get_table_name(semester)
        
        # Extract column names and values
        cols = list(record_dict.keys())
        val_placeholders = ", ".join(["%s"] * len(cols))
        col_names = ", ".join([f"`{c}`" for c in cols])
        
        # Construct ON DUPLICATE KEY UPDATE clause (exclude primary key `id` from update)
        update_assignments = ", ".join([f"`{c}`=VALUES(`{c}`)" for c in cols if c != "id"])

        upsert_sql = f"""
        INSERT INTO {table_name} ({col_names})
        VALUES ({val_placeholders})
        ON DUPLICATE KEY UPDATE {update_assignments};
        """

        values = [record_dict[c] for c in cols]

        cursor = self.conn.cursor()
        cursor.execute(upsert_sql, values)
        is_insert = cursor.rowcount == 1
        cursor.close()
        return is_insert

    def commit(self):
        if self.conn and self.conn.is_connected():
            self.conn.commit()

    def rollback(self):
        if self.conn and self.conn.is_connected():
            self.conn.rollback()

@contextmanager
def get_db(config):
    db = Database(config)
    db.connect()
    try:
        yield db
    finally:
        db.close()
