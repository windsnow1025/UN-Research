from urllib.parse import urlparse, urlunparse

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.expected_conditions import (
    presence_of_element_located,
    presence_of_all_elements_located,
    staleness_of,
)
from selenium.webdriver.support.wait import WebDriverWait


def get_base_url(full_url: str) -> str:
    parsed_url = urlparse(full_url)
    base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, parsed_url.path, '', '', ''))
    return base_url


class Scraper:
    def __init__(self, url: str, headless: bool, timeout: float):
        options = Options()
        
        if headless:
            options.add_argument("--headless=new")
        
        options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36"
        )

        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(timeout)
        self.driver.get(url)
        self.timeout = timeout
    
    def _wait(
        self,
        element: WebDriver | WebElement = None,
        timeout: float | None = None
    ) -> WebDriverWait:
        if timeout is None:
            timeout = self.timeout
        if element is None:
            element = self.driver
        return WebDriverWait(element, timeout=timeout)
    
    def _wait_find(
        self,
        path: str,
        element: WebDriver | WebElement = None,
        find_all: bool = False,
        timeout: float | None = None
    ) -> WebElement | list[WebElement]:
        if timeout is None:
            timeout = self.timeout
        if element is None:
            element = self.driver
        if not find_all:
            return self._wait(element, timeout=timeout).until(
                presence_of_element_located((By.XPATH, path))
            )
        else:
            return self._wait(element, timeout=timeout).until(
                presence_of_all_elements_located((By.XPATH, path))
            )
    
    def _wait_for_staleness(
        self,
        element: WebElement,
        timeout: float | None = None
    ):
        if timeout is None:
            timeout = self.timeout
        WebDriverWait(self.driver, timeout).until(staleness_of(element))
    
    def close(self):
        self.driver.quit()
    
    def __enter__(self):
        return self
    
    def __exit__(self, *args):
        self.close()
