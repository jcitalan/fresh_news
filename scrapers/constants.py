BASE_URL = "https://www.latimes.com/"

BROWSER_OPTIONS = [
    "--no-sandbox",
    "--disable-web-security",
    "--disable-dev-shm-usage",
    "--memory-pressure-off",
    "--ignore-certificate-errors",
    "--disable-notifications",
    "--start-maximized",
    "--disable-logging",
    "--disable-extensions",
]

XPATH_SELECTORS = {
    "news_search_button": 'xpath://button[@data-element="search-button"]',
    "news_search_input": 'xpath://input[@data-element="search-form-input"]',
    "news_search_submit": 'xpath://button[@data-element="search-submit-button"]',
    "news_input_topic": 'xpath://span[contains(text(),"{topic}")]/parent::label/input[@class="checkbox-input-element"]',
    "search_page_sort": 'xpath://select[@class="select-input"]',
    "menu_no_results": 'xpath://*[contains(text(),"There are not any results that match")]',
    "menu_search_results": 'xpath://ul[@class="search-results-module-results-menu"]/li',
    "menu_search_results_title": 'xpath:(//h3[@class="promo-title"])[{count}]',
    "menu_search_results_description": 'xpath:(//p[@class="promo-description"])[{count}]',
    "menu_search_results_timestamp": 'xpath:(//p[@class="promo-timestamp"])[{count}]',
    "menu_search_results_img": 'xpath:(//img[@class="image"])[{count}]',
    "label_page_counts": 'xpath://div[@class="search-results-module-page-counts"]',
    "btn_next_page": 'xpath://div[@class="search-results-module-next-page"]/a',
}
# input_topic = 'xpath://span[contains(text(),"{topic}")]/parent::label/input[@class="checkbox-input-element"]'
