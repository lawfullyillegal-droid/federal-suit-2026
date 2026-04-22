import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def run_audit(case_id):
    print(f"[*] INITIATING BARE-BONES AUDIT: {case_id}")

    options = Options()
    options.binary_location = "/data/data/com.termux/files/usr/bin/chromium-browser"
    
    # The 'Adversarial' Flag Set for Termux
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--disable-setuid-sandbox')
    options.add_argument('--memory-pressure-off')
    options.add_argument('--single-process') # Force single process to save RAM
    options.add_argument("user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36")

    service = Service(executable_path="/data/data/com.termux/files/usr/bin/chromedriver")

    try:
        driver = webdriver.Chrome(service=service, options=options)
        print("[*] Engine Engaged. Bypassing Administrative Gates...")
        
        driver.set_page_load_timeout(30)
        driver.get("https://apps.azcourts.gov/publicaccess/caselookup.aspx")
        
        # Searching
        print(f"[*] Injecting Case ID: {case_id}")
        search_field = driver.find_element(By.ID, "ctl00_mainContent_txtCaseNumber")
        search_field.send_keys(case_id)
        search_field.send_keys(Keys.RETURN)
        
        time.sleep(10)
        
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        ss_path = f"04_Kingman_Audit/evidence/AUDIT_FINAL_{case_id}_{timestamp}.png"
        driver.save_screenshot(ss_path)
        
        with open(f"04_Kingman_Audit/raw_data/{case_id}_SNAPSHOT.html", "w") as f:
            f.write(driver.page_source)
            
        print(f"[+] AUDIT SUCCESSFUL. Evidence secured.")

    except Exception as e:
        print(f"[!] AUDIT FAULT: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    run_audit("TR-2024-00143")
