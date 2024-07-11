from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(url="http://orteil.dashnet.org/experiments/cookie/ ")

cookie = driver.find_element(By.ID, value="cookie")
p = driver.find_elements(By.CSS_SELECTOR, value="#store div")
ids = [i.get_attribute("id") for i in p]

timeout = time.time() + 5
t_time = timeout + 60 * 5

while True:
    cookie.click()

    if time.time() > timeout:
        p_prices = driver.find_elements(by=By.CSS_SELECTOR, value="#store div b")
        item_prices = []
        for item in p_prices:
            data = item.text
            if data != "":
                item_prices.append(int(data.split("-")[1].strip().replace(",", "")))

        dict_items = {}
        for i in range(len(item_prices)):
            dict_items[item_prices[i]] = ids[i]

        money = driver.find_element(by=By.ID, value="money")
        cookie_count = money.text
        cookie_count = int(cookie_count.replace(",",""))
        affordable_upgrades = {}
        for cost, id in dict_items.items():
            if cost < cookie_count:
                affordable_upgrades[cost] = id
        most_expensive_id = dict_items[max(affordable_upgrades)]
        driver.find_element(by=By.ID,value=most_expensive_id).click()
        timeout = time.time()+5

    if time.time() > t_time:
        cookies_per_sec = driver.find_element(by=By.ID, value="cps").text
        print(cookies_per_sec)
        break

driver.quit()
