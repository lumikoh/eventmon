from selenium import webdriver  
import time  
import json
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from create_event import create_event

LOCATION_FILE = 'config.json'


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
    ...


def get_data(element):
    card = get_elements_wait(element, By.ID, "league-detail-view")
    if card is None:
        return
    #prices = card.find_element(By.CLASS_NAME, "entry-fees")
    #price = prices.find_element(By.CLASS_NAME, "data-value").get_attribute("innerHTML")
    #division = prices.find_element(By.CLASS_NAME, "data-label").get_attribute("innerHTML")
    name = get_attribute_safe(card[0],By.CLASS_NAME, "event-header","innerHTML")
    when = get_attribute_safe(card[0],By.CLASS_NAME, "when","innerHTML")
    location = get_attribute_safe(card[0],By.CLASS_NAME, "locality","innerHTML")
    address = get_attribute_safe(card[0],By.CLASS_NAME, "address","innerHTML")

    print(name)
    print(when)
    print(location)
    print(address, "\n")
    #print(division, price, "\n")

    # description = division + ":" + price + "\n" + location + "\n" + address

    # create_event()


def open_location(driver, location, country):
    driver.get("https://events.pokemon.com/en-us/events?near=" + location)  

    data = get_elements_wait(driver, By.CLASS_NAME, "card-holder")

    if data is None:
        return

    print(len(data))

    for i in range(len(data)):
        list = get_elements_wait(driver, By.CLASS_NAME, "card-holder")
        if len(list) < i+1:
            break
        element = list[i]
        if country not in element.find_element(By.CLASS_NAME, 'location').get_attribute('innerHTML')[-5:]:
            continue
        element.click()
        get_data(driver)
        driver.find_element(By.CLASS_NAME, "back-button").click()
        time.sleep(1)



def main():
    driver = webdriver.Firefox()  

    data = open(LOCATION_FILE)
    json_data = json.load(data)

    country = json_data["Country"]
    for location in json_data["Locations"]:
        open_location(driver, location, country)

    driver.close()  


if __name__ == "__main__":
    main()