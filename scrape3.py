import configparser
import os
import pickle
import time
from datetime import datetime
import pytz
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


def read_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def setup_driver(config):
    PATH = config.get('main', 'PATH')
    driver = webdriver.Chrome(PATH)
    return driver


def load_cookies(driver):
    driver.get("https://www.instagram.com/")
    if os.path.exists("cookies.pkl"):
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
    else:
        print("The file 'cookies.pkl' does not exist.")


def login(driver, config, Islogin, save_info):
    if not Islogin:
        driver.get("https://www.instagram.com/")
        time.sleep(5)

        username_field = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
        password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")

        username_field.clear()
        username_field.send_keys(config.get('main', 'username'))
        password_field.clear()
        password_field.send_keys(config.get('main', 'password'))

        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()

        time.sleep(5)

        if save_info:
            save_info_button = driver.find_element(By.XPATH, "//[text()='Save info']")
        else:
            save_info_button = driver.find_element(By.XPATH, "//[text()='Not now']")

        save_info_button.click()
        config.set('main', 'Islogin', 'True')


def save_config(config):
    with open('config.ini', 'w') as configfile:
        print("Config saved")
        config.write(configfile)


def get_insights(driver, config):
    driver.get(config.get('main', 'target_link'))
    time.sleep(5)

    insight_element = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/section[1]/div/section/div")
    insight_element.click()

    time.sleep(5)

    all = driver.find_element(By.CSS_SELECTOR, ".x71s49j")
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    results = soup.find_all(attrs={'data-bloks-name': 'bk.components.Flexbox'})

    return all, soup, results


def save_debug_info(all, soup, results):
    hk_timezone = pytz.timezone('Asia/Hong_Kong')
    current_datetime = datetime.now(hk_timezone)
    formatted_date = current_datetime.strftime("%Y-%m-%d")
    formatted_time = current_datetime.strftime("%H-%M-%S")

    directory = "log"
    if not os.path.exists(directory):
        os.makedirs(directory)

    file_path_css = os.path.join(directory, "css", f"{formatted_date}_{formatted_time}_css.txt")
    file_path_html = os.path.join(directory, "html", f"{formatted_date}_{formatted_time}_html.txt")
    file_path_bs = os.path.join(directory, "bs4", f"{formatted_date}_{formatted_time}_bs4.txt")

    for path in [os.path.dirname(file_path_css), os.path.dirname(file_path_html), os.path.dirname(file_path_bs)]:
        if not os.path.exists(path):
            os.makedirs(path)

    with open(file_path_css, 'w') as f:
        all_text = all.text
        f.write(all_text)

    with open(file_path_html, 'w') as f:
        f.write(soup.prettify())

    with open(file_path_bs, 'w', encoding='utf-8') as file:
        for result in results:
            text = result.get_text()
            file.write(text + '\n')


def save_cookies(driver):
    pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))


def main():
    config = read_config()
    Islogin = bool(config.get('main', 'Islogin'))
    save_info = bool(config.get('main', 'save_info'))

    driver = setup_driver(config)
    load_cookies(driver)

    login(driver, config, Islogin, save_info)

    all, soup, results = get_insights(driver, config)

    save_debug_info(all, soup, results)

    save_cookies(driver)
    save_config(config)

    driver.quit()


if __name__ == "__main__":
    main()