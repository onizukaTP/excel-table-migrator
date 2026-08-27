import logging
from contextlib import contextmanager
import mysql.connector

logger = logging.getLogger(__name__)

def get_table_name(semester: int) -> str:
    if semester in (2, 3, 4):
        return f"student_track_evaluation_sem{semester}"
    raise ValueError(f"Invalid semester {semester}. Expected 2, 3, or 4.")

# ──────────────────────────────────────────────────────────────────────
# Semester 2 DDL
# ──────────────────────────────────────────────────────────────────────
# Input metrics: VARCHAR(255) / TEXT (words like 'Good', 'Average', 'Level1')
# Score metrics: DECIMAL(5,2) (numbers like 0.95, 4.75)
# ──────────────────────────────────────────────────────────────────────
DDL_SEM2 = """
CREATE TABLE IF NOT EXISTS student_track_evaluation_sem2 (
    id VARCHAR(50) PRIMARY KEY,
    sn INT,
    full_name VARCHAR(255),
    college_email_id VARCHAR(255),
    gmail_id VARCHAR(255),
    num_reviews VARCHAR(255),
    regularity_attendance VARCHAR(255),
    assignment_submission VARCHAR(255),

    -- Programming Construct (Input: 7 cols)
    prog_level TEXT,
    prog_review VARCHAR(255),
    prog_learnability VARCHAR(255),
    prog_technicality VARCHAR(255),
    prog_communicability VARCHAR(255),
    prog_review_comment TEXT,
    prog_coding_level TEXT,

    -- Control Flow (Input: 7 cols)
    cf_level TEXT,
    cf_review VARCHAR(255),
    cf_learnability VARCHAR(255),
    cf_technicality VARCHAR(255),
    cf_communicability VARCHAR(255),
    cf_review_comment TEXT,
    cf_coding_level TEXT,

    -- Arrays (Input: 7 cols)
    arr_level TEXT,
    arr_review VARCHAR(255),
    arr_learnability VARCHAR(255),
    arr_technicality VARCHAR(255),
    arr_communicability VARCHAR(255),
    arr_review_comment TEXT,
    arr_coding_level TEXT,

    -- Methods (Input: 7 cols)
    meth_level TEXT,
    meth_review VARCHAR(255),
    meth_learnability VARCHAR(255),
    meth_technicality VARCHAR(255),
    meth_communicability VARCHAR(255),
    meth_review_comment TEXT,
    meth_coding_level TEXT,

    -- Strings (Input: 7 cols)
    str_level TEXT,
    str_review VARCHAR(255),
    str_learnability VARCHAR(255),
    str_technicality VARCHAR(255),
    str_communicability VARCHAR(255),
    str_review_comment TEXT,
    str_coding_level TEXT,

    -- Programming Construct Score (6 cols)
    prog_score_level DECIMAL(5,2),
    prog_score_review DECIMAL(5,2),
    prog_score_learnability DECIMAL(5,2),
    prog_score_technicality DECIMAL(5,2),
    prog_score_communicability DECIMAL(5,2),
    prog_score_total DECIMAL(5,2),

    -- Control Flow Score (6 cols)
    cf_score_level DECIMAL(5,2),
    cf_score_review DECIMAL(5,2),
    cf_score_learnability DECIMAL(5,2),
    cf_score_technicality DECIMAL(5,2),
    cf_score_communicability DECIMAL(5,2),
    cf_score_total DECIMAL(5,2),

    -- Arrays Score (6 cols)
    arr_score_level DECIMAL(5,2),
    arr_score_review DECIMAL(5,2),
    arr_score_learnability DECIMAL(5,2),
    arr_score_technicality DECIMAL(5,2),
    arr_score_communicability DECIMAL(5,2),
    arr_score_total DECIMAL(5,2),

    -- Methods Score (6 cols)
    meth_score_level DECIMAL(5,2),
    meth_score_review DECIMAL(5,2),
    meth_score_learnability DECIMAL(5,2),
    meth_score_technicality DECIMAL(5,2),
    meth_score_communicability DECIMAL(5,2),
    meth_score_total DECIMAL(5,2),

    -- Strings Score (6 cols)
    str_score_level DECIMAL(5,2),
    str_score_review DECIMAL(5,2),
    str_score_learnability DECIMAL(5,2),
    str_score_technicality DECIMAL(5,2),
    str_score_communicability DECIMAL(5,2),
    str_score_total DECIMAL(5,2),

    -- Final Tracks (5 cols)
    prog_cf_final_avg DECIMAL(5,2),
    prog_cf_final_last DECIMAL(5,2),
    arr_meth_final_avg DECIMAL(5,2),
    arr_meth_final_last DECIMAL(5,2),
    final_average DECIMAL(5,2)
);
"""

