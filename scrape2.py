import configparser
import os
import pickle
import time
from datetime import datetime
import pytz
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# Read config
config = configparser.ConfigParser()
config.read('config.ini')
Islogin = bool(config.get('main', 'Islogin'))
save_info = bool(config.get('main', 'save_info'))


target_link = config.get('main', 'target_link')
username = config.get('main', 'username')
password = config.get('main', 'password')


# Set up driver
PATH = config.get('main', 'PATH')
driver = webdriver.Chrome(PATH)


driver.get("https://www.instagram.com/")

# Load cookies
if os.path.exists("cookies.pkl"):
    cookies = pickle.load(open("cookies.pkl", "rb"))
    for cookie in cookies:
        driver.add_cookie(cookie)
else:
    print("The file 'cookies.pkl' does not exist.")

def login(Islogin,save_info): # only exceute for first time login    
    if Islogin == False: 
        # Wait for page to load
        time.sleep(5)
        
        # Find username and password fields
        username_field = driver.find_element(By.CSS_SELECTOR, "input[name='username']")
        password_field = driver.find_element(By.CSS_SELECTOR, "input[name='password']")
        
        # Clear fields and enter your credentials
        username_field.clear()
        username_field.send_keys(username)
        password_field.clear()
        password_field.send_keys(password)
        
        # Click on the login button
        login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()

        time.sleep(5)
        if not Islogin: # Only do for first time login
            if save_info == True: # First login + Choose to save info
                save_info_button = driver.find_element(By.XPATH, "//[text()='Save info']")
                save_info_button.click()
            elif save_info == False: # First login + Choose not to save info
                save_info_button = driver.find_element(By.XPATH, "//[text()='Not now']")
                save_info_button.click()    

        config.set('main', 'Islogin', 'True') #change IsLogin to True

login(Islogin=Islogin,save_info=save_info)

link = target_link
driver.get(link)
# driver.implicitly_wait(5)
time.sleep(5)

# Click View insights
# insight_element = driver.find_element(By.XPATH, "//[text()='View Insights']")
insight_element = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/section[1]/div/section/div")
insight_element.click()

# Wait for insights to load
time.sleep(5)

all = driver.find_element(By.CSS_SELECTOR, ".x71s49j")

# Get the page source after the JavaScript has executed 
page_source = driver.page_source 
 
# Use BeautifulSoup to parse the HTML 
soup = BeautifulSoup(page_source, 'html.parser') 
results = soup.find_all(attrs={'data-bloks-name': 'bk.components.Flexbox'})

# ---------------------- Debug ----------------------
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

# Create the subdirectories if they don't exist
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

# ---------------------- Debug ----------------------
# Save cookies
pickle.dump(driver.get_cookies() , open("cookies.pkl","wb"))

# Save config
with open('config.ini', 'w') as configfile:
  print("Config saved")
  config.write(configfile)

# Quit the driver
driver.quit()