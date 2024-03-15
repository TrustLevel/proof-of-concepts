from playwright.sync_api import TimeoutError, sync_playwright


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