# ──────────────────────────────────────────────────────────────────────
# Semester 3 DDL
# ──────────────────────────────────────────────────────────────────────
# Input metrics: VARCHAR(255) (e.g. 'Below Average', 'Good', 'Average')
# Score metrics: DECIMAL(5,2) (e.g. 0.85, 0.70, 4.50)
# ──────────────────────────────────────────────────────────────────────
DDL_SEM3 = """
CREATE TABLE IF NOT EXISTS student_track_evaluation_sem3 (
    id VARCHAR(50) PRIMARY KEY,
    sn INT,
    full_name VARCHAR(255),
    college_email_id VARCHAR(255),
    assignment_submission VARCHAR(255),
    engagement_status VARCHAR(255),

    -- String Fundamentals, String Operations & Performance and OOP Fundamentals
    string_class_practice VARCHAR(255),
    string_lab_practice VARCHAR(255),
    string_assignment VARCHAR(255),
    string_tech_input_t1 VARCHAR(255),
    string_tech_input_t2 VARCHAR(255),
    string_tech_input_t3 VARCHAR(255),
    string_tech_input_t4 VARCHAR(255),
    string_learn_input_l1 VARCHAR(255),
    string_learn_input_l2 VARCHAR(255),
    string_learn_input_l3 VARCHAR(255),
    string_learn_input_l4 VARCHAR(255),
    string_comm_input_c1 VARCHAR(255),
    string_comm_input_c2 VARCHAR(255),
    string_comm_input_c3 VARCHAR(255),
    string_comm_input_c4 VARCHAR(255),
    string_tech_score_t1 DECIMAL(5,2),
    string_tech_score_t2 DECIMAL(5,2),
    string_tech_score_t3 DECIMAL(5,2),
    string_tech_score_t4 DECIMAL(5,2),
    string_learn_score_l1 DECIMAL(5,2),
    string_learn_score_l2 DECIMAL(5,2),
    string_learn_score_l3 DECIMAL(5,2),
    string_learn_score_l4 DECIMAL(5,2),
    string_level_combined TEXT,
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

    -- Core OOP Principles
    oop_class_practice VARCHAR(255),
    oop_lab_practice VARCHAR(255),
    oop_assignment VARCHAR(255),
    oop_tech_input_t1 VARCHAR(255),
    oop_tech_input_t2 VARCHAR(255),
    oop_tech_input_t3 VARCHAR(255),
    oop_tech_input_t4 VARCHAR(255),
    oop_learn_input_l1 VARCHAR(255),
    oop_learn_input_l2 VARCHAR(255),
    oop_learn_input_l3 VARCHAR(255),
    oop_learn_input_l4 VARCHAR(255),
    oop_comm_input_c1 VARCHAR(255),
    oop_comm_input_c2 VARCHAR(255),
    oop_comm_input_c3 VARCHAR(255),
    oop_comm_input_c4 VARCHAR(255),
    oop_tech_score_t1 DECIMAL(5,2),
    oop_tech_score_t2 DECIMAL(5,2),
    oop_tech_score_t3 DECIMAL(5,2),
    oop_tech_score_t4 DECIMAL(5,2),
    oop_learn_score_l1 DECIMAL(5,2),
    oop_learn_score_l2 DECIMAL(5,2),
    oop_learn_score_l3 DECIMAL(5,2),
    oop_learn_score_l4 DECIMAL(5,2),
    oop_level_combined TEXT,
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

    -- Advanced OOP Concepts and Data Structure
    adv_oop_class_practice VARCHAR(255),
    adv_oop_lab_practice VARCHAR(255),
    adv_oop_assignment VARCHAR(255),
    adv_oop_tech_input_t1 VARCHAR(255),
    adv_oop_tech_input_t2 VARCHAR(255),
    adv_oop_tech_input_t3 VARCHAR(255),
    adv_oop_tech_input_t4 VARCHAR(255),
    adv_oop_learn_input_l1 VARCHAR(255),
    adv_oop_learn_input_l2 VARCHAR(255),
    adv_oop_learn_input_l3 VARCHAR(255),
    adv_oop_learn_input_l4 VARCHAR(255),
    adv_oop_comm_input_c1 VARCHAR(255),
    adv_oop_comm_input_c2 VARCHAR(255),
    adv_oop_comm_input_c3 VARCHAR(255),
    adv_oop_comm_input_c4 VARCHAR(255),
    adv_oop_tech_score_t1 DECIMAL(5,2),
    adv_oop_tech_score_t2 DECIMAL(5,2),
    adv_oop_tech_score_t3 DECIMAL(5,2),
    adv_oop_tech_score_t4 DECIMAL(5,2),
    adv_oop_learn_score_l1 DECIMAL(5,2),
    adv_oop_learn_score_l2 DECIMAL(5,2),
    adv_oop_learn_score_l3 DECIMAL(5,2),
    adv_oop_learn_score_l4 DECIMAL(5,2),
    adv_oop_level_combined TEXT,
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

    -- Final Tracks
    string_final VARCHAR(255),
    oop_final VARCHAR(255),
    adv_oop_final VARCHAR(255),
    final_avg_track VARCHAR(255)
);
"""

