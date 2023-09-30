from selenium import webdriver  
import time  
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from create_event import create_event
from datetime_parser import string_to_datetime
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from datetime import datetime
import os

LOCATION_FILE = 'config.json'

types = [
        "&filters=league_cup",
        "&filters=league_challenge",
        "&filters=prerelease",
        "&filters=premier_challenge",
        "&filters=midseason_showdown",
        "&filters=league"
]
    
def get_elements_wait(element, selector, property):
    for i in range(10):
        parts = element.find_elements(selector, property)
        if(len(parts) == 0):
            time.sleep(1)
            continue
        return parts
    return None
        

def get_attribute_safe(element, selector, property, attribute):
    parts = element.find_elements(selector, property)
    if(len(parts) == 0):
        return ""
    return parts[0].get_attribute(attribute)


def get_website(element):

    owner = element.find_elements(By.CLASS_NAME, "address-and-owner")

    if len(owner) != 0:
        data_rows = owner[0].find_elements(By.CLASS_NAME, "data-row")
        for row in data_rows:
            label = get_attribute_safe(row, By.CLASS_NAME, "data-label", "innerHTML")
            if label == 'Website':
                link = get_attribute_safe(row, By.CLASS_NAME, 'data-value', 'innerHTML')
                if link != "":
                    return link
    
    playtimes = element.find_elements(By.CLASS_NAME, "event_playtimes")
    if len(playtimes) != 0:
        return get_attribute_safe(playtimes[0], By.TAG_NAME, 'a', 'href')
    return ""


def get_data(element):
    card = get_elements_wait(element, By.ID, "league-detail-view")
    if card is None:
        return
    
    time.sleep(1)
    name = get_attribute_safe(card[0],By.CLASS_NAME, "event-header","innerHTML")
    when = get_attribute_safe(card[0],By.CLASS_NAME, "when","innerHTML")
    location = get_attribute_safe(card[0],By.CLASS_NAME, "locality","innerHTML")
    address = get_attribute_safe(card[0],By.CLASS_NAME, "address","innerHTML")
    website = get_website(card[0])

    date = string_to_datetime(when)

    description = location + "\n" + address + "\n" + website

    try:
        create_event(name, description, date, date)
    except:
        print("Error: Something went wrong.")



def open_location(driver, location, country):
    driver.get("https://events.pokemon.com/en-us/" + location)  

    data = get_elements_wait(driver, By.CLASS_NAME, "card-holder")

    if data is None:
        return
    
    i = 0

    while True:
        list = get_elements_wait(driver, By.CLASS_NAME, "card-holder")
        time.sleep(1)

        if len(list) < i+1:
            break
        element = list[i]

        if country not in get_attribute_safe(element,By.CLASS_NAME, 'location', 'innerHTML')[-5:]:
            continue

        element.click()
        get_data(driver)
        time.sleep(0.5)
        button = get_elements_wait(driver,By.CLASS_NAME,"back-button")
        
        if len(button) == 0:
            break

        button[0].click()
        time.sleep(0.5)
        i += 1


def main():

    os.system("cls") # Change for Linux/MacOS

    print("\nCrawling Pokemon events.... ")

    start = datetime.now()

    options = Options()
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    
    #options.add_argument("no-sandbox")

    options.add_argument("start-maximized")
    options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36")
    driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)  

    data = open(LOCATION_FILE)
    json_data = json.load(data)

    country = json_data["country"]
    for location in json_data["locations"]:
        for type in types:
            open_location(driver, location+type, country)

    driver.close()  

    end = datetime.now()
    duration = start-end
    print(duration)


if __name__ == "__main__":
    main()