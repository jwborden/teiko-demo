-- TODO: finish

-- This isn't efficient, but it reflects the provided csv
-- I'll make more tables later (TODO)
CREATE TABLE IF NOT EXISTS imported (
    uid UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project VARCHAR(255),
    subject VARCHAR(255),
    condition VARCHAR(255),
    age INT,
    sex VARCHAR(255),
    treatment VARCHAR(255),
    response VARCHAR(255),
    sample VARCHAR(255),
    sample_type VARCHAR(255),
    time_from_treatment_start INT,
    b_cell INT,
    cd8_t_cell INT,
    cd4_t_cell INT,
    nk_cell INT,
    monocyte INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
