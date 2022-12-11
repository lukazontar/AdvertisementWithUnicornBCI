import random
import time
import urllib
from typing import List

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from tqdm import tqdm
from webdriver_manager.chrome import ChromeDriverManager


class FBAdLibraryPartyPageScraper:
    def __init__(self, page_id: str,
                 valid_ids: List[str]):
        self.page_id = page_id
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        self.driver.get(
            f'https://www.facebook.com/ads/library/?active_status=all&ad_type=political_and_issue_ads&country=SI&view_all_page_id={self.page_id}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=page&media_type=all')
        self.driver.implicitly_wait(0.2)
        time.sleep(random.uniform(18, 25))
        self.media_collection = []
        self.valid_ids = valid_ids

    def scroll_to_bottom(self):
        # Load all creatives
        while True:
            try:
                button_see_more = self.driver.find_element(by=By.XPATH,
                                                           value="//a[contains(.,'Prikaži več')]")
                self.driver.execute_script("arguments[0].click();", button_see_more)
                time.sleep(random.uniform(4, 6))

            # All creatives are loaded when "See more" is not on page
            except NoSuchElementException as e:
                print("Scroll to bottom finished.")
                break

    def collect_images(self):
        img_url_substring = 'https://scontent.flju4-1.fna.fbcdn.net/'

        images = self.driver.find_elements(by=By.XPATH,
                                           value=f"//img[contains(@src, '{img_url_substring}')]")

        return list(filter(lambda x: x.get_attribute('referrerpolicy') == 'origin-when-cross-origin', images))

    def collect_videos(self):
        video_url_substring = 'https://video.flju4-1.fna.fbcdn.net/'
        return self.driver.find_elements(by=By.XPATH,
                                         value=f"//video[contains(@src, '{video_url_substring}')]")

    def collect_media(self):
        for img_elem in tqdm(self.collect_images()):
            try:
                id_elem = img_elem.find_element(by=By.XPATH,
                                                value="./../../../../../..//*/span[contains(., 'ID: ')]")
                id = id_elem.get_attribute('innerHTML').split('ID: ')[1]
                if int(id) in self.valid_ids:
                    urllib.request.urlretrieve(url=img_elem.get_attribute('src'),
                                               filename=f'../data/media/{id}.jpg')
                    time.sleep(random.uniform(1, 2))
            except NoSuchElementException:
                continue

        for video_elem in tqdm(self.collect_videos()):
            try:
                id_elem = video_elem.find_element(by=By.XPATH,
                                                  value="./../../../../../../..//*/span[contains(., 'ID: ')]")
                id = id_elem.get_attribute('innerHTML').split('ID: ')[1]
                if int(id) in self.valid_ids:
                    urllib.request.urlretrieve(url=video_elem.get_attribute('src'),
                                               filename=f'../data/media/{id}.mp4')
            except NoSuchElementException:
                continue

    def close(self):
        self.driver.close()
