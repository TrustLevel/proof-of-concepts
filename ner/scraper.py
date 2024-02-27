from playwright.sync_api import TimeoutError, sync_playwright


def scrape_text(url):
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            # Increase the timeout to 60 seconds and wait until 'domcontentloaded'
            page.goto(url, timeout=60000, wait_until='domcontentloaded')
            # Try to find <main> tag, if not, try to find className equal to article, if not just get everything as is
            if page.is_visible("main"):
                text = page.inner_text("main")
            elif page.is_visible(".article"):
                text = page.inner_text(".article")
            else:
                text = page.inner_text('body')
        except TimeoutError:
            text = "A timeout occurred while loading the page."
        finally:
            browser.close()
        return text