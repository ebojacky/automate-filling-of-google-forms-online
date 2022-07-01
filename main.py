import time

import bs4
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import requests

URL_GOOGLE_FORM = "https://docs.google.com/forms/d/e/1FAIpQLSeNCdphKKoxSGeycPSmGym-jen2KBd0jasQVpsjiQCxW0gAow/" \
                  "viewform?vc=0&c=0&w=1&flr=0"

URL_RENT = "https://www.zillow.com/homes/for_rent/"


# SCRAP DATA FROM RENTAL SITE
header = {
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
}
response = requests.get(url=URL_RENT, headers=header)
soup = bs4.BeautifulSoup(response.text, "html.parser")

addresses = [item.text for item in soup.select(".list-card-info a address")]
prices = [item.text for item in soup.select(".list-card-info .list-card-heading .list-card-price")]
links = [item["href"] for item in soup.select(".list-card-info a")]

for i in range(0, len(links)):
    if links[i][0:5:] == "https":
        pass
    else:
        links[i] = "https://www.zillow.com/homedetails/" + links[i]


# FILL GOOGLE FORMS WITH DATA

chrome_path = "chromedriver_win32/chromedriver.exe"
chrome_service = Service(chrome_path)
browser = webdriver.Chrome(service=chrome_service)

for i in range(len(addresses)):
    browser.get(URL_GOOGLE_FORM)
    time.sleep(5)

    inp = browser.find_elements(by=By.CSS_SELECTOR, value='input[type="text"]')
    inp[0].send_keys(addresses[i])
    inp[1].send_keys(prices[i])
    inp[2].send_keys(links[i])

    time.sleep(2)

    btn = browser.find_element(by=By.CSS_SELECTOR, value='div[role="button"]')
    btn.click()
