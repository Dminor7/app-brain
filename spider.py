from login import Login
from utils import Apps
from detail_page import DetailPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from bs4 import BeautifulSoup 
from urllib.parse import urljoin
from urllib.request import urlparse
from time import sleep
from random import uniform
from datetime import datetime
import os
import codecs
import pandas as pd


class Spider:

    def __init__(self):
        self._ouput = os.path.join(os.getcwd(), 'output')
        self._base_url = "https://www.appbrain.com/dev/"

    def _d_links(self, url, page_source):
        '''
        Parse the developer account page to find links of detail page for apps

        Args:
        url: str Developer account url
        page_source: bs4.BeautifulSoup The source page

        Returns:
        detail_links: List Detail page links
        '''
        soup = BeautifulSoup(page_source, 'lxml')    
        anchors = soup.find_all("a",attrs={'class': Apps.DETAIL_LINKS}, href=True)
        if anchors:
            detail_links = [urljoin(url,a['href']) for a in anchors]
        else:
            detail_links = None
        return detail_links
    
    def _make_csv(self, apps_dataframes, filename):
        '''
        Makes two CSV files on Changelog and Rating Hostory
        
        Args: 
        apps_dataframes: List containg dataframe objects
        filename: str developer account name 
        '''
        change_log_data = []
        rating_history_data = [] 

        for detail_page in apps_dataframes:
            change_log_data.append(detail_page.df_change_log)
            rating_history_data.append(detail_page.df_rating_history)

        change_log_df = pd.concat(change_log_data, ignore_index=True)
        rating_history_df = pd.concat(rating_history_data, ignore_index=True)
        
        change_log_df['installs'] = change_log_df.description.str.extract('(?P<installs>.*installs)')
        change_log_df['update']   = change_log_df.description.str.extract('(?P<update>Version.*)')

        os.makedirs("output", exist_ok=True)
        date = datetime.now().strftime('%Y_%m_%d_')
        ch_filepath = os.path.join(self._ouput, date+"Ch_"+filename)
        rh_filepath = os.path.join(self._ouput, date+"Rh_"+filename)
        change_log_df.to_csv(ch_filepath, index=False)
        rating_history_df.to_csv(rh_filepath, index=False)

    def modify_urls(self, url_list):
        return [self._base_url + urlparse(url).query.split("=")[1].rstrip() + "/" for url in url_list]
    
    def crawl(self, url_list, email, password, gui_queue):

        l = Login()
        driver = l.gmail(email=email, password=password)
        
        try:
            # Iterating over developer account urls
            for url in url_list:
                print(url)
                driver.get(url)

                try:
                    # Wait until table loads
                    WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.ID,Apps.TABLE))
                    )
                except exceptions.TimeoutException as e:
                    pass

                
                try:
                    # Click show more button if exists
                    show_more = driver.find_element_by_xpath(Apps.SHOW_MORE)
                    if show_more:
                        show_more.click()
                except exceptions.NoSuchElementException as e:
                    pass    
                
                # Paring develper account and fetching detail page links for apps
                page_source = driver.page_source
                developer = url.split("/")[-2].replace("+","").replace("%20","")
                filename = developer + Apps.FILE_EXTENSION
                apps_dataframes = []
                detail_links = self._d_links(url, page_source) 
                
                sleep(uniform(1.5,3.1))
                
                if detail_links:
                    # Itrating over detail app pages for developer
                    for link in detail_links:
                        driver.get(link)

                        try:
                            # Wait Until Table Loads
                            main_content = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR,Apps.IT_MAIN_CONTENT))
                            )
                        except exceptions.TimeoutException as e:
                            pass
                        
                        if(main_content):
                            app_url = driver.current_url
                            app_name = app_url.split("/")[-1]
                            page_source = driver.page_source
                            # with codecs.open(app_name.split(".")[-1]+".html",'w',"utf-8") as f:
                            #     f.write(page_source)
                            try:
                                apps_dataframes.append(DetailPage(app_name,page_source).scrape())
                            except Exception as e:
                                pass
                        sleep(uniform(2.5,6.3))
                    self._make_csv(apps_dataframes, filename)
                message = "Check the CSV files for: " + developer
                gui_queue.put(message)    
            gui_queue.put("\t-----Completed-----\t")
        except Exception as e:
            raise e("Error getting the requested page")
        finally:
            driver.quit()