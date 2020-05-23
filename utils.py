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


class Apps:
    DETAIL_LINKS = "dev-page-table-app-link"
    FILE_EXTENSION = ".csv"
    TABLE = "app_table_gwt"
    SHOW_MORE = "//*[@id='app_table_gwt']/table/tbody/tr[2]/td/table/tbody/tr/td/a"
    CL_UL_TAG = "app-changelog"
    CL_DATE = "app-changelog-date"
    CL_STATUS = "app-changelog-type"
    CL_DESCRIPTION = "app-changelog-description"
    IT_MAIN_CONTENT = "div#main_content > div.infotiles"
    RH_RATINGS = "#ratinghistory > div.table-div"
    RH_VOTES = "app-ratings-cell-votes"
    RH_STARS = "app-ratings-cell-stars"
    RH_RATING_DATA = "var ratingHistoryData = (.*?);"
    


class Path:
    INPUT = os.path.join(os.getcwd(),"input")
    OUPUT = os.path.join(os.getcwd(),"ouput")