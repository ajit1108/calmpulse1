-- MySQL Migration Script --
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS stress_history;
DROP TABLE IF EXISTS user;
SET FOREIGN_KEY_CHECKS = 1;

CREATE TABLE user (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE stress_history (
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Seeding 'user' table --
INSERT INTO user (id, first_name, last_name, contact, email, password_hash, age, gender, role, is_new_user) VALUES (1, 'Anagha', 'Shelake', '7248984546', 'anaghashelake1606@gmail.com', '$2b$12$OPB96lKKgDNq3p2Q7tKfNOLgxAPYnryVdKvhkAdjL5VM/QISz/tbe', NULL, NULL, NULL, 1);
INSERT INTO user (id, first_name, last_name, contact, email, password_hash, age, gender, role, is_new_user) VALUES (2, 'Ajit', 'Birajdar', '8308129957', 'ajitbirajdar1108@gmail.com', '$2b$12$uEADWWux1gFifqiNt.iUhubM9bb0cjak2ctCl1QOsjE8ebNrwZ3em', NULL, NULL, NULL, 1);

