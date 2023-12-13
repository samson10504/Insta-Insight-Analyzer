import configparser
import os
import pickle
import time
from datetime import datetime

import pytz
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By


def read_config():
    """Reads the configuration file and returns a ConfigParser object."""
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config


def setup_driver():
    """Sets up the Chrome driver with the options specified in the configuration file."""
    config = read_config()
    headless = config.get('main', 'headless')
    options = ChromeOptions()
    if headless == "True":
        options.add_argument("--headless")
    PATH = config.get('main', 'PATH')
    driver = webdriver.Chrome(PATH,options=options)
    return driver


def load_cookies(driver):
    """Loads the saved cookies from the 'cookies.pkl' file."""
    driver.get("https://www.instagram.com/")
    if os.path.exists("cookies.pkl"):
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                driver.add_cookie(cookie)
        except:
            print("Error loading cookies from 'cookies.pkl'.")


def login(driver):
    """Logs in to Instagram using the credentials specified in the configuration file."""
    config = read_config()
    Islogin = config.get('main', 'Islogin')
    save_info = config.get('main', 'save_info')

    if Islogin == "False":
        # TODO: Delete cookies to ensure a fresh login
        
        driver.get("https://www.instagram.com/")
        time.sleep(5)

        username_field = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
        password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")

        username_field.clear()
        password_field.clear()
        
        username_field.send_keys(config.get('main', 'username')) 
        password_field.send_keys(config.get('main', 'password'))

        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()

        time.sleep(5)
        
        # TODO: some problem here
        if save_info == "True":
            save_info_button = driver.find_element(By.XPATH, "//button[contains(text(),'Save info')]")
        else:
            save_info_button = driver.find_element(By.XPATH, "//div[@role='button' and text()='Not now']")

        save_info_button.click()
        config.set('main', 'Islogin', 'True')


def save_config(config):
    """Saves the updated configuration to the configuration file."""
    with open('config.ini', 'w') as configfile:
        print("Config saved")
        config.write(configfile)


def get_insights(driver):
    """Navigates to the target link and extracts the insights data."""
    config = read_config()
    driver.get(config.get('main', 'target_link'))
    time.sleep(5)

    insight_element = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/section[1]/div/section/div")
    insight_element.click()

    time.sleep(5)

    all = driver.find_element(By.CSS_SELECTOR, ".x71s49j")
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    results = soup.find_all(attrs={'data-block-name': 'bk.components.Flexbox'})

    return all, soup, results


def save_debug_info(all, soup, results):
    """Saves the insights data and HTML/CSS source to files for debugging purposes."""
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

    try:
        with open(file_path_css, 'w') as f:
            all_text = all.text
            f.write(all_text)
    except:
        print(f"Error saving CSS to '{file_path_css}'.")

    try:
        with open(file_path_html, 'w') as f:
            f.write(soup.prettify())
    except:
        print(f"Error saving HTML to '{file_path_html}'.")

    try:
        with open(file_path_bs, 'w') as file:
            for result in results:
                text = result.get_text()
                file.write(text + '\n')
    except:
        print(f"Error saving BS4 results to '{file_path_bs}'.")


def save_cookies(driver):
    """Saves the current cookies to the 'cookies.pkl' file."""
    try:
        pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
    except:
        print("Error saving cookies to 'cookies.pkl'.")


def main():
    """Runs the main program."""
    driver = setup_driver()
    load_cookies(driver)

    login(driver)

    all, soup, results = get_insights(driver)

    save_debug_info(all, soup, results)

    save_cookies(driver)
    save_config(read_config())

    driver.quit()


if __name__ == "__main__":
    main()