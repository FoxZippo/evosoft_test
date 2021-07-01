import logging
import os
import random
import time

from dotenv import load_dotenv
from seleniumwire import webdriver

from utils import interceptor

load_dotenv()

logger = logging.getLogger('seleniumwire')
logger.setLevel(logging.WARNING)
logging.basicConfig(filename='../twitter_musk.log', level=logging.INFO)


class TwitterParser:
    twitter_url = 'https://twitter.com'
    num_of_articles = 20

    def __init__(self, twitter_username: str, twitter_password: str):
        self._username = twitter_username
        self._password = twitter_password

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
            driver.request_interceptor = interceptor
            driver.get(self.twitter_url)
            login_btn = driver.find_element_by_xpath('//a[@href="/login"]')
            login_btn.click()
            time.sleep(random.uniform(2, 4))
            self.login(driver)
            driver.get(f'{self.twitter_url}/elonmusk')
            time.sleep(random.uniform(2, 4))
            tweets = driver.find_elements_by_xpath('//div[@data-testid="primaryColumn"]/descendant::section/div/div/div')

            result = []
            while len(result) < self.num_of_articles:
                time.sleep(random.uniform(2, 4))

                last_tweet = tweets[-1]
                text = [tweet.find_element_by_xpath('descendant::div[@role="group"]/preceding-sibling::*[last()]').text for tweet in tweets]
                result.extend(text)

                driver.execute_script('arguments[0].scrollIntoView();', last_tweet)
                time.sleep(random.uniform(2, 4))
                tweets = last_tweet.find_elements_by_xpath('following-sibling::*')

            logging.info('\n\n'.join(result[:self.num_of_articles]))


if __name__ == '__main__':
    username = os.environ.get('TWITTER_USERNAME')
    password = os.environ.get('TWITTER_PASSWORD')

    TwitterParser(username, password).parse()
