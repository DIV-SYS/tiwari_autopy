from utils.google_sheet import get_permit_ids, update_sheet_link
from utils.web_scraper import download_pdfs
from utils.pdf_extractor import extract_contact_info
from utils.excel_writer import write_to_excel
from utils.drive_uploader import upload_to_drive

def main():
    permit_rows = get_permit_ids()
    all_data = []

    for permit_id, row in permit_rows:
        try:
            pdfs = download_pdfs(permit_id)
            for i, pdf in enumerate(pdfs):
                info = extract_contact_info(pdf)
                info["permit_id"] = f"{permit_id}_{i}"
                all_data.append(info)
        except Exception as e:
            print(f"Error processing {permit_id}: {e}")

    
    xlsx_path = write_to_excel(all_data)

    
    drive_link = upload_to_drive(xlsx_path)
    update_sheet_link(2, drive_link)  

if __name__ == "__main__":
    main()
