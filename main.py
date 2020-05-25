import queue
import threading
import time
import PySimpleGUI as sg
from random import uniform
import pandas as pd
import os
from spider import Spider

class Gui:

    def __init__(self):
        sg.theme("DarkBlue3")
        icon = os.path.join(os.getcwd(),"crawl.ico")
        sg.SetOptions(font='opensans 11', icon = icon)
        self.layout =  [
                        [sg.Text("App Brain Crawler", font='sfprodisplay 25 bold')],
                        [sg.Text("Gmail Id",pad=((10,65),(10,10))), sg.InputText(key='_EMAIL_')],
                        [sg.Text("Gmail Password",pad=((10,10),(10,10))), sg.InputText(password_char='*',key='_PASS_')],
                        [sg.Text("Input CSV File",pad=((10,25),(10,10))), sg.InputText(key='_FILE_'), sg.FileBrowse()],
                        [sg.Button("Scrape", pad=((200,50),(10,10)), key='_SCRAPE_'), sg.Button("Quit", pad=((50,0),(10,10)), key='_QUIT_')],
                        [sg.Output(size=(200,400), pad=(0,(10,10)))]
                    ]
        self.window = sg.Window("Spider", size=(600,400), layout = self.layout)


if __name__ == '__main__':

    # queue used to communicate between the gui and the threads
    gui_queue = queue.Queue() 
    
    gui = Gui()               
    spidy = Spider()
    
    
    # --------------------- EVENT LOOP ---------------------
    while True:
         # wait for up to 100 ms for a GUI event
        event, values = gui.window.Read(timeout=100)      
        if event is None or event == '_QUIT_':
            break

        if event == '_SCRAPE_':
            email = values.get('_EMAIL_')
            password = values.get('_PASS_')
            filepath = values.get('_FILE_')

            if (all([email, password, filepath])):
                try:
                    df = pd.read_csv(filepath)
                    url_list = list(df.urls)
                    urls = spidy.modify_urls(url_list)
                    print('Starting to crawl will take approx {} seconds'.format(len(urls)*uniform(1.5678,2.9999)*120))
                    threading.Thread(target=spidy.crawl, args=(urls, email, password, gui_queue,), daemon=True).start()
                except Exception as e:
                    print("Error occured".format(e))
            else:
                print("Please don't leave any field empty") 


        # --------------- Check for incoming messages from threads  ---------------
        try:
            # get_nowait() will get exception when Queue is empty
            message = gui_queue.get_nowait()
        except queue.Empty:
            # break from the loop if no more messages are queued up             
            message = None              

        # if message received from queue, display the message in the Window
        if message:
            print('<<<Message>>>: ', message)

    # if user exits the window, then close the window and exit the GUI func
    gui.window.Close()