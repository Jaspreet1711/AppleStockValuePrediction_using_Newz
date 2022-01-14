# -*- coding: utf-8 -*-
"""
Created on Fri Dec 31 11:00:29 2021

@author: Jaspreet Singh
"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
import pandas as pd
import time
from datetime import datetime as dt

ignored_exceptions = (NoSuchElementException,StaleElementReferenceException)

path = 'C:/Users/Jaspreet Singh/Desktop/ISB/3. Term- 2/Foundation Project Data Science/Web Scraper/chromedriver.exe'
driver = webdriver.Chrome(path)
driver.get("https://www.investing.com/equities/apple-computer-inc-news/1")

action = webdriver.ActionChains(driver)

time.sleep(2)

# Input
Pages_to_scrape = 1300

# Output
Dt = []
Newz_Headline = []
Newz_Brief = []
Source = []

# Closing the Pop up and Ad
try:
    close_loc = driver.find_element_by_css_selector("a[class='bugCloseIcon']")
    close_loc.click()
except:
    pass
try:
    close_ad = WebDriverWait(driver, 2, ignored_exceptions=ignored_exceptions).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "i[class='popupCloseIcon largeBannerCloser']"))
        )
    close_ad.click()
except:
    pass
    

# Starting Scraping
n = 0

for i in range( 0, Pages_to_scrape):
    
    n += 1
    
    pagi_tray = WebDriverWait(driver, 5, ignored_exceptions=ignored_exceptions).until(
        EC.presence_of_element_located((By.ID, "paginationWrap"))
        )
    next_button = pagi_tray.find_element_by_css_selector("div[class='sideDiv inlineblock text_align_lang_base_2']")
    if n > 1:
        next_button.click()
    else:
        pass
    
    # Closing the ad, other notifications, etc
    try:
        close_ad = WebDriverWait(driver, 0.25, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "i[class='popupCloseIcon largeBannerCloser']"))
            )
        close_ad.click()
    except:
        pass
    
    try:
        Notification_popup = driver.find_element_by_css_selector("div[class='allow-notifications-popup-button-line']")
        Notification_later = Notification_popup.find_element_by_css_selector("button[class='allow-notifications-popup-button later']")
        Notification_later.click()
    except:
        pass
    
    # Collecting data from the page
    try:
        Newz_Section = WebDriverWait(driver, 2, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='mediumTitle1']"))
            )
    except:
        # Sometimes page crashes. It will refersh twice to ensure content comebacks again.
        print("Page_Crashed_Refreshing_it")
        driver.refresh()
        time.sleep(2)
        driver.refresh()
        time.sleep(2)
        try:
            close_ad = WebDriverWait(driver, 2, ignored_exceptions=ignored_exceptions).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "i[class='popupCloseIcon largeBannerCloser']"))
                )
            close_ad.click()
        except:
            pass
        Newz_Section = WebDriverWait(driver, 2, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='mediumTitle1']"))
            )
        
    Articles = Newz_Section.find_elements_by_tag_name("article")
    
    for article in Articles:
        Text_Section = article.find_element_by_css_selector("div[class='textDiv']")
        # Extracting Newz Heading
        a_ls = Text_Section.find_elements_by_tag_name("a")
        Headline_ele = a_ls[0]
        Newz_Headline.append(Headline_ele.text)
        # Extracting Newz Source
        span_ls = Text_Section.find_elements_by_tag_name("span")
        Source_text = span_ls[0].text.split(' ')[1]
        Source.append(Source_text)
        # Extracting Newz Date
        Dt_txt = span_ls[0].text.split('- ')
        try:
            Date_txt = Dt_txt[1].replace(',', '').split(' ')
            Date_text = Date_txt[1] + ' ' + Date_txt[0] + ' ' + Date_txt[2]
        except:
            try:
                Date_text = Dt_txt[1]
            except:
                Date_text = 'NA'
        Dt.append(Date_text)
        # Extracting Newz Brief
        Brief_ele = article.find_element_by_tag_name("p")
        Brief = Brief_ele.text
        Newz_Brief.append(Brief)
        
    # Closing the ad and newz video popup if it pops up in last.
    try:
        close_ad = WebDriverWait(driver, 0.15, ignored_exceptions=ignored_exceptions).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "i[class='popupCloseIcon largeBannerCloser']"))
            )
        close_ad.click()
    except:
        pass
    
    print('Scraping Progress: ' + str(n) + ' / ' + str(Pages_to_scrape))
    
# Arranging Data Set in Dataframe    
Output_DF = pd.DataFrame(
    {'Date': Dt,
     'Newz_Headline': Newz_Headline,
     'Newz_Brief': Newz_Brief,
     'Source': Source
    })

Output_DF.to_csv('AAPL_Newz_Data.csv', index = False)




