from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        page.goto("https://www.google.com")
        print(f"Page Title: {page.title()}")

        page.fill('textarea[name="q"]', "Latest news on Data Science")
        
        # Press Enter
        page.press('[name="q"]', "Enter")
        # Keeping the window open for 60 seconds as requested
        page.wait_for_timeout(60000)
        browser.close()

if __name__ == "__main__":
    run()

