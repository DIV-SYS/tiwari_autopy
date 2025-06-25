import os
import re
import requests
from urllib.parse import urlparse, parse_qs

def download_pdfs_from_drive_link(link):
    # Extract file ID from drive link
    match = re.search(r"/d/([\w-]+)|id=([\w-]+)", link)
    file_id = match.group(1) if match.group(1) else match.group(2)

    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    response = requests.get(url)

    os.makedirs("permit_automation/temp_pdfs", exist_ok=True)
    path = f"permit_automation/temp_pdfs/{file_id}.pdf"
    with open(path, "wb") as f:
        f.write(response.content)
    return [path]