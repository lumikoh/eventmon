from selenium import webdriver  
import time  
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from datetime import datetime, timedelta
from create_event import create_event
from datetime_parser import string_to_datetime

LOCATION_FILE = 'config.json'
CREATED_FILE = 'created.json'


# def parse_datetime(datestring):
    
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


def add_created(name,date,address):
    with open(CREATED_FILE, 'r+') as file:
        eventstring =  f"{str(date)}" + "|" + f"{name:<10}"[:10] + "|" + f"{address:<10}"[:10]
        
        json_data = json.load(file)

        if eventstring in json_data["created"]:
            return False

        json_data["created"].append(eventstring)

        file.seek(0)
        json.dump(json_data, file, indent=4)
        return True

def get_data(element):
    card = get_elements_wait(element, By.ID, "league-detail-view")
    if card is None:
        return
    
    time.sleep(1)
    #prices = card.find_element(By.CLASS_NAME, "entry-fees")
    #price = prices.find_element(By.CLASS_NAME, "data-value").get_attribute("innerHTML")
    #division = prices.find_element(By.CLASS_NAME, "data-label").get_attribute("innerHTML")
    name = get_attribute_safe(card[0],By.CLASS_NAME, "event-header","innerHTML")
    when = get_attribute_safe(card[0],By.CLASS_NAME, "when","innerHTML")
    location = get_attribute_safe(card[0],By.CLASS_NAME, "locality","innerHTML")
    address = get_attribute_safe(card[0],By.CLASS_NAME, "address","innerHTML")
    website = get_website(card[0])

    date = string_to_datetime(when)

    description = location + "\n" + address + "\n" + website

    if add_created(name,date,address):
        create_event(name, description, date, date)


def open_location(driver, location, country):
    driver.get("https://events.pokemon.com/en-us/events?near=" + location)  

    data = get_elements_wait(driver, By.CLASS_NAME, "card-holder")

    if data is None:
        return

    for i in range(len(data)):
        list = get_elements_wait(driver, By.CLASS_NAME, "card-holder")
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



def main():

    options = Options()
    options.add_argument('--headless')
    driver = webdriver.Firefox(options=options)  

    data = open(LOCATION_FILE)
    json_data = json.load(data)

    country = json_data["Country"]
    for location in json_data["Locations"]:
        open_location(driver, location, country)

    driver.close()  


if __name__ == "__main__":
    main()