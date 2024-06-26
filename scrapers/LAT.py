import hashlib
import time
from pathlib import Path
from typing import List

from dateutil import parser
from RPA.Browser.Selenium import Selenium
from RPA.HTTP import HTTP
from selenium.common.exceptions import NoSuchElementException
from tenacity import retry

from utils import (
    WorkItemHandler,
    get_month_range,
    wait_for_element_and_click,
)

from .constants import BASE_URL, XPATH_SELECTORS
from .log import log_decorator, logger
from .news import News
from .parse import ParserNews
from .schemas.selectors import XPathSelectors
from .schemas.sort_option import Sort_By


class AngelesTimesScraper(ParserNews):
    def __init__(self, browser: Selenium):
        """
        Initialize the scraper with the browser and necessary handlers.

        :param browser: Selenium instance used for browsing.
        """
        super().__init__()
        self._browser = browser
        self.payload_handler = WorkItemHandler().get_current_payload()
        self.requests = HTTP()
        self.log = logger
        self.xpathselectors = XPathSelectors()

    @log_decorator
    @retry(stop=3, wait=2000)
    def _extract_news_images(self, data: List[News]):
        """
        Download news images and save them locally.

        :param data: List of News objects containing news information.
        """
        output_directory = Path("./output")
        output_directory.mkdir(exist_ok=True)

        for news in data:
            if not news.image_src:
                continue

            # TODO: Handle file name collisions
            title_hash = hashlib.md5(news.title.encode()).hexdigest()
            file_name = f"{title_hash}_{news.title}.jpg"
            file_path = output_directory / file_name

            try:
                self.requests.download(news.image_src, str(file_path))
                news.image_file_name = file_name
                self.log.info(f"Image downloaded for news item {news.title}")
            except Exception as e:
                self.log.error(f"Failed to download image for news item {news}: {e}")
                time.sleep(5)  # Wait for 5 seconds before trying again

    @log_decorator
    @retry(stop=3, wait=2000)
    def _get_news_data(self, number_of_months: int = 1) -> List[News]:
        """
        Extract news data from the website.

        :param number_of_months: Number of months to consider for extraction.
        :return: List of News objects containing news information.
        """
        self._browser.wait_for_condition(
            'return document.readyState == "complete"', timeout=30
        )
        try:
            try:
                self._browser.wait_until_element_is_visible(
                    XPATH_SELECTORS["menu_no_results"], timeout=5
                )
            except Exception:
                self.log.info("No results found, we have data to scrape")

            result = self._browser.get_element_count(XPATH_SELECTORS["menu_no_results"])
            if result > 0:
                return [{"No results found": "No results found"}]

            start_date = get_month_range(number_of_months)
            list_news = []
            self._browser.wait_until_element_is_visible(
                XPATH_SELECTORS["label_page_counts"], timeout=30
            )
            page_count = self._browser.get_text(XPATH_SELECTORS["label_page_counts"])
            page_count = page_count.strip().replace(",", "").split(" ")[-1]

            for j in range(1, int(page_count) + 1):
                self.log.info(f"Page {j} of {page_count}")
                self._browser.wait_for_condition(
                    'return document.readyState == "complete"', timeout=30
                )
                self._browser.wait_until_element_is_visible(
                    XPATH_SELECTORS["menu_search_results"], timeout=30
                )
                results_per_page = self._browser.get_element_count(
                    XPATH_SELECTORS["menu_search_results"]
                )
                for i in range(1, results_per_page + 1):
                    date = self._browser.get_text(
                        XPATH_SELECTORS["menu_search_results_timestamp"].format(count=i)
                    )
                    title = self._browser.get_text(
                        XPATH_SELECTORS["menu_search_results_title"].format(count=i)
                    )
                    try:
                        description = self._browser.get_text(
                            XPATH_SELECTORS["menu_search_results_description"].format(
                                count=i
                            )
                        )
                    except NoSuchElementException:
                        description = ""

                    self._browser.wait_until_element_is_visible(
                        XPATH_SELECTORS["menu_search_results_img"].format(count=i),
                        timeout=30,
                    )
                    img_url = self._browser.get_element_attribute(
                        XPATH_SELECTORS["menu_search_results_img"].format(count=i),
                        "src",
                    )

                    date = parser.parse(date, fuzzy=True)
                    self.log.info(f"Start date: {start_date} End date: {date}")
                    if date < start_date:
                        return list_news

                    list_news.append(
                        News(
                            search_phrase=self.payload_handler.search_phrase,
                            title=title,
                            description=description,
                            date=date,
                            image_src=img_url,
                        )
                    )
                if j == 10:
                    break
                self._browser.click_element(XPATH_SELECTORS["btn_next_page"])
            return list_news
        except Exception as e:
            self.log.error(f"Error extracting news data: {e}")
            return []

    @log_decorator
    @retry(stop=3, wait=2000)
    def _get_news(self, number_of_months: int) -> List[News]:
        """
        Get news and their images.

        :param number_of_months: Number of months to consider for extraction.
        :return: List of News objects containing news information.
        """
        news = self._get_news_data(number_of_months)
        self._extract_news_images(news)
        return news

    @log_decorator
    @retry(stop=3, wait=2000)
    def _got_to_sort_items(self, sort_option: int = 1):
        """
        Sort items according to the selected option.

        :param sort_option: Sorting option.
        """
        try:
            self._browser.select_from_list_by_value(
                XPATH_SELECTORS["search_page_sort"], sort_option
            )
            self._browser.wait_for_condition(
                'return document.readyState == "complete"', timeout=30
            )
        except Exception as e:
            self.log.error(f"Error sorting items: {e}")

    @log_decorator
    @retry(stop=3, wait=2000)
    def _go_to_search_topic(self):
        """
        Navigate to the search page for the specified topic.
        """
        self.log.info(f"Topic: {self.payload_handler.topic}")
        try:
            self._browser.wait_for_condition(
                'return document.readyState == "complete"', timeout=50
            )

            topic_exist = self._browser.get_element_count(
                XPATH_SELECTORS["news_input_topic"].format(
                    topic=self.payload_handler.topic
                )
            )
            if topic_exist < 1:
                self.log.warning(f"Topic {self.payload_handler.topic} not found")
            else:
                self._browser.wait_until_element_is_enabled(
                    XPATH_SELECTORS["news_input_topic"].format(
                        topic=self.payload_handler.topic
                    ),
                    timeout=30,
                )
                self._browser.click_element(
                    XPATH_SELECTORS["news_input_topic"].format(
                        topic=self.payload_handler.topic
                    )
                )
                self._browser.wait_for_condition(
                    'return document.readyState == "complete"', timeout=30
                )
                time.sleep(2)
        except Exception as e:
            self.log.error(f"Error navigating to search topic: {e}")

    @log_decorator
    @retry(stop=3, wait=2000)
    def _go_to_search_page(self):
        """
        Navigate to the search page.
        """
        try:
            wait_for_element_and_click(
                self._browser, XPATH_SELECTORS["news_search_button"]
            )
            self._browser.input_text(
                XPATH_SELECTORS["news_search_input"],
                self.payload_handler.search_phrase,
            )
            wait_for_element_and_click(
                self._browser, XPATH_SELECTORS["news_search_submit"]
            )
        except Exception as e:
            self.log.error(f"Error navigating to search page: {e}")
            raise

    @log_decorator
    @retry(stop=3, wait=2000)
    def _go_to_main_page(self):
        """
        Navigate to the main page.
        """
        try:
            self._browser.go_to(BASE_URL)
        except Exception as e:
            self.log.error(f"Error navigating to main page: {e}")
            raise

    @log_decorator
    @retry(stop=3, wait=2000)
    def _scroll_down_once(self):
        """
        Scroll down the page once.
        """
        try:
            self._browser.execute_javascript("window.scrollBy(0, window.innerHeight);")
            self._browser.execute_javascript(
                'document.querySelectorAll("video").forEach(ad => ad.style.display = "none");'
            )
        except Exception as e:
            self.log.error(f"Error scrolling down: {e}")
            raise

    @log_decorator
    def extract(self):
        """
        Main method to extract news.
        """
        try:
            self._go_to_main_page()
            self._scroll_down_once()
            self._go_to_search_page()
            self._go_to_search_topic()
            self._got_to_sort_items(sort_option=Sort_By.NEWEST)
            time.sleep(5)
            news = self._get_news(number_of_months=self.payload_handler.months)
            self.parse(news)
            time.sleep(5)
        except Exception as e:
            self.log.error(f"Error in extraction process: {e}")
