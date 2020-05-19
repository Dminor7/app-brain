from login import Login
from utils import Apps
from config import config
from detail_page import DetailPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import exceptions
from bs4 import BeautifulSoup 
from urllib.parse import urljoin
from time import sleep
from random import uniform
import os
import codecs
import pandas as pd

def d_links(url, page_source):
    soup = BeautifulSoup(page_source, 'lxml')
    anchors = soup.find_all("a",attrs={'class':'dev-page-table-app-link'},href=True) 
    if anchors:
        detail_links = [urljoin(url,a['href']) for a in anchors]
    else:
         detail_links = None

    return detail_links


def make_csv(apps_dataframes, filename):
    change_log_data = []
    rating_history_data = [] 
    for dp in apps_dataframes:
        change_log_data.append(dp.df_change_log)
        rating_history_data.append(dp.df_rating_history)
    change_log_df = pd.concat(change_log_data, ignore_index=True)
    rating_history_df = pd.concat(rating_history_data, ignore_index=True)
    change_log_df.to_csv("Ch_"+filename,index=False)
    rating_history_df.to_csv("Rh_"+filename,index=False)


def crawl(url_list):

    configurations = config()
    l = Login()

    driver = l.gmail(email=configurations['email'], password=configurations['password'])
    
    try:
        for url in url_list:
            driver.get(url)

            try:
                # Wait Until Table Loads
                WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.ID,Apps.TABLE))
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
            filename = url.split("/")[-2].replace("+","") + Apps.FILE_EXTENSION
            apps_dataframes = []
            detail_links = d_links(url, page_source)
            sleep(uniform(1.5,3.1))
            if detail_links:
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
                        with codecs.open(app_name.split(".")[-1]+".html",'w',"utf-8") as f:
                            f.write(page_source)
                        try:
                            apps_dataframes.append(DetailPage(app_name,page_source).scrape())
                        except Exception as e:
                            pass
                make_csv(apps_dataframes, filename)
            sleep(uniform(2.5,6.3))

    except Exception as e:
        raise e("Error getting the requested page")
    finally:
        driver.quit()


# crawl(["https://www.appbrain.com/dev/Virtual+Apps+2019/"])

# print(d_links("https://www.appbrain.com/dev/Virtual+Apps+2019/",open("page_source.html",'r').read())[:2])


# make_csv([
#             DetailPage("remoteforall",open("remoteforall.html","r").read()).scrape(),
#             DetailPage("screenmirroring",open("screenmirroring.html","r").read()).scrape(),
#         ],"VirtualApps2019.csv")