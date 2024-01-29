#import requests
import os
#from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time

def download_data():
    link = 'https://www.codot.gov/safety/traffic-safety/data-analysis/crash-data'

    # Set up Chrome options
    options = webdriver.ChromeOptions() 
    # with an abolute path the download worked!
    prefs = {"download.default_directory" : "C:\\Users\\menam\\boulder_code\\personal_projects\\accident_tracker\\data"}
    #example: prefs = {"download.default_directory" : "C:\Tutorial\down"};
    options.add_experimental_option("prefs",prefs)

    # init our webdriver with our options
    driver = webdriver.Chrome(options=options)
    #driver = webdriver.Chrome(options=chrome_options)
    driver.get(link)
    # update the website so we can see the data files
    driver.find_element(By.CSS_SELECTOR, '.fas.fa-caret-down').click()

    # click the file to be redirected
    links = driver.find_elements(By.CLASS_NAME, 'col-sm-2')

    # iterate trhough all redirect links and click to download
    #for link in links:
        #link.send_keys(Keys.CONTROL +"t")
        # Simulate Ctrl+click to open the link in a new tab
    for i in range(len(links)):
        ActionChains(driver).key_down(Keys.CONTROL).click(links[i]).key_up(Keys.CONTROL).perform()

        time.sleep(12)

    driver.quit()

class WebScraper:
    url = ''
    driver= None


    def __init__(self, link):
        self.url = link
        self.driver = webdriver.Chrome()
        #self.soup = self.parse_content(self.response)

    def make_request(self, url):
        return self.driver.get(url)
        

    #def parse_content(self, response, parser = 'html.parser'):
        #return BeautifulSoup(response.content, parser)

    # # Function to download Excel files from URLs into a folder
    # def download_excel_files(self, links, years, folder):
    #     # Create the folder if it doesn't exist
    #     os.makedirs(folder, exist_ok=True)
        
    #     for link, year in zip(links, years):
    #         response = requests.get(link)
    #         if response.status_code == 200:
    #             # Determine the filename from the URL
    #             #filename = os.path.join(folder, link.split('/')[-1])
    #             with open(folder + '/' + year + '.xlsx', 'wb') as f:
    #                 f.write(response.content)
    #                 #print(f"File '{filename}' downloaded successfully.")



