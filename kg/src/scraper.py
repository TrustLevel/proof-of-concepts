from playwright.sync_api import TimeoutError, sync_playwright


def scrape_article_text(url):
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
    

def get_img_from_url(url) -> str:
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        try:
            page.goto(url, timeout=30000, wait_until='domcontentloaded')
            # First, try to get image from meta tags
            meta_img = page.query_selector("meta[property='og:image']")
            if meta_img:
                img_src = meta_img.get_attribute('content')
                return img_src
            # If no image in meta tags, look for the first image in the page
            img_elements = page.query_selector_all('img')
            if img_elements:
                img_src = img_elements[0].get_attribute('src')
                return img_src
            else:
                return None
        except TimeoutError:
            return None
        finally:
            browser.close()
