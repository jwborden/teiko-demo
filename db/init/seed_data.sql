-- TODO

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
FROM './cell-count.csv'
DELIMITER ','
CSV HEADER;
