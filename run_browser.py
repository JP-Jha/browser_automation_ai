
import sys
import os
import time
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError

# ------------- Helper Functions -------------
def perform_normal_web_search(page, url, query, extracted_file):
    page.goto(url, wait_until="networkidle")
    time.sleep(2)
    extracted_titles = []
    if query:
        try:
            page.wait_for_selector('input[name="q"]', timeout=15000)
            page.fill('input[name="q"]', query)
            page.keyboard.press("Enter")
            page.wait_for_timeout(5000)

            # Deep scrolling
            for _ in range(10):
                page.mouse.wheel(0, 3000)
                time.sleep(2)

            try:
                titles = page.locator('h2').all_text_contents()
                if not titles:
                    titles = page.locator('h3').all_text_contents()
            except Exception:
                titles = []

            extracted_titles = titles if titles else ["No titles found."]

        except PlaywrightTimeoutError:
            print("Search box not found, skipping search and extraction.")
            extracted_titles = ["Search box not found."]

    save_extracted_data(extracted_titles, extracted_file)


def perform_skyscanner_search(page, source, destination, departure_date, return_date, adults, children, extracted_file):
    page.goto("https://www.skyscanner.com", wait_until="networkidle")
    time.sleep(3)

    # Enter source city
    page.click('input[aria-label="From"]')
    page.fill('input[aria-label="From"]', source)
    page.wait_for_timeout(1000)
    page.keyboard.press("Enter")

    # Enter destination city
    page.click('input[aria-label="To"]')
    page.fill('input[aria-label="To"]', destination)
    page.wait_for_timeout(1000)
    page.keyboard.press("Enter")

    # Select departure date
    page.click('button[data-testid="depart-fsc-datepicker-button"]')
    page.wait_for_timeout(1000)
    # Just basic way (advanced date pick needs more)
    page.keyboard.press("Enter")

    # Set passengers
    try:
        page.click('button[data-testid="CabinClassTravellersSelector"]')
        time.sleep(1)

        for _ in range(adults - 1):
            page.click('button[data-testid="Adults-increase"]')
            time.sleep(0.5)
        for _ in range(children):
            page.click('button[data-testid="Children-increase"]')
            time.sleep(0.5)

        page.click('button[data-testid="CabinClassTravellersSelector-done"]')
    except Exception:
        print("Passenger selection may have changed.")

    # Click Search button
    page.click('button[type="submit"]')
    page.wait_for_timeout(8000)

    # Deep scrolling to load more flights
    for _ in range(5):
        page.mouse.wheel(0, 3000)
        time.sleep(2)

    # Extract flight titles
    try:
        flights = page.locator('div[data-testid="itinerary-title"]').all_text_contents()
    except Exception:
        flights = []

    flights = flights if flights else ["No flights found."]
    save_extracted_data(flights, extracted_file)

def perform_gmail_login(page, email, password, extracted_file):
    page.goto("https://accounts.google.com/signin", wait_until="networkidle")
    time.sleep(3)
    results = []
    try:
        page.fill('input[type="email"]', email)
        page.click('button:has-text("Next")')
        page.wait_for_timeout(3000)

        page.fill('input[type="password"]', password)
        page.click('button:has-text("Next")')
        page.wait_for_timeout(5000)

        if "challenge" in page.url:
            results = ["Captcha detected, login blocked."]
        else:
            results = ["Login attempted successfully."]

    except Exception:
        results = ["Login failed or blocked."]
    save_extracted_data(results, extracted_file)
    
def save_extracted_data(data_list, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        for line in data_list:
            f.write(line + "\n")

# ------------- Main Execution -------------
def main():
    mode = sys.argv[1]  # 'search', 'flight', 'gmail'
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(record_video_dir="recordings")
        page = context.new_page()
        if mode == "search":
            url = sys.argv[2]
            query = sys.argv[3]
            recording_file = sys.argv[4]
            extracted_file = sys.argv[5]

            perform_normal_web_search(page, url, query, extracted_file)
        elif mode == "flight":
            source = sys.argv[2]
            destination = sys.argv[3]
            departure_date = sys.argv[4]
            return_date = sys.argv[5]
            adults = int(sys.argv[6])
            children = int(sys.argv[7])
            recording_file = sys.argv[8]
            extracted_file = sys.argv[9]
            perform_skyscanner_search(page, source, destination, departure_date, return_date, adults, children, extracted_file)

        elif mode == "gmail":
            email = sys.argv[2]
            password = sys.argv[3]
            recording_file = sys.argv[4]
            extracted_file = sys.argv[5]
            perform_gmail_login(page, email, password, extracted_file)
        else:
            print("Invalid mode selected. Choose 'search', 'flight', or 'gmail'.")

        # Properly close browser
        page.close()
        context.close()
        browser.close()
        # Fix file locking delay before rename
        time.sleep(2)
        # Rename the recorded video file to correct name
        videos = os.listdir("recordings")
        videos = sorted([f for f in videos if f.endswith('.webm')], key=lambda x: os.path.getctime(os.path.join("recordings", x)))
        latest = videos[-1]
        os.rename(os.path.join("recordings", latest), recording_file)
if __name__ == "__main__":
    main()
