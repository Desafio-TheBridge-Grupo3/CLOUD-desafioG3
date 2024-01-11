from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import time
from os import environ

URL = environ.get("URL_CANDELA")
USER = environ.get("USER_CANDELA")
PASSWORD = environ.get("PASSWORD_CANDELA")
CUPS = environ.get("JAVI_CUPS")

def get_soup_info(driver):
    candela_info = {
        "rate": [],
        "anual_consumption": [],
        "anual_consumption_p1": [],
        "anual_consumption_p2": [],
        "anual_consumption_p3": [],
        "anual_consumption_p4": [],
        "anual_consumption_p5": [],
        "anual_consumption_p6": [],
        "anual_power_p1": [],
        "anual_power_p2": [],
        "anual_power_p3": [],
        "anual_power_p4": [],
        "anual_power_p5": [],
        "anual_power_p6": []
    }

    candela_info["rate"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[9]').text
    candela_info["anual_consumption"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[11]').text
    candela_info["anual_consumption_p1"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[13]').text
    candela_info["anual_consumption_p2"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[14]').text
    candela_info["anual_consumption_p3"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[15]').text
    candela_info["anual_consumption_p4"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[16]').text
    candela_info["anual_consumption_p5"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[17]').text
    candela_info["anual_consumption_p6"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[18]').text
    candela_info["anual_power_p1"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[21]').text
    candela_info["anual_power_p2"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[22]').text
    candela_info["anual_power_p3"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[23]').text
    candela_info["anual_power_p4"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[24]').text
    candela_info["anual_power_p5"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[25]').text
    candela_info["anual_power_p6"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[26]').text

    return candela_info


def get_candelas_chrome_info(driver):
    candela_info = {
        "rate": [],
        "anual_consumption": [],
        "anual_consumption_p1": [],
        "anual_consumption_p2": [],
        "anual_consumption_p3": [],
        "anual_consumption_p4": [],
        "anual_consumption_p5": [],
        "anual_consumption_p6": [],
        "anual_power_p1": [],
        "anual_power_p2": [],
        "anual_power_p3": [],
        "anual_power_p4": [],
        "anual_power_p5": [],
        "anual_power_p6": []
    }

    candela_info["rate"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[9]').text
    candela_info["anual_consumption"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[11]').text
    candela_info["anual_consumption_p1"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[13]').text
    candela_info["anual_consumption_p2"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[14]').text
    candela_info["anual_consumption_p3"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[15]').text
    candela_info["anual_consumption_p4"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[16]').text
    candela_info["anual_consumption_p5"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[17]').text
    candela_info["anual_consumption_p6"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[18]').text
    candela_info["anual_power_p1"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[21]').text
    candela_info["anual_power_p2"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[22]').text
    candela_info["anual_power_p3"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[23]').text
    candela_info["anual_power_p4"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[24]').text
    candela_info["anual_power_p5"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[25]').text
    candela_info["anual_power_p6"] = driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-table-container/table/tbody/tr[2]/td[26]').text

    return candela_info

def webscraping_chrome_candelas(cups):
    
    # Create driver Chrome
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")

    servicio = Service('/usr/local/bin/chromedriver')
    driver = webdriver.Chrome(service=servicio, options=chrome_options)
    driver.get(URL)
    assert "Candela"
    time.sleep(5)

    # Login in candelas web

    driver.find_element(By.ID, "select_1").click()
    time.sleep(1)
    driver.find_element(By.ID, "select_option_3").click()
    driver.find_element(By.NAME, "usuario").send_keys(USER)
    driver.find_element(By.NAME, "password").send_keys(PASSWORD)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/form/button').click()
    time.sleep(3)

    # Download info

    driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[1]/ul/li[3]/a').click()
    time.sleep(1)
    driver.find_element(By.ID, "input_6").send_keys(cups)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-card/div[1]/form/div[4]/button').click()
    time.sleep(10)
    driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[2]/md-tabs/md-tabs-content-wrapper/md-tab-content/div[1]/md-content/md-card/md-toolbar/div[1]/button[1]').click()

    info = get_soup_info(driver)

    # Close driver
    driver.quit()

    return info

a = webscraping_chrome_candelas(CUPS)

print(a)