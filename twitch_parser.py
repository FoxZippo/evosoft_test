# 2. Поиск результатов Twitch (среднее).
# Повторить действия пользователя по вводу запроса "Pool" (ну или свой по желанию) в строку поиска.
# Получить результаты предпросмотра поискового запроса
# (подcказки перед отправкой запроса поиска) и результаты самого поиска.
# Из результатов поиска достать все ссылки и вывести в лог.

import logging
import random
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver

TWITCH_URL = 'https://twitch.tv'
SEARCH_REQUEST = 'Pool'

logger = logging.getLogger('seleniumwire')
logger.setLevel(logging.WARNING)
logging.basicConfig(filename='twitch_pools.log', level=logging.INFO)


def interceptor(request):
    request.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
    request.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'


def get_proxy():
    pass


def parse_twitch(search_request: str):
    """ Writes to twitch.log links of result for search_request on twitch.tv """
    with webdriver.Chrome() as driver:
        webdriver.DesiredCapabilities.CHROME['proxy'] = {"httpProxy": get_proxy()}
        wait = WebDriverWait(driver, 10)
        driver.request_interceptor = interceptor
        driver.get(TWITCH_URL)
        pause_btn = driver.find_element_by_xpath(
            '//div[contains(@class, "player-controls")]//button[@data-a-target="player-play-pause-button"]')
        pause_btn.click()

        search_input = driver.find_element_by_xpath('//input[@type="search"]')
        search_input.click()
        search_input.send_keys(search_request)

        wait.until(presence_of_element_located((By.XPATH, '//div[@class="search-tray"]')))
        time.sleep(random.uniform(2, 4))
        hints = driver.find_elements_by_xpath('//div[@class="search-tray"]//a')
        hint_links = [hint.get_attribute('href') for hint in hints]
        logging.info('HINTS: \n' + '\n'.join(hint_links) + '\n')

        find_button = driver.find_element_by_xpath('//div[@data-a-target="tray-search-input"]//button')
        find_button.click()
        time.sleep(random.uniform(2, 4))

        a_tags = driver.find_elements_by_xpath('//div[@class="simplebar-scroll-content"]//a')
        links = [a_tag.get_attribute('href') for a_tag in a_tags]
        logging.info('CONTENT: \n' + '\n'.join(set(links)) + '\n')


if __name__ == '__main__':
    parse_twitch(SEARCH_REQUEST)
