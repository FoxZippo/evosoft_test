# 3. Парсинг последних твитов Elon Musk (сложное).
# Используя HTTP-запрос получить список последних 20 твитов Илона Маска.
# Вывести в лог только текст (если есть) последних твитов.
# Нужные для запроса вспомогательные данные рекомендуется получить через webdriver (Selenium).
# Действия должны повторять пользовательский путь, официальное API Twitter в задаче не должно быть использовано.

# Будет плюсом:
# - Использование проксирования
# - Схожесть поведения с реальным пользовательским насколько это возможно

import logging
import os
import random
import time

from seleniumwire import webdriver

logger = logging.getLogger('seleniumwire')
logger.setLevel(logging.WARNING)
logging.basicConfig(filename='twitter_musk.log', level=logging.INFO)


class TwitterParser:
    twitter_url = 'https://twitter.com'
    num_of_articles = 20
    transform_reg = r'translateY\((\d+\.\d)px\)'

    def __init__(self, twitter_username: str, twitter_password: str):
        self._username = twitter_username
        self._password = twitter_password

    @staticmethod
    def _interceptor(request):
        """ Changes request headers """
        request.headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36'
        request.headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'

    def login(self, driver):
        login_form = driver.find_element_by_xpath('//form[@action="/sessions"]')

        email_input = login_form.find_element_by_xpath('//input[@name="session[username_or_email]"]')
        email_input.send_keys(self._username)

        pass_input = login_form.find_element_by_xpath('//input[@name="session[password]"]')
        pass_input.send_keys(self._password)

        submit_btn = login_form.find_element_by_xpath('//div[@role="button"]')
        submit_btn.click()

    def parse(self):
        """ Parses last 20 Elon Musk tweets """
        with webdriver.Chrome() as driver:
            driver.request_interceptor = self._interceptor
            driver.get(self.twitter_url)
            login_btn = driver.find_element_by_xpath('//a[@href="/login"]')
            login_btn.click()
            time.sleep(random.uniform(1, 4))
            self.login(driver)
            driver.get(f'{self.twitter_url}/elonmusk')
            tweets = driver.find_element_by_xpath('//div[count(div) > 5]') \
                           .find_elements_by_xpath('div')
            result = []
            while len(result) < self.num_of_articles:
                time.sleep(random.uniform(2, 4))

                last_tweet = tweets[-1]

                text = [tweet.find_element_by_xpath('descendant::div[@role="group"]/preceding-sibling::*[last()]').text for tweet in tweets]
                result.extend(text)

                driver.execute_script("arguments[0].scrollIntoView();", last_tweet)
                time.sleep(random.uniform(2, 4))
                tweets = last_tweet.find_elements_by_xpath('following-sibling::*')

            logging.info('\n\n'.join(result[:self.num_of_articles]))


if __name__ == '__main__':
    username = os.environ.get('TWITTER_USERNAME')
    password = os.environ.get('TWITTER_PASSWORD')

    TwitterParser(username, password).parse()
