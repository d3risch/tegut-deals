import os
import sys
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import TimeoutException


if __name__ == "__main__":
    # Default to Frankfurt if no zip code was given.
    plz = "60306"
    if len(sys.argv) > 1:
        plz = sys.argv[1]
    assert len(plz) == 5 and plz.isdigit()

    # Basic Chrome setup to run in headless mode.
    service = Service('/usr/local/share/chrome_driver/chromedriver')

    service.start()
    chrome_options = Options()
    options = [
        "--headless",
        "--disable-gpu",
        "--window-size=1920,1200",
        "--ignore-certificate-errors",
        "--disable-extensions",
        "--no-sandbox",
        "--disable-dev-shm-usage"
    ]
    for option in options:
        chrome_options.add_argument(option)
    
    with webdriver.Chrome(service=service, options=chrome_options) as driver:
        # Load initial website.
        driver.get("https://www.tegut.com/angebote-produkte/angebote.html")

        # Wait until cookie banner has loaded.
        cookieBtn = WebDriverWait(driver, 4).until(expected_conditions.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
        cookieBtn.click()

        # Input zip code into respective form.
        plzInput = WebDriverWait(driver, 4).until(expected_conditions.element_to_be_clickable((By.ID, 'adressInput')))
        plzInput.send_keys(plz)

        # Click submit button.
        submitButton = driver.find_element(By.NAME, 'mktegut[submit]')
        submitButton.click()

        # Wait until list of supermarkets has loaded and click first one.
        try:
            firstMarketInList = WebDriverWait(driver, 4).until(expected_conditions.element_to_be_clickable((By.XPATH, '/html/body/main/article/div/div/div/div[3]/div/div/div[2]/div/div/div[1]/ul/li[1]/a')))
            firstMarketInList.click()
        except TimeoutException as ex:
            print("There are no Tegut stores near the given plz.")
            driver.close()
            sys.exit()

        # Wait for deals buttons to be visible and click all of them. Opens new tabs.
        WebDriverWait(driver, 4).until(expected_conditions.visibility_of_element_located((By.XPATH, "//a[@class='button trackEvent']")))

        elems = driver.find_elements(By.XPATH, "//a[@class='button trackEvent']")
        for elem in elems:
            elem.click()

        # Wait for downloads to finish or break if 20 seconds have passed.
        download = True
        seconds = 20
        while seconds >= 0 and download:
            time.sleep(1)
            download = False
            files = os.listdir('.')
            for fname in files:
                if fname.endswith('.crdownload'):
                    download = True 
