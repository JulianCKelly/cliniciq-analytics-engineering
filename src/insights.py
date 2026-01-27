import pandas as pd
import io


def process_emr_csv(file_bytes: bytes) -> dict:
    """
    Processes raw EMR CSV data and returns clinical/business insights.
    Expects a CSV with the following columns:
    ['PatientID', 'VisitDate', 'CPTCode', 'Revenue', 'NoShow']
    """

    try:
        df = pd.read_csv(io.BytesIO(file_bytes))
    except Exception as e:
        return {"error": f"Could not read CSV: {str(e)}"}

    required_columns = {"PatientID", "VisitDate", "CPTCode", "Revenue", "NoShow"}
    if not required_columns.issubset(df.columns):
        return {"error": f"Missing required columns: {required_columns - set(df.columns)}"}

    try:
        # Basic metrics
        total_revenue = df['Revenue'].sum()
        no_show_rate = round(df['NoShow'].mean() * 100, 2)
        cpt_distribution = df['CPTCode'].value_counts().to_dict()

        # Additional insights
        avg_revenue_per_visit = round(df['Revenue'].mean(), 2)
        visit_volume = df['VisitDate'].nunique()
        most_common_cpt = df['CPTCode'].mode()[0]

        return {
            "Total Revenue": total_revenue,
            "No-Show Rate (%)": no_show_rate,
            "Average Revenue per Visit": avg_revenue_per_visit,
            "Unique Visit Dates": visit_volume,
            "Most Common CPT Code": most_common_cpt,
            "CPT Code Distribution": cpt_distribution
        }

    except Exception as e:
        return {"error": f"Failed to generate insights: {str(e)}"}