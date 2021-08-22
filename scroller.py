from selenium import webdriver
import time
import id_scraper


def chrome_driver():
    CHROME_PATH = "C:\Program Files (x86)\chromedriver.exe"
    return webdriver.Chrome(CHROME_PATH)

def firefox_driver():
    FIREFOX_PATH = "C:\Program Files (x86)\geckodriver.exe"
    return webdriver.Firefox(FIREFOX_PATH)

def scroll():
    driver = chrome_driver()
    driver.get("https://tenor.com/users/isail")


    for i in range(20):
        print("SCROLLING")
        scroll_amount = str(400 * i)
        driver.execute_script("window.scroll(0,"+ scroll_amount + ")")
        print("SLEEPING")
        time.sleep(2)
        print("WRITING")
        with open('page.html', 'w') as f:
            f.write(driver.execute_script("return document.body.innerHTML;"))

        id_scraper.get_ids()
        print(i)



    driver.close()

