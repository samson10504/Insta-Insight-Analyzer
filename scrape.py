import configparser
import os
import pickle
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

# Read config
config = configparser.ConfigParser()
config.read('config.ini')
Islogin = bool(config.get('main', 'Islogin'))
save_info = bool(config.get('main', 'save_info'))


target_link = config.get('main', 'target_link')
username = config.get('main', 'username')
password = config.get('main', 'password')


# Set up driver
PATH = "/opt/homebrew/bin/chromedriver"
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


all = driver.find_element(By.CSS_SELECTOR, "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.xw2csxc.x1odjw0f.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div > div.wbloks_1.wbloks_77.wbloks_75")
print(all.text)

# # Get overview, reach, engagement, and profile visit elements
# overview = driver.find_element(By.CSS_SELECTOR, "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.xw2csxc.x1odjw0f.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div > div.wbloks_1.wbloks_78.wbloks_76 > div:nth-child(6)")
# reach = driver.find_element(By.CSS_SELECTOR, "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.xw2csxc.x1odjw0f.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div > div.wbloks_1.wbloks_78.wbloks_76 > div:nth-child(8)")
# engagement = driver.find_element(By.CSS_SELECTOR, "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.xw2csxc.x1odjw0f.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div > div.wbloks_1.wbloks_78.wbloks_76 > div:nth-child(10) > div")
# profile_visit = driver.find_element(By.CSS_SELECTOR, "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.xw2csxc.x1odjw0f.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div > div.wbloks_1.wbloks_78.wbloks_76 > div:nth-child(12)")

# # Get text from elements
# overview_text = overview.text
# reach_text = reach.text
# engagement_text = engagement.text
# profile_visit_text = profile_visit.text

# # Print the results
# print("Overview:", overview_text)
# print("------------------")
# print("Reach:", reach_text)
# print("------------------")
# print("Engagement:", engagement_text)
# print("------------------")
# print("Profile Visits:", profile_visit_text)
# print("------------------")

# Save cookies
pickle.dump(driver.get_cookies() , open("cookies.pkl","wb"))

# Save config
with open('config.ini', 'w') as configfile:
  print("Config saved")
  config.write(configfile)

# Quit the driver
driver.quit()