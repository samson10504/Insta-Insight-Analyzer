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
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


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
    options.add_argument('--no-sandbox')
    if headless == "True":
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("window-size=1920,1080")

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
            print("Cookies loaded")
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
        
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "input[name='username']")))
        
        username_field = (driver.find_element(By.CSS_SELECTOR, "input[name='username']"))
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

        save_config(config)
        save_cookies(driver)
        
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(text(),'Not Now')]")))

        # close notification box
        driver.find_element(By.XPATH, "//button[contains(text(),'Not Now')]").click()
        time.sleep(2)
    else:
        load_cookies(driver)

def save_config(config):
    """Saves the updated configuration to the configuration file."""
    with open('config.ini', 'w') as configfile:
        print("Config saved")
        config.write(configfile)


def get_insights(driver, link):
    """Navigates to the target link and extracts the insights data."""

    driver.get(link)

    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@role='button' and text()='View Insights']")))
    
    insight_element = driver.find_element(By.XPATH, "//div[@role='button' and text()='View Insights']")
    insight_element.click()
    

    # wait the insight layout to be loaded
    
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@data-bloks-name='bk.components.Collection']")))
        time.sleep(2)   
    except Exception as e:
        print("Button click timeout")
    
    try:
        # insight_info = driver.find_element(By.CSS_SELECTOR, ".x71s49j")
        xpath = '//div[@data-bloks-name="bk.components.Flexbox" and @class="wbloks_1" and contains(@style, "pointer-events: none; width: 100%; height: 100%; flex-direction: column;")]'
        insight_info = driver.find_elements(By.XPATH, xpath)

        return insight_info
    except Exception as e:
        print("CSS selector not found",str(e)) # print("An exception occurred:", str(e))
        return None

# def save_debug_info(all, soup, results, link):
def save_debug_info(insight_info, link):
    """Saves the insights data and HTML/CSS source to files for debugging purposes."""
    hk_timezone = pytz.timezone('Asia/Hong_Kong')
    current_datetime = datetime.now(hk_timezone)
    formatted_date = current_datetime.strftime("%Y-%m-%d")
    formatted_time = current_datetime.strftime("%H-%M-%S")

    # Extract unique_id from the link
    unique_id = link.split("/")[-2]

    # Define the directory path
    directory = 'log'
    subdirectory = f"log/{unique_id}"
    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    if not os.path.exists(subdirectory):
        os.makedirs(subdirectory)
    
    # file_path_css = os.path.join(subdirectory, "css", f"{unique_id}_{formatted_date}_{formatted_time}_css.txt")
    # file_path_html = os.path.join(subdirectory, "html", f"{unique_id}_{formatted_date}_{formatted_time}_html.txt")
    # file_path_bs = os.path.join(subdirectory, "bs4", f"{unique_id}_{formatted_date}_{formatted_time}_bs4.txt")
    
    file_path = os.path.join(subdirectory, f"{unique_id}_{formatted_date}_{formatted_time}.txt")
    # for path in [os.path.dirname(file_path_css), os.path.dirname(file_path_html), os.path.dirname(file_path_bs)]:
    for path in [os.path.dirname(file_path)]:
        if not os.path.exists(path):
            os.makedirs(path)

    print("Link:",link)
    try:
        with open(file_path, 'w') as file:
            for result in insight_info:
                text = result.text
                file.write(text + '\n')
        print("Unique ID:",unique_id,'Info saved')

    except Exception as e:
        print(f"Error saving BS4 results to '{file_path}'.")
        print(str(e)) 

def save_cookies(driver):
    """Saves the current cookies to the 'cookies.pkl' file."""
    try:
        pickle.dump(driver.get_cookies(), open("cookies.pkl", "wb"))
        print("Cookies saved")
    except:
        print("Error saving cookies to 'cookies.pkl'.")


def main():
    """Runs the main program."""
    driver = setup_driver()

    login(driver)

    config = read_config()

    links = config.get('links', 'target_links').split('\n')[1:]
    for link in links:
        if get_insights(driver, link) != None:
            insight_info = get_insights(driver, link)
            save_debug_info(insight_info, link)

    driver.quit()


if __name__ == "__main__":
    main()