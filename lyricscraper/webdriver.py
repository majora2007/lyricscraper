from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import Proxy, ProxyType

import time
import os
import logging

logger = logging.getLogger('lyricscraper')


class WebDriver(object):
    # Time in seconds to wait for an element to render. This can cause slow downs in code by waiting for extra time.
    wait_time = 5
    # This is how we reset wait_time. Keep the same
    WAIT_TIME = 5
    driver = None

    def __init__(self):
        self.driver = None
        
    def init_chrome(self, download_dir='', headless=True):
        opts = webdriver.ChromeOptions()
        opts.add_argument('--no-sandbox')
        opts.add_argument("--disable-gpu")
        opts.add_argument('log-level=3')
        opts.add_argument("--window-size=1920,1200")
        opts.add_argument("--ignore-certificate-errors")

        if headless:
            opts.add_argument("--headless")

        if download_dir != '':
            logger.debug('Download Directory: {0}'.format(download_dir))
            prefs = {'download.default_directory': download_dir}
            opts.add_experimental_option('prefs', prefs)


        logger.debug('Opening Chrome')
        # fileExt = '.exe' if (config_parser['Selenium']['PLATFORM'] == 'win') else ''
        # driver = webdriver.Chrome('./drivers/' + config_parser['Selenium']['PLATFORM'] + '/chromedriver' + fileExt, chrome_options=opts)
        self.driver = webdriver.Chrome(chrome_options=opts, service_log_path=os.devnull)
        return self.driver

    def switch_to_frame(self, elem_id):
        logger.debug('Switching to {0} iFrame'.format(elem_id))
        # wait_for_iframe(driver, '//iframe[id="ngtModule"]')
        self.driver.switch_to_frame(elem_id)
        # Ensure the iframe is loaded 
        # verify_iframe(driver, 'iframe[id="ngtModule"]')
        # self.driver.frame_to_be_available_and_switch_to_it('ngtModule')

    def switch_to_window(self):
        logger.debug('Switching to new window')
        for handle in self.driver.window_handles:
            self.driver.switch_to_window(handle)

    def verify_iframe(self, selector):
        WebDriverWait(self.driver, self.wait_time).until(
            EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR, selector)))

    def verify_elem(self, selector):
        elem = WebDriverWait(self.driver, self.wait_time).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        return elem

    def verify_elem_xpath(self, selector):
        elem = WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((By.XPATH, selector)))
        return elem

    def verify_elems(self, selector):
        WebDriverWait(self.driver, self.wait_time).until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
        elems = self.driver.find_elements_by_css_selector(selector)
        return elems

    @staticmethod
    def sleep(t):
        logger.debug('Sleeping for {0} seconds'.format(t))
        time.sleep(t)  # Wait for a few seconds

    def get_url(self, url):
        logger.debug('Fetching {0}'.format(url))
        self.driver.get(url)

    @staticmethod
    def verify_file(path, filename):
        full_path = os.path.join(path, filename)
        logger.debug('Verifying file exists: {0}'.format(full_path))
        while not os.path.exists(full_path):
            time.sleep(1)

    def close(self):
        if self.driver:
            self.driver.quit()

    def set_time(self, wait_time):
        """ Sets internal time to wait for an element to show up before throwing exception """
        self.wait_time = wait_time

    def reset_time(self):
        # """ Reset the internal time to wait for an element to show up to factory default """
        self.wait_time = self.WAIT_TIME

    def current_url(self):
        if self.driver:
            return self.driver.current_url
        return ''
    
    def is_alive(self):
        try:
            self.driver.title
            return True
        except:
            pass
        
        return False
        
