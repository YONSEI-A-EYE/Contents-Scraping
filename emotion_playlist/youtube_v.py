import pandas as pd
import html as h
import json
import time
import pickle
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service


df = pd.read_csv('theme_title_artist.csv', encoding='cp949')
search = list(df.iloc[:,1])
file_path_csv = 'theme_title_artist_url.csv'

url_list = []

for i in range(len(search)):        
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    time.sleep(1.5)
    try : 
        url = ('https://www.youtube.com/results?search_query={}'.format(search[i]))
        driver.get(url)
        soup = bs(driver.page_source, 'lxml')
        title = soup.select('a#video-title')
        url_list.append(str(title[0].get('href')).split('v=')[1])
    except : 
        url_list.append('error')

# Save data_dict
with open('v_list.pkl','wb') as f:
    pickle.dump(url_list,f)

