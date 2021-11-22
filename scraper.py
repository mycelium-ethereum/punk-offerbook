import re
import logging
import settings
import numpy as np
import pandas as pd
from typing import List
from utils import mongo
from time import time, sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime
from webdriver_manager.utils import ChromeType
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class CryptopunksScraper:
    BASE_URL = "https://www.larvalabs.com/cryptopunks"

    def __init__(self, headless: bool = True):
        self.logger = logging.getLogger('root')
        self.headless_toggle = headless
        self.create_driver()
        
    def create_driver(self):
        options = Options()
        options.headless = self.headless_toggle
        self.driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.GOOGLE).install(), options=options)

    def kill_driver(self):
        self.logger.debug('Killing driver now...')
        self.driver.quit()

    def get_floor_price(self):
        flag = True
        start_time = time()
        self.driver.get(self.BASE_URL)
        while flag:
            try:
                html = self.driver.page_source
                soup = BeautifulSoup(html, features="html.parser")
                all_rows = soup.find_all('b')
                val = float(all_rows[0].text.split(' ')[0])
                flag = False
            except:
                if time() - start_time > 5:
                    val = np.nan
                    flag = False
        return val