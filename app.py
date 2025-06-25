import os
from flask import Flask, render_template, request
from utils.web_scraper import download_pdfs_from_drive_link
from utils.pdf_extractor import extract_contact_info
from utils.excel_writer import write_to_excel
from utils.drive_uploader import upload_to_drive

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def upload_drive_link():
    if request.method == "POST":
        drive_link = request.form.get("drive_link")
        try:
            pdf_paths = download_pdfs_from_drive_link(drive_link)
            results = []
            for path in pdf_paths:
                info = extract_contact_info(path)
                info["permit_id"] = "manual_input"
                results.append(info)

            xlsx_path = write_to_excel(results)
            drive_url = upload_to_drive(xlsx_path)
            return render_template("result.html", results=results, drive_link=drive_url)
        except Exception as e:
            return render_template("index.html", error=str(e))
    return render_template("index.html")

if __name__ == "__main__":
    os.environ["PATH"] += os.pathsep + r"C:\\Release-23.08.0-0\\poppler-23.08.0\\Library\\bin"
    app.run(debug=True)