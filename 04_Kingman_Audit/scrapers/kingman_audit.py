import asyncio
import datetime
import os
from playwright.async_api import async_playwright

async def run_audit(case_id):
    async with async_playwright() as p:
        print(f"[*] Launching Stealth Audit for {case_id}...")
        # Added --no-sandbox for Termux stability
        browser = await p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            viewport={'width': 1280, 'height': 720}
        )
        page = await context.new_page()

        try:
            # Navigate to the portal
            print("[*] Accessing Arizona Judicial Branch Portal...")
            await page.goto("https://apps.azcourts.gov/publicaccess/caselookup.aspx", wait_until="networkidle")

            # Check for the Verification Gate
            if await page.query_selector('text=Verification'):
                print("[!] Verification Gate detected. Manual intervention or cookie persistence required.")

            print(f"[*] Injecting Case ID: {case_id}")
            await page.fill('input[name*="txtCaseNumber"]', case_id)
            await page.keyboard.press("Enter")
            
            # Allow time for 'Deterministic Truth' to render
            await page.wait_for_timeout(7000) 
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Save visual evidence
            img_path = f"04_Kingman_Audit/evidence/SCREENSHOT_{case_id}_{timestamp}.png"
            await page.screenshot(path=img_path)
            
            # Save raw data for Logic Audit
            content = await page.content()
            html_path = f"04_Kingman_Audit/raw_data/{case_id}_audit.html"
            with open(html_path, "w") as f:
                f.write(content)
                
            print(f"[+] Audit Complete.")
            print(f"[+] Visual Evidence: {img_path}")
            print(f"[+] Logic Source: {html_path}")

        except Exception as e:
            print(f"[!] Audit Interrupted: {e}")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_audit("TR-2024-00143"))
