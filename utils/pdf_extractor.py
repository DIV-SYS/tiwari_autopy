import re
import platform
import pytesseract
from pdf2image import convert_from_path

# ✅ Set tesseract path for Windows (skip for Linux/Render)
if platform.system() == "Windows":
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_contact_info(pdf_path):
    # Step 1: Convert PDF pages to images
    images = convert_from_path(pdf_path)

    # Step 2: Extract text from all images using OCR
    text = "\n".join(pytesseract.image_to_string(img) for img in images)

    # Step 3: Define helper functions to extract specific info
    def extract_field_after_label(label, full_text):
        pattern = rf"{label}.*?\n(.*?)\n"
        match = re.search(pattern, full_text, re.IGNORECASE | re.DOTALL)
        return match.group(1).strip().title() if match else None

    def extract_email_near_label(label, full_text):
        label_index = full_text.lower().find(label.lower())
        if label_index == -1:
            return None
        snippet = full_text[label_index : label_index + 300]  # Look ahead for email
        match = re.search(r"([\w\.-]+@[\w\.-]+)", snippet)
        return match.group(1).strip() if match else None

    # Step 4: Try extracting official and local contacts
    official_name = extract_field_after_label("Official Contact Person Name", text)
    official_email = extract_email_near_label("Official Contact Person Name", text)

    local_name = extract_field_after_label("Local Contact Person Name", text)
    local_email = extract_email_near_label("Local Contact Person Name", text)

    contacts = []
    if official_name and official_email:
        contacts.append((official_name, official_email))
    if local_name and local_email:
        contacts.append((local_name, local_email))

    # Step 5: Fallback — up to 3 name+email matches from the whole text
    fallback_contacts = re.findall(
        r'([A-Z][a-z]+(?:\s[A-Z][a-z]+)+).*?([\w\.-]+@[\w\.-]+)',
        text, re.DOTALL
    )
    for contact in fallback_contacts:
        if contact not in contacts:
            contacts.append(contact)
        if len(contacts) >= 3:
            break

    # Step 6: Try extracting company name
    company_match = re.search(r'(Company Name|Owner):?\s*(.+)', text, re.IGNORECASE)
    if not company_match:
        company_match = re.search(r'([A-Z][\w\.\s&,-]+(?:LLC|Inc|Ltd|Corporation|Services))', text)

    company = (
        company_match.group(2).strip() if company_match and company_match.lastindex == 2
        else company_match.group(1).strip() if company_match
        else "Unknown Company"
    )

    # Step 7: Return final result
    return {
        "company": company,
        "contacts": contacts[:3]  # Max 3 contacts
    }
