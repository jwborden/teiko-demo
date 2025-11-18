import pandas as pd  # type: ignore
from scipy import stats  # type: ignore
import plotly.graph_objects as go  # type: ignore

from api.crud import (
    get_project_by_project_id,
    get_samples_by_sample_id,
    get_samples_by_sample_condition_treatment_timeline,
    get_for_subset_analysis,
)


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
    df = df.sort_values(by=["sample_id"])

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
      </head>
      <body>
          <header>
            <h1>Teiko Demo - Data Overview</h1>
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


def statistical_analysis() -> str:
    # Get samples of type PBMC with treatment type miraclib
    samples = get_samples_by_sample_condition_treatment_timeline(
        sample_types=["PBMC"],
        conditions=["melanoma"],
        treatment_types=["miraclib"],
        time_points=None,
    )
    data = [
        {
            "subject_id": sample._mapping["Sample"].subject_id,
            "sample_id": sample._mapping["Sample"].sample_id,
            "condition": sample._mapping["Treatment"].subject_condition_name,
            "treatment": sample._mapping["Treatment"].treatment_name,
            "response": sample._mapping["Treatment"].response,
            "sample_type": sample._mapping["Sample"].sample_type,
            "time": sample._mapping["Sample"].time_from_treatment_start,
            "b_cell": sample._mapping["Sample"].b_cell,
            "cd8_t_cell": sample._mapping["Sample"].cd8_t_cell,
            "cd4_t_cell": sample._mapping["Sample"].cd4_t_cell,
            "nk_cell": sample._mapping["Sample"].nk_cell,
            "monocyte": sample._mapping["Sample"].monocyte,
        }
        for sample in samples
    ]
    df = pd.DataFrame(data)
    df = df.sort_values(by=["sample_id"])

    # Calculate cell type percentages by response status
    cell_types = ["b_cell", "cd8_t_cell", "cd4_t_cell", "nk_cell", "monocyte"]
    df["total_cells"] = df[cell_types].sum(axis=1)
    for ctype in cell_types:
        df[f"{ctype} (%)"] = (df[ctype] / df["total_cells"]) * 100

    responders_df = df[df["response"]]
    non_responders_df = df[~df["response"]]

    # Perform t-tests
    stats_dict: dict = {
        "Cell Type": [],
        "Responders Mean (%)": [],
        "Non-Responders Mean (%)": [],
        "p-value": [],
    }
    for ctype in cell_types:
        _, p, *_ = stats.ttest_ind(
            responders_df[f"{ctype} (%)"],
            non_responders_df[f"{ctype} (%)"],
            equal_var=False,
        )
        stats_dict["Cell Type"].append(ctype)
        stats_dict["Responders Mean (%)"].append(
            round(responders_df[f"{ctype} (%)"].mean(), 2)
        )
        stats_dict["Non-Responders Mean (%)"].append(
            round(non_responders_df[f"{ctype} (%)"].mean(), 2)
        )
        stats_dict["p-value"].append(round(float(p), 4))  # type: ignore
    stats_df = pd.DataFrame(stats_dict)

    # Create box plots
    fig = go.Figure()
    for ctype in cell_types:
        for grp, grp_df in [
            ("Responders", responders_df),
            ("Non-Responders", non_responders_df),
        ]:
            fig.add_trace(
                go.Box(y=grp_df[f"{ctype} (%)"], name=f"{ctype} - {grp}", boxmean="sd")
            )
    fig.update_layout(
        yaxis_title="Percentage (%)",
        dragmode="pan",
        plot_bgcolor="rgb(50, 50, 50)",
        paper_bgcolor="rgb(50, 50, 50)",
        xaxis=dict(color="white", gridcolor="gray"),
        yaxis=dict(color="white", gridcolor="gray"),
        font=dict(color="white"),
    )
    config_options = {
        "displaylogo": False,
    }

    fig_html = fig.to_html(full_html=False, config=config_options)  # give a div only
    responders_df_html = responders_df.to_html()
    non_responders_df_html = non_responders_df.to_html()
    stats_df_html = stats_df.to_html()

    out = f"""
    <!doctype html>
    <html>

      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Teiko Demo - Statistical Analysis (PBMC/Melanoma/Miraclib)</title>
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

          h2 {{
            text-align: center;
            font-family: Arial, Helvetica, sans-serif;
            font-size: 18px;            /* Smaller font size for h2 */
            margin: 15px 0;
            color: #eee;
            border-bottom: 1px solid #e0e0e0; /* Subtle underline */
            padding-bottom: 5px;
          }}

          p {{
            max-width: 500px;
            margin: 2rem auto;
            font-size: 14px;
            line-height: 1.5;
          }}

          nav {{
            text-align: center;
            margin: 20px 0;
            padding-top: 10px;
            padding-bottom: 20px;
          }}

          nav ul {{
            list-style: none;           /* Remove bullet points */
            padding: 0;
            margin: 0;
            display: inline-flex;       /* Horizontal layout */
            gap: 15px;                  /* Space between links */
          }}

          nav ul li {{
            display: inline;            /* Ensure list items are inline */
          }}

          nav ul li a {{
            color: #1a73e8;             /* Blue links */
            text-decoration: none;
            font-size: 1.5rem;
            padding: 10px 15px;
            border: 1px solid #1a73e8;  /* Add a border for buttons */
            border-radius: 5px;         /* Rounded corners */
            transition: all 0.3s ease;  /* Smooth hover effect */
          }}

          nav ul li a:hover {{
            background-color: #1a73e8;  /* Blue background on hover */
            color: #fff;                /* White text on hover */
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

          .plotly-graph-div.js-plotly-plot {{
            margin: 2rem auto;
            min-height: 600px;
            max-width: 1400px;

          }}

        </style>
      </head>
      <body>
          <header>
            <h1>Teiko Demo - Statistical Analysis (PBMC/Melanoma/Miraclib)</h1>
          </header>
          <nav>
            <ul>
              <li><a href="#cell-type-percentages">Cell Type Percentages by Response Status</a></li>
              <li><a href="#t-test-comparison">T-test Comparison</a></li>
              <li><a href="#responders-data">Responders Data</a></li>
              <li><a href="#non-responders-data">Non-Responders Data</a></li>
            </ul>
          </nav>
          <main>
            <section id="cell-type-percentages"">
              <h2>Cell Type Percentages by Response Status (PBMC/Melanoma/Miraclib)</h2>
              {fig_html}
            </section>
            <section id="t-test-comparison">
              <h2>T-test Comparison (PBMC/Melanoma/Miraclib)</h2>
              {stats_df_html}
              <p>
                CD4 T-cells show a statistically significant difference in relative
                frequencies between responders and non-responders (p &lt; 0.05),
                however, the means are quite close (Responders: {stats_df.loc[stats_df["Cell Type"] == "cd4_t_cell", "Responders Mean (%)"].values[0]}%,
                Non-Responders: {stats_df.loc[stats_df["Cell Type"] == "cd4_t_cell", "Non-Responders Mean (%)"].values[0]}%), suggesting
                that the effect size may not be clinically significant.
              </p>
            </section>
            <section id="responders-data">
              <h2>Responders Data (PBMC/Melanoma/Miraclib)</h2>
              {responders_df_html}
            </section>
            <section id="non-responders-data">
              <h2>Non-Responders Data (PBMC/Melanoma/Miraclib)</h2>
              {non_responders_df_html}
            </section>
          </main>
      </body>
    </html>
    """

    return out


