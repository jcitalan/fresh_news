class XPathSelectors:
    @classmethod
    def get_news_search_button(cls):
        return 'xpath://button[@data-element="search-button"]'

    @classmethod
    def get_news_search_input(cls):
        return 'xpath://input[@data-element="search-form-input"]'

    @classmethod
    def get_news_search_submit(cls):
        return 'xpath://button[@data-element="search-submit-button"]'

    @classmethod
    def get_news_input_topic(cls, topic):
        return f'xpath://span[contains(text(),"{topic}")]/parent::label/input[@class="checkbox-input-element"]'

    @classmethod
    def get_search_page_sort(cls):
        return 'xpath://select[@class="select-input"]'

    @classmethod
    def get_menu_no_results(cls):
        return 'xpath://*[contains(text(),"There are not any results that match")]'

    @classmethod
    def get_menu_search_results(cls):
        return 'xpath://ul[@class="search-results-module-results-menu"]/li'

    @classmethod
    def get_menu_search_results_title(cls, count):
        return f'xpath:(//h3[@class="promo-title"])[{count}]'

    @classmethod
    def get_menu_search_results_description(cls, count):
        return f'xpath:(//p[@class="promo-description"])[{count}]'

    @classmethod
    def get_menu_search_results_timestamp(cls, count):
        return f'xpath:(//p[@class="promo-timestamp"])[{count}]'

    @classmethod
    def get_menu_search_results_img(cls, count):
        return f'xpath:(//img[@class="image"])[{count}]'

    @classmethod
    def get_label_page_counts(cls):
        return 'xpath://div[@class="search-results-module-page-counts"]'

    @classmethod
    def get_btn_next_page(cls):
        return 'xpath://div[@class="search-results-module-next-page"]/a'
