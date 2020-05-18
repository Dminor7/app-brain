from gmail import login
from parse_setup import Apps,Elements
from config import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from bs4 import BeautifulSoup 
from urllib.parse import urljoin
from time import sleep
from random import uniform
import os

def get_detail_links(url, page_source):
    soup = BeautifulSoup(page_source, 'lxml')
    anchors = soup.find_all("a",attrs={'class':'dev-page-table-app-link'},href=True) 
    if anchors:
        detail_links = [urljoin(url,a['href']) for a in anchors]
    else:
         detail_links = None

    return detail_links


def parse(url_list):

    configurations = config()
    driver = login(email=configurations['email'], password=configurations['password'])
    
    try:
        for url in url_list:
            driver.get(url)

            try:
                # Wait Until Table Loads
                WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID,Apps.TABLE))
                )
            except exceptions.TimeoutException as e:
                pass

            # Click Show More Button 
            try:
                show_more = driver.find_element_by_xpath(Apps.SHOW_MORE)
                if show_more:
                    show_more.click()
            except exceptions.NoSuchElementException as e:
                pass    
            
            page_source = driver.page_source
            detail_links = get_detail_links(url, page_source)
            sleep(uniform(1.5,3.1))
            if detail_links:
                for link in detail_links:
                    driver.get(link)
                    # Wait For Page To Load
                    # Get source and parse

    except Exception as e:
        raise e("Error getting the requested page")
    finally:
        driver.quit()


get_detail_links("https://www.appbrain.com/dev/Virtual+Apps+2019/",open("page_source.html","r").read())