from utils.google_sheet import get_permit_ids, update_sheet_link
from utils.web_scraper import download_pdfs
from utils.pdf_extractor import extract_contact_info, save_extracted_data_as_doc
from utils.drive_uploader import upload_to_drive

def main():
    permit_rows = get_permit_ids()
    for permit_id, row in permit_rows:
        try:
            pdfs = download_pdfs(permit_id)
            for i, pdf in enumerate(pdfs):
                info = extract_contact_info(pdf)
                doc_path = save_extracted_data_as_doc(f"{permit_id}_{i}", info)
                link = upload_to_drive(doc_path)
                update_sheet_link(row, link)
        except Exception as e:
            print(f"Error processing {permit_id}: {e}")

if __name__ == "__main__":
    main()
