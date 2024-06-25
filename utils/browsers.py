from typing import Dict, List, Optional, Union

from RPA.Browser.Selenium import Selenium
from selenium.webdriver.remote.webelement import WebElement


class SeleniumBrowser:
    def __init__(
        self,
        selenium_settings: Optional[Dict[str, Union[int, float]]] = None,
        browser_settings: Optional[Dict[str, Union[str, bool]]] = None,
    ):
        self._selenium_settings = selenium_settings or {
            "timeout": 5,
            "implicit_wait": 10,
        }
        self._browser_settings = browser_settings or {"headless": True}
        self._browser = None

    def __enter__(self) -> Selenium:
        self._browser = Selenium(**self._selenium_settings)
        self._browser.open_available_browser(**self._browser_settings)
        return self._browser

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self._browser:
            self._browser.close_browser()


def wait_for_element_and_retrieve(
    browser: Selenium,
    locator: Union[str, WebElement],
    multiple: bool = False,
    timeout: int = 10,
) -> Union[WebElement, List[WebElement]]:
    browser.wait_until_element_is_visible(locator, timeout=timeout)

    if multiple:
        result = browser.get_webelements(locator)
    else:
        result = browser.get_webelement(locator)

    return result


def wait_for_element_and_click(
    browser: Selenium,
    locator: Union[str, WebElement],
    timeout: int = 10,
) -> WebElement:
    element = wait_for_element_and_retrieve(browser, locator, timeout=timeout)
    browser.click_element(element)
    return element