# ──────────────────────────────────────────────────────────────────────
# Semester 4 DDL
# ──────────────────────────────────────────────────────────────────────
# Input metrics: VARCHAR(255) (e.g. 'Below Average', 'Good', 'Average')
# Score metrics: DECIMAL(5,2) (e.g. 0.85, 0.70, 4.50)
# ──────────────────────────────────────────────────────────────────────
DDL_SEM4 = """
CREATE TABLE IF NOT EXISTS student_track_evaluation_sem4 (
    id VARCHAR(50) PRIMARY KEY,
    sn INT,
    full_name VARCHAR(255),
    college_email_id VARCHAR(255),
    assignment_submission VARCHAR(255),
    engagement_status VARCHAR(255),

    -- Data Structures and Algorithms
    dsa_class_practice VARCHAR(255),
    dsa_lab_practice VARCHAR(255),
    dsa_assignment VARCHAR(255),
    dsa_tech_input_t1 VARCHAR(255),
    dsa_tech_input_t2 VARCHAR(255),
    dsa_tech_input_t3 VARCHAR(255),
    dsa_tech_input_t4 VARCHAR(255),
    dsa_learn_input_l1 VARCHAR(255),
    dsa_learn_input_l2 VARCHAR(255),
    dsa_learn_input_l3 VARCHAR(255),
    dsa_learn_input_l4 VARCHAR(255),
    dsa_comm_input_c1 VARCHAR(255),
    dsa_comm_input_c2 VARCHAR(255),
    dsa_comm_input_c3 VARCHAR(255),
    dsa_comm_input_c4 VARCHAR(255),
    dsa_tech_score_t1 DECIMAL(5,2),
    dsa_tech_score_t2 DECIMAL(5,2),
    dsa_tech_score_t3 DECIMAL(5,2),
    dsa_tech_score_t4 DECIMAL(5,2),
    dsa_learn_score_l1 DECIMAL(5,2),
    dsa_learn_score_l2 DECIMAL(5,2),
    dsa_learn_score_l3 DECIMAL(5,2),
    dsa_learn_score_l4 DECIMAL(5,2),
    dsa_level_combined TEXT,
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

    -- Collections and Stream API
    collections_class_practice VARCHAR(255),
    collections_lab_practice VARCHAR(255),
    collections_assignment VARCHAR(255),
    collections_tech_input_t1 VARCHAR(255),
    collections_tech_input_t2 VARCHAR(255),
    collections_tech_input_t3 VARCHAR(255),
    collections_tech_input_t4 VARCHAR(255),
    collections_learn_input_l1 VARCHAR(255),
    collections_learn_input_l2 VARCHAR(255),
    collections_learn_input_l3 VARCHAR(255),
    collections_learn_input_l4 VARCHAR(255),
    collections_comm_input_c1 VARCHAR(255),
    collections_comm_input_c2 VARCHAR(255),
    collections_comm_input_c3 VARCHAR(255),
    collections_comm_input_c4 VARCHAR(255),
    collections_tech_score_t1 DECIMAL(5,2),
    collections_tech_score_t2 DECIMAL(5,2),
    collections_tech_score_t3 DECIMAL(5,2),
    collections_tech_score_t4 DECIMAL(5,2),
    collections_learn_score_l1 DECIMAL(5,2),
    collections_learn_score_l2 DECIMAL(5,2),
    collections_learn_score_l3 DECIMAL(5,2),
    collections_learn_score_l4 DECIMAL(5,2),
    collections_level_combined TEXT,
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

    -- Java Advanced
    java_adv_class_practice VARCHAR(255),
    java_adv_lab_practice VARCHAR(255),
    java_adv_assignment VARCHAR(255),
    java_adv_tech_input_t1 VARCHAR(255),
    java_adv_tech_input_t2 VARCHAR(255),
    java_adv_tech_input_t3 VARCHAR(255),
    java_adv_tech_input_t4 VARCHAR(255),
    java_adv_learn_input_l1 VARCHAR(255),
    java_adv_learn_input_l2 VARCHAR(255),
    java_adv_learn_input_l3 VARCHAR(255),
    java_adv_learn_input_l4 VARCHAR(255),
    java_adv_comm_input_c1 VARCHAR(255),
    java_adv_comm_input_c2 VARCHAR(255),
    java_adv_comm_input_c3 VARCHAR(255),
    java_adv_comm_input_c4 VARCHAR(255),
    java_adv_tech_score_t1 DECIMAL(5,2),
    java_adv_tech_score_t2 DECIMAL(5,2),
    java_adv_tech_score_t3 DECIMAL(5,2),
    java_adv_tech_score_t4 DECIMAL(5,2),
    java_adv_learn_score_l1 DECIMAL(5,2),
    java_adv_learn_score_l2 DECIMAL(5,2),
    java_adv_learn_score_l3 DECIMAL(5,2),
    java_adv_learn_score_l4 DECIMAL(5,2),
    java_adv_level_combined TEXT,
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

    -- Final Tracks
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
