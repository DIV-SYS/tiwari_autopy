from playwright.sync_api import sync_playwright
import os

def download_pdfs(permit_id):
    save_dir = 'permit_automation/input/downloaded_pdfs'
    os.makedirs(save_dir, exist_ok=True)
    file_paths = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        url = f"https://dataviewers.tdec.tn.gov/dataviewers/f?p=2005:34051:::NO::P34051_PERMIT_NUMBER={permit_id}"
        page.goto(url)
        page.wait_for_selector("a.t-Button--hot", timeout=10000)

        buttons = page.query_selector_all("a.t-Button--hot")
        for i, btn in enumerate(buttons):
            with page.expect_download() as download_info:
                btn.click()
            download = download_info.value
            file_path = os.path.join(save_dir, f"{permit_id}_{i}.pdf")
            download.save_as(file_path)
            file_paths.append(file_path)

        browser.close()
    return file_paths
