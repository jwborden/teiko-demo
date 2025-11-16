-- Our first table handles seeding, but is not clean
CREATE TABLE IF NOT EXISTS imported (
    uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project VARCHAR(100),
    subject VARCHAR(100),
    condition VARCHAR(100),
    age INT,
    sex VARCHAR(100),
    treatment VARCHAR(100),
    response VARCHAR(100),
    sample VARCHAR(100),
    sample_type VARCHAR(100),
    time_from_treatment_start INT,
    b_cell INT,
    cd8_t_cell INT,
    cd4_t_cell INT,
    nk_cell INT,
    monocyte INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- These tables are more clean
CREATE TABLE IF NOT EXISTS project (
    id VARCHAR(100) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS subject (
    id VARCHAR(100) PRIMARY KEY,
    age INT CHECK (age>=0),
    sex VARCHAR(100) CHECK (sex IN ('M', 'F', 'Other'))
);

CREATE TABLE IF NOT EXISTS sample (
    id VARCHAR(100) PRIMARY KEY,
    sample_type VARCHAR(100) CHECK (sample_type IN ('PBMC', 'WB')),
    time_from_treatment_start INT,
    b_cell INT,
    cd8_t_cell INT,
    cd4_t_cell INT,
    nk_cell INT,
    monocyte INT,
    subject_id VARCHAR(100) NOT NULL,

    FOREIGN KEY (subject_id)
        REFERENCES subject(id)
        ON DELETE RESTRICT
);

CREATE TABLE IF NOT EXISTS med_condition (
    subject_id VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,

    PRIMARY KEY (subject_id, name),
    
    FOREIGN KEY (subject_id)
        REFERENCES subject(id)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS treatment (
    subject_id VARCHAR(100) NOT NULL,
    med_condition_name VARCHAR(100) NOT NULL,
    name VARCHAR(100) NOT NULL,
    response BOOLEAN,

    PRIMARY KEY (subject_id, med_condition_name, name),
    
    FOREIGN KEY (subject_id)
        REFERENCES subject(id)
        ON DELETE CASCADE,

    FOREIGN KEY (subject_id, med_condition_name)
        REFERENCES med_condition(subject_id, name)
        ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS project_subjects (
    project_id VARCHAR(100) NOT NULL,
    subject_id VARCHAR(100) NOT NULL,

    PRIMARY KEY (project_id, subject_id),
    
    FOREIGN KEY (project_id)
        REFERENCES project(id)
        ON DELETE CASCADE,
    
    FOREIGN KEY (subject_id)
        REFERENCES subject(id)
        ON DELETE CASCADE
);

-- Handle ownership
ALTER TABLE imported OWNER TO demo_user;
ALTER TABLE project OWNER TO demo_user;
ALTER TABLE subject OWNER TO demo_user;
ALTER TABLE sample OWNER TO demo_user;
ALTER TABLE med_condition OWNER TO demo_user;
ALTER TABLE treatment OWNER TO demo_user;
ALTER TABLE project_subjects OWNER TO demo_user;