def data_subset_analysis() -> str:
    # Get samples of type PBMC with treatment type miraclib
    samples = get_for_subset_analysis(
        sample_types=["PBMC"],
        conditions=["melanoma"],
        treatment_types=["miraclib"],
        time_points=[0],
    )
    data = [
        {
            "project_id": sample._mapping["ProjectSubject"].project_id,
            "subject_id": sample._mapping["Sample"].subject_id,
            "sample_id": sample._mapping["Sample"].sample_id,
            "condition": sample._mapping["Treatment"].subject_condition_name,
            "age": sample._mapping["Subject"].age,
            "F/M": sample._mapping["Subject"].sex,
            "treatment": sample._mapping["Treatment"].treatment_name,
            "response": sample._mapping["Treatment"].response,
            "sample_type": sample._mapping["Sample"].sample_type,
            "time": sample._mapping["Sample"].time_from_treatment_start,
            "b_cell": sample._mapping["Sample"].b_cell,
            "cd8_t_cell": sample._mapping["Sample"].cd8_t_cell,
            "cd4_t_cell": sample._mapping["Sample"].cd4_t_cell,
            "nk_cell": sample._mapping["Sample"].nk_cell,
            "monocyte": sample._mapping["Sample"].monocyte,
        }
        for sample in samples
    ]
    df = pd.DataFrame(data)
    df = df.sort_values(by=["sample_id"])

    samples_per_proj_pivot = df.pivot_table(
        values=["sample_id"],
        index=["project_id"],
        aggfunc={"sample_id": pd.Series.nunique},  # type: ignore
    )
    subjects_responders_pivot = df.pivot_table(
        values=["subject_id"],
        index=["response"],
        aggfunc={"subject_id": pd.Series.nunique},  # type: ignore
    )
    subjects_sex_pivot = df.pivot_table(
        values=["subject_id"],
        index=["F/M"],
        aggfunc={"subject_id": pd.Series.nunique},  # type: ignore
    )
    big_pivot = df.pivot_table(
        values=["sample_id", "subject_id"],
        index=["project_id", "F/M", "response"],
        aggfunc={
            "sample_id": pd.Series.nunique,  # type: ignore
            "subject_id": pd.Series.nunique,  # type: ignore
        },
    )

    df_html = df.to_html()
    samples_per_proj_html = samples_per_proj_pivot.to_html()
    subjects_responders_html = subjects_responders_pivot.to_html()
    subjects_sex_html = subjects_sex_pivot.to_html()
    big_pivot_html = big_pivot.to_html()

    out = f"""
    <!doctype html>
    <html>

      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Teiko Demo - Data Subset Analysis (PBMC/Melanoma/Miraclib/Baseline)</title>
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

          h2 {{
            text-align: center;
            font-family: Arial, Helvetica, sans-serif;
            font-size: 18px;            /* Smaller font size for h2 */
            margin: 15px 0;
            color: #eee;
            border-bottom: 1px solid #e0e0e0; /* Subtle underline */
            padding-bottom: 5px;
          }}

          p {{
            max-width: 500px;
            margin: 2rem auto;
            font-size: 14px;
            line-height: 1.5;
          }}

          nav {{
            text-align: center;
            margin: 20px 0;
            padding-top: 10px;
            padding-bottom: 20px;
          }}

          nav ul {{
            list-style: none;           /* Remove bullet points */
            padding: 0;
            margin: 0;
            display: inline-flex;       /* Horizontal layout */
            gap: 15px;                  /* Space between links */
          }}

          nav ul li {{
            display: inline;            /* Ensure list items are inline */
          }}

          nav ul li a {{
            color: #1a73e8;             /* Blue links */
            text-decoration: none;
            font-size: 1.5rem;
            padding: 10px 15px;
            border: 1px solid #1a73e8;  /* Add a border for buttons */
            border-radius: 5px;         /* Rounded corners */
            transition: all 0.3s ease;  /* Smooth hover effect */
          }}

          nav ul li a:hover {{
            background-color: #1a73e8;  /* Blue background on hover */
            color: #fff;                /* White text on hover */
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

          .plotly-graph-div.js-plotly-plot {{
            margin: 2rem auto;
            min-height: 600px;
            max-width: 1400px;

          }}

        </style>
      </head>
      <body>
          <header>
            <h1>Teiko Demo - Data Subset Analysis (PBMC/Melanoma/Miraclib/Baseline)</h1>
          </header>
          <nav>
            <ul>
              <li><a href="#samples-per-project">Samples Per Project</a></li>
              <li><a href="#responders-vs-non-responders">Responders (True) vs. Non-Responders (False)</a></li>
              <li><a href="#patient-sex-distribution">Patient Sex Distribution</a></li>
              <li><a href="#subset-analysis-summary">Subset Analysis Summary</a></li>
              <li><a href="#all-patient-samples">All Patient Samples</a></li>
            </ul>
          </nav>
          <main>
            <section id="samples-per-project">
              <h2>Samples Per Project (PBMC/Melanoma/Miraclib/Baseline)</h2>
              {samples_per_proj_html}
            </section>
            <section id="responders-vs-non-responders">
              <h2>Responders (True) vs. Non-Responders (False) (PBMC/Melanoma/Miraclib/Baseline)</h2>
              {subjects_responders_html}
            </section>
            <section id="patient-sex-distribution">
              <h2>Patient Sex Distribution (PBMC/Melanoma/Miraclib/Baseline)</h2>
              {subjects_sex_html}
            </section>
            <section id="subset-analysis-summary">
              <h2>Subset Analysis Summary (PBMC/Melanoma/Miraclib/Baseline)</h2>
              {big_pivot_html}
            </section>
            <section id="all-patient-samples">
              <h2>All Patient Samples (PBMC/Melanoma/Miraclib/Baseline)</h2>
              {df_html}
            </section>
          </main>
      </body>
    </html>
    """

    return out
