from selenium import webdriver  
import time  
import json
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
from create_event import create_event

LOCATION_FILE = 'locations.json'


# def parse_datetime(datestring):
    


def get_data(element):
    card = element.find_element(By.ID, "league-detail-view")
    #prices = card.find_element(By.CLASS_NAME, "entry-fees")
    #price = prices.find_element(By.CLASS_NAME, "data-value").get_attribute("innerHTML")
    #division = prices.find_element(By.CLASS_NAME, "data-label").get_attribute("innerHTML")
    name = card.find_element(By.CLASS_NAME, "event-header").get_attribute("innerHTML")
    when = card.find_element(By.CLASS_NAME, "when").get_attribute("innerHTML")
    location = card.find_element(By.CLASS_NAME, "locality").get_attribute("innerHTML")
    address = card.find_element(By.CLASS_NAME, "address").get_attribute("innerHTML")

    print(name)
    print(when)
    print(location)
    print(address, "\n")
    #print(division, price, "\n")

    # description = division + ":" + price + "\n" + location + "\n" + address

    # create_event()


def open_location(driver, location, country):
    driver.get("https://events.pokemon.com/en-us/events?near=" + location)  
    time.sleep(3)  

    data = driver.find_elements(By.CLASS_NAME, "card-holder")

    for i in range(len(data)):
        element = driver.find_elements(By.CLASS_NAME, "card-holder")[i]
        if 'FI' not in element.find_element(By.CLASS_NAME, 'location').get_attribute('innerHTML')[-5:]:
            continue
        time.sleep(1)
        element.click()
        time.sleep(2)
        #part = driver.find_element(By.CLASS_NAME, "league-detail-view")
        get_data(driver)
        time.sleep(1)
        driver.find_element(By.CLASS_NAME, "back-button").click()



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