import os
import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


GOOGLE_FORM = os.environ.get("google_form")
ZILLOW_CLONE = "https://appbrewery.github.io/Zillow-Clone/"


response = requests.get(url=ZILLOW_CLONE)
website = response.text
soup = BeautifulSoup(website, "html.parser")

prices = [i.get_text().split('+' or '/')[0].split('/mo')[0] for i in soup.find_all( 'span', class_='PropertyCardWrapper__StyledPriceLine')]

links = list(set([i.get('href') for i in soup.find_all('a')]))
addresses = [i.getText().strip() for i in soup.find_all('address')]

chrome_settings = webdriver.ChromeOptions()
chrome_settings.add_experimental_option('detach',True)
driver = webdriver.Chrome(chrome_settings)

for i in range(len(prices)):
    driver.get(GOOGLE_FORM)
    time.sleep(2)
    address = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    address.send_keys(addresses[i])
    time.sleep(1)
    price = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price.send_keys(prices[i])
    time.sleep(1)
    link = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
    link.send_keys(links[i], Keys.TAB,Keys.ENTER)
    submit_another = driver.find_element(By.XPATH, value='/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    submit_another.click()
    time.sleep(1)

driver.quit()
