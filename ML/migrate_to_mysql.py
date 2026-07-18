import sqlite3
import os

def migrate():
    # Paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sqlite_db_path = os.path.join(base_dir, 'instance', 'local.db')
    output_sql_path = os.path.join(base_dir, 'migration.sql')

    if not os.path.exists(sqlite_db_path):
        print(f"SQLite database not found at {sqlite_db_path}. Nothing to migrate.")
        return

    print(f"Reading SQLite database: {sqlite_db_path}")
    sqlite_conn = sqlite3.connect(sqlite_db_path)
    sqlite_cursor = sqlite_conn.cursor()

    sql_statements = []

    # Write DDL for MySQL
    sql_statements.append("-- MySQL Migration Script --\n")
    sql_statements.append("SET FOREIGN_KEY_CHECKS = 0;\n")
    sql_statements.append("DROP TABLE IF EXISTS stress_history;\n")
    sql_statements.append("DROP TABLE IF EXISTS user;\n")
    sql_statements.append("SET FOREIGN_KEY_CHECKS = 1;\n\n")

    sql_statements.append("""CREATE TABLE user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    contact VARCHAR(20),
    email VARCHAR(120) UNIQUE NOT NULL,
    password_hash VARCHAR(128) NOT NULL,
    age INT,
    gender VARCHAR(20),
    role VARCHAR(20),
    is_new_user BOOLEAN DEFAULT TRUE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n\n""")

    sql_statements.append("""CREATE TABLE stress_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    stress_score FLOAT NOT NULL,
    timestamp DATETIME NOT NULL,
    job_role VARCHAR(100),
    working_hours INT,
    virtual_meetings INT,
    work_life_balance INT,
    access_to_mental_health VARCHAR(10),
    satisfaction_with_remote_work VARCHAR(20),
    company_support INT,
    physical_activity VARCHAR(20),
    sleep_quality VARCHAR(20),
    anxiety_level INT,
    depression INT,
    academic_performance INT,
    study_load INT,
    teacher_student_relationship INT,
    future_career_concerns INT,
    social_support INT,
    peer_pressure INT,
    extracurricular_load INT,
    FOREIGN KEY (user_id) REFERENCES user(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n\n""")

    # Migrate User Table Rows
    print("Reading 'user' table...")
    sqlite_cursor.execute("SELECT * FROM user;")
    users = sqlite_cursor.fetchall()
    
    # Get columns
    sqlite_cursor.execute("PRAGMA table_info(user);")
    user_cols = [col[1] for col in sqlite_cursor.fetchall()]

    if users:
        print(f"Found {len(users)} users. Writing insert statements...")
        sql_statements.append("-- Seeding 'user' table --\n")
        for u in users:
            row_dict = dict(zip(user_cols, u))
            
            # Escape strings for SQL
            first_name = f"'{row_dict['first_name']}'" if row_dict['first_name'] is not None else "NULL"
            last_name = f"'{row_dict['last_name']}'" if row_dict['last_name'] is not None else "NULL"
            contact = f"'{row_dict['contact']}'" if row_dict['contact'] is not None else "NULL"
            email = f"'{row_dict['email']}'"
            password_hash = f"'{row_dict['password_hash']}'"
            age = str(row_dict['age']) if row_dict['age'] is not None else "NULL"
            gender = f"'{row_dict['gender']}'" if row_dict['gender'] is not None else "NULL"
            role = f"'{row_dict['role']}'" if row_dict['role'] is not None else "NULL"
            is_new_user = "1" if row_dict['is_new_user'] else "0"

            insert_statement = f"INSERT INTO user (id, first_name, last_name, contact, email, password_hash, age, gender, role, is_new_user) VALUES ({row_dict['id']}, {first_name}, {last_name}, {contact}, {email}, {password_hash}, {age}, {gender}, {role}, {is_new_user});\n"
            sql_statements.append(insert_statement)
        sql_statements.append("\n")

    # Migrate Stress History Table Rows
    print("Reading 'stress_history' table...")
    sqlite_cursor.execute("SELECT * FROM stress_history;")
    histories = sqlite_cursor.fetchall()
    
    # Get columns
    sqlite_cursor.execute("PRAGMA table_info(stress_history);")
    history_cols = [col[1] for col in sqlite_cursor.fetchall()]

    if histories:
        print(f"Found {len(histories)} history records. Writing insert statements...")
        sql_statements.append("-- Seeding 'stress_history' table --\n")
        for h in histories:
            row_dict = dict(zip(history_cols, h))
            
            user_id = str(row_dict['user_id'])
            stress_score = str(row_dict['stress_score'])
            timestamp = f"'{row_dict['timestamp']}'"
            job_role = f"'{row_dict['job_role']}'" if row_dict['job_role'] is not None else "NULL"
            working_hours = str(row_dict['working_hours']) if row_dict['working_hours'] is not None else "NULL"
            virtual_meetings = str(row_dict['virtual_meetings']) if row_dict['virtual_meetings'] is not None else "NULL"
            work_life_balance = str(row_dict['work_life_balance']) if row_dict['work_life_balance'] is not None else "NULL"
            access_to_mental_health = f"'{row_dict['access_to_mental_health']}'" if row_dict['access_to_mental_health'] is not None else "NULL"
            satisfaction_with_remote_work = f"'{row_dict['satisfaction_with_remote_work']}'" if row_dict['satisfaction_with_remote_work'] is not None else "NULL"
            company_support = str(row_dict['company_support']) if row_dict['company_support'] is not None else "NULL"
            physical_activity = f"'{row_dict['physical_activity']}'" if row_dict['physical_activity'] is not None else "NULL"
            sleep_quality = f"'{row_dict['sleep_quality']}'" if row_dict['sleep_quality'] is not None else "NULL"
            anxiety_level = str(row_dict['anxiety_level']) if row_dict['anxiety_level'] is not None else "NULL"
            depression = str(row_dict['depression']) if row_dict['depression'] is not None else "NULL"
            academic_performance = str(row_dict['academic_performance']) if row_dict['academic_performance'] is not None else "NULL"
            study_load = str(row_dict['study_load']) if row_dict['study_load'] is not None else "NULL"
            teacher_student_relationship = str(row_dict['teacher_student_relationship']) if row_dict['teacher_student_relationship'] is not None else "NULL"
            future_career_concerns = str(row_dict['future_career_concerns']) if row_dict['future_career_concerns'] is not None else "NULL"
            social_support = str(row_dict['social_support']) if row_dict['social_support'] is not None else "NULL"
            peer_pressure = str(row_dict['peer_pressure']) if row_dict['peer_pressure'] is not None else "NULL"
            extracurricular_load = str(row_dict['extracurricular_load']) if row_dict['extracurricular_load'] is not None else "NULL"

            insert_statement = f"INSERT INTO stress_history (id, user_id, stress_score, timestamp, job_role, working_hours, virtual_meetings, work_life_balance, access_to_mental_health, satisfaction_with_remote_work, company_support, physical_activity, sleep_quality, anxiety_level, depression, academic_performance, study_load, teacher_student_relationship, future_career_concerns, social_support, peer_pressure, extracurricular_load) VALUES ({row_dict['id']}, {user_id}, {stress_score}, {timestamp}, {job_role}, {working_hours}, {virtual_meetings}, {work_life_balance}, {access_to_mental_health}, {satisfaction_with_remote_work}, {company_support}, {physical_activity}, {sleep_quality}, {anxiety_level}, {depression}, {academic_performance}, {study_load}, {teacher_student_relationship}, {future_career_concerns}, {social_support}, {peer_pressure}, {extracurricular_load});\n"
            sql_statements.append(insert_statement)
        sql_statements.append("\n")

    sqlite_conn.close()

    # Write to file
    with open(output_sql_path, 'w', encoding='utf-8') as f:
        f.writelines(sql_statements)

    print(f"Successfully generated MySQL migration script: {output_sql_path}")


if __name__ == '__main__':
    migrate()
