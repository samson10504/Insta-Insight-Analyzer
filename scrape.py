import time
import urllib.request

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

PATH = "/opt/homebrew/bin/chromedriver"
driver = webdriver.Chrome(PATH)

driver.get("https://www.instagram.com/")

def login():
    #login
    time.sleep(5)
    username=driver.find_element(By.CSS_SELECTOR,"input[name='username']")
    password=driver.find_element(By.CSS_SELECTOR,"input[name='password']")
    username.clear()
    password.clear()
    username.send_keys("kenny@projectmelo.com")
    password.send_keys("09231974dcKL#")
    login = driver.find_element(By.CSS_SELECTOR,"button[type='submit']")
    login.click()

    time.sleep(5)
    # notnow = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div/div/div/div").click()
    notnow1 = driver.find_element(By.XPATH, value ="//*[text()='Not now']")
    notnow1.click()

    time.sleep(5)
    notnow2 = driver.find_element(By.XPATH, value ="//*[text()='Not Now']")
    notnow2.click()

login()
link = 'https://www.instagram.com/p/C0d6bT6hqR7/?img_index=1'
driver.get(link)
# driver.implicitly_wait(5)
time.sleep(5)

# Click View insights
insight_element = driver.find_element(By.XPATH, "/html/body/div[2]/div/div/div[2]/div/div/div[1]/div[1]/div[2]/section/main/div/div[1]/div/div[2]/div/section[1]/div/section/div")
insight_element.click()

time.sleep(5)

overview = driver.find_element(By.CSS_SELECTOR, "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.xw2csxc.x1odjw0f.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div > div.wbloks_1.wbloks_78.wbloks_76 > div:nth-child(6)")
print(overview.text)
print("------------------")

reach = driver.find_element(By.CSS_SELECTOR, "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.xw2csxc.x1odjw0f.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div > div.wbloks_1.wbloks_78.wbloks_76 > div:nth-child(8)")
print(reach.text)
print("------------------")

engagement = driver.find_element(By.CSS_SELECTOR, "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.xw2csxc.x1odjw0f.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div > div.wbloks_1.wbloks_78.wbloks_76 > div:nth-child(10) > div")
print(engagement.text)
print("------------------")

profile_visit = driver.find_element(By.CSS_SELECTOR, "body > div.x1n2onr6.xzkaem6 > div.x9f619.x1n2onr6.x1ja2u2z > div > div.x1uvtmcs.x4k7w5x.x1h91t0o.x1beo9mf.xaigb6o.x12ejxvf.x3igimt.xarpa2k.xedcshv.x1lytzrv.x1t2pt76.x7ja8zs.x1n2onr6.x1qrby5j.x1jfb8zj > div > div > div > div > div.x7r02ix.xf1ldfh.x131esax.xdajt7p.xxfnqb6.xb88tzc.xw2csxc.x1odjw0f.x5fp0pe > div > div > div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1n2onr6.xw2csxc.x1odjw0f.x1iyjqo2.x2lwn1j.xeuugli.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 > div > div.wbloks_1.wbloks_78.wbloks_76 > div:nth-child(12)")
print(profile_visit.text)
print("------------------")

# Print the results
# print("Likes:", likes)
# print("Comments:", comments)



time.sleep(99999)