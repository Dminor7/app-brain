from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options 
from selenium.common import exceptions 
from login_setup import Gmail,Config,AppBrainLogin


chrome_options = Options()  
chrome_options.add_argument(Config.USER_AGENT)
chrome_options.add_argument("start-maximized")
chrome_options.add_argument("disable-infobars")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--headless")

LOGIN_URL = "https://www.appbrain.com/login"


def login(email, password):
    driver = webdriver.Chrome(executable_path=Config.CHROMEDRIVER, chrome_options=chrome_options)
    
    try:
        driver.get(LOGIN_URL)
    except Exception as e:
        raise e(f"Error fetching URL : {LOGIN_URL}")
    
    
    try:
        # Waiting till the page loads and <input> is visible
        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, Gmail.WAIT_FLAG))
        )

        sign_with_gmail = driver.find_element_by_xpath(Gmail.SIGNIN)
        if sign_with_gmail.is_displayed():
            sign_with_gmail.click()
        
        # Entering Gmail Email 
        input_email = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, Gmail.EMAIL))
        )

        input_email.send_keys(email) 

        driver.find_element_by_xpath(Gmail.EMAIL_NEXT).click()

        # Entering Password
        input_password = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, Gmail.PASSWORD))
        )
        input_password.send_keys(password) 

        driver.find_element_by_xpath(Gmail.PASSWORD_NEXT).click()
        
        # Waiting Till AppBrain Home Page Loads
        WebDriverWait(driver, 25).until(
        EC.url_contains(AppBrainLogin.URL_CONTAINS))

        WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, AppBrainLogin.USER_ICON))
        )
        
        return driver

    except exceptions.TimeoutException as e:
        raise e("Timeout Exceeded Check your Internet Connection")
    except  exceptions.NoSuchElementException as e:
        raise e("Element is not found in the DOM")
    except exceptions.ElementNotInteractableException as e:
        raise e("Element is present in the DOM but interactions with that element will hit another element do to paint order")
    

