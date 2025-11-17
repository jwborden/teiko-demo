-- Import from .csv
COPY imported (
    project,
    subject,
    condition,
    age,
    sex,
    treatment,
    response,
    sample,
    sample_type,
    time_from_treatment_start,
    b_cell,
    cd8_t_cell,
    cd4_t_cell,
    nk_cell,
    monocyte
)
FROM '../init/cell-count.csv'
DELIMITER ','
CSV HEADER;

-- Populate project
INSERT INTO project (project_id)
SELECT DISTINCT project
FROM imported
WHERE project IS NOT NULL
ON CONFLICT (project_id) DO NOTHING;

-- Populate subject
INSERT INTO subject (subject_id, age, sex)
SELECT DISTINCT subject, age, sex
FROM imported
WHERE subject IS NOT NULL
ON CONFLICT (subject_id) DO NOTHING;

-- Populate sample
INSERT INTO sample (
    sample_id,
    sample_type,
    time_from_treatment_start,
    b_cell,
    cd8_t_cell,
    cd4_t_cell,
    nk_cell,
    monocyte,
    subject_id
)
SELECT DISTINCT
    sample,
    sample_type,
    time_from_treatment_start,
    b_cell,
    cd8_t_cell,
    cd4_t_cell,
    nk_cell,
    monocyte,
    subject
FROM imported
WHERE sample IS NOT NULL
AND subject IS NOT NULL
ON CONFLICT (sample_id) DO NOTHING;

-- Populate subject_condition
INSERT INTO subject_condition (subject_id, condition_name)
SELECT DISTINCT subject, condition
FROM imported
WHERE subject IS NOT NULL
AND condition IS NOT NULL
ON CONFLICT (subject_id, condition_name) DO NOTHING;

-- Populate treatment
INSERT INTO treatment (
    subject_id,
    subject_condition_name,
    treatment_name,
    response
)
SELECT DISTINCT
    subject,
    condition,
    treatment,
    CASE LOWER(response)
        WHEN 'yes' THEN TRUE
        WHEN 'no' THEN FALSE
        ELSE NULL
    END
FROM imported
WHERE subject IS NOT NULL
AND condition IS NOT NULL
AND treatment IS NOT NULL
ON CONFLICT (
    subject_id,
    subject_condition_name,
    treatment_name
) DO NOTHING;

-- Populate project_subjects
INSERT INTO project_subjects (project_id, subject_id)
SELECT DISTINCT project, subject
FROM imported
WHERE project IS NOT NULL
AND subject IS NOT NULL
ON CONFLICT (project_id, subject_id) DO NOTHING;
