import os

class Gmail:
    WAIT_FLAG = "email"
    SIGNIN = "/html/body/div/div[2]/div[1]/div/div[2]/div[1]/div/div[1]/a[1]"
    # EMAIL = "identifier"
    EMAIL = "#view_container > div > div > div.pwWryf.bxPAYd > div > div.WEQkZc > div > form input[name=identifier]"
    EMAIL_NEXT = "//*[@id='identifierNext']/span/span"
    # PASSWORD = "password"
    PASSWORD = "#view_container > div > div > div.pwWryf.bxPAYd > div > div.WEQkZc > div > form input[name=password]"
    PASSWORD_NEXT = "//*[@id='passwordNext']/span/span"

class Config:
    USER_AGENT = "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
    CHROMEDRIVER = os.path.join(os.getcwd(),"chromedriver")


class AppBrainLogin:
    USER_ICON = "//*[@id='userIcon']"
    URL_CONTAINS = "appbrain"