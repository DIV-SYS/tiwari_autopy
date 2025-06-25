import os
import pandas as pd

EXCEL_PATH = "permit_automation/output/final_output.xlsx"

def write_to_excel(all_data):
    # all_data = list of dicts
    rows = []
    for data in all_data:
        row = {
            "Permit ID": data["permit_id"],
            "Company Name": data["company"],
            "First Contact Name": data.get("contacts", [("","")])[0][0] if len(data.get("contacts", [])) > 0 else "",
            "First Contact Email": data.get("contacts", [("","")])[0][1] if len(data.get("contacts", [])) > 0 else "",
            "Second Contact Name": data.get("contacts", [("","")]*2)[1][0] if len(data.get("contacts", [])) > 1 else "",
            "Second Contact Email": data.get("contacts", [("","")]*2)[1][1] if len(data.get("contacts", [])) > 1 else "",
            "Third Contact Name": data.get("contacts", [("","")]*3)[2][0] if len(data.get("contacts", [])) > 2 else "",
            "Third Contact Email": data.get("contacts", [("","")]*3)[2][1] if len(data.get("contacts", [])) > 2 else "",
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    os.makedirs(os.path.dirname(EXCEL_PATH), exist_ok=True)
    df.to_excel(EXCEL_PATH, index=False)
    return EXCEL_PATH
