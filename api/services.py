import pandas as pd  # type: ignore

from api.crud import get_project_by_project_id, get_samples_by_sample_id


def get_projects(project_ids: list[str] | None = None) -> list[str]:
    projects = get_project_by_project_id(project_ids if project_ids else None)
    out = [proj._mapping["Project"].project_id for proj in projects]
    return out


def basic_html() -> str:
    out = """
    <html>
      <head>
        <title>Teiko Demo</title>
      </head>
      <body>
        <h1>Teiko Demo Service</h1>
        <p>This is a basic HTML response from the Teiko Demo Service.</p>
      </body>
    </html>
    """
    return out


def data_overview() -> str:
    samples = get_samples_by_sample_id(None)
    data = [
        {
            "subject_id": sample._mapping["Sample"].subject_id,
            "sample_id": sample._mapping["Sample"].sample_id,
            "sample_type": sample._mapping["Sample"].sample_type,
            # "time_from_treatment_start": sample._mapping["Sample"].time_from_treatment_start,
            "b_cell": sample._mapping["Sample"].b_cell,
            "cd8_t_cell": sample._mapping["Sample"].cd8_t_cell,
            "cd4_t_cell": sample._mapping["Sample"].cd4_t_cell,
            "nk_cell": sample._mapping["Sample"].nk_cell,
            "monocyte": sample._mapping["Sample"].monocyte,
        }
        for sample in samples
    ]
    df = pd.DataFrame(data)

    cell_types = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]
    df["total_cells"] = df[cell_types].sum(axis=1)
    for ctype in cell_types:
        df[f"{ctype} (%)"] = ((df[ctype] / df["total_cells"]) * 100).round(2)

    df_html = df.to_html()
    out = f"""
    <!doctype html>
    <html>

      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Teiko Demo - Data Overview</title>
      </head>
      <body>
          <header>
            <h1>Teiko Demo - Data Overview</h1>
            <style>
              html, body {{
                  width: 100%;
                  margin: 0;
                  padding: 0;
                  background: #222;          /* dark background */
                  color: #eee;               /* light text */
                  font-size: 12px;          /* base font size */
              }}

              header {{
                text-align: center;
                font-family: Arial, Helvetica, sans-serif;
                font-size: 1.5rem;
                margin: 20px 0;
                color: #eee;
                border-bottom: 2px solid #e0e0e0;
                padding-bottom: 10px;
              }}

              table {{
                  margin: 2rem auto;          /* center the table */
                  border-collapse: collapse;  /* cleaner borders */
                  background: #222;           /* dark background */
                  color: #fff;                /* white text */
                  font-family: sans-serif;
                  min-width: 300px;
              }}

              th, td {{
                  padding: 0.75rem 1rem;
                  border: 1px solid #444;     /* subtle borders */
                  text-align: left;
              }}

              th {{
                  background: #333;           /* slightly lighter header */
                  font-weight: 600;
              }}

              tr:nth-child(even) td {{
                  background: #2a2a2a;        /* alternating dark rows */
              }}

              tr:hover td {{
                  background: #383838;        /* highlight on hover */
              }}
            </style>

          </header>
          <main>
            <section>
              {df_html}
            </section>
          </main>
      </body>
    </html>
    """

    return out


def statistical_analysis():
    return {"message": "This is the statistical analysis service."}


def data_subset_analysis():
    return {"message": "This is the data subset analysis service."}
