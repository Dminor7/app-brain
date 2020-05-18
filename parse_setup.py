import os

class Apps:
    TABLE = "app_table_gwt"
    SHOW_MORE = "//*[@id='app_table_gwt']/table/tbody/tr[2]/td/table/tbody/tr/td/a"


class Elements:
    pass

class Path:
    INPUT = os.path.join(os.getcwd(),"input")
    OUPUT = os.path.join(os.getcwd(),"ouput")
