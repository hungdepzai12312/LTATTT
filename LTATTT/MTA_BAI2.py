import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup

url = 'http://thienlongtpct.github.io/inict-reconnaissance/'
  
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(url)
bt1 = set()
bt2 = set()

for student_code in range(100):  
    input_field = driver.find_element(By.CSS_SELECTOR, 'input#studentId')
    input_field.click()

    input_field.send_keys(Keys.CONTROL, "a")
    input_field.send_keys(Keys.BACKSPACE)
    input_field.send_keys(str(student_code))
    
    submit_button = driver.find_element(By.CSS_SELECTOR, '#studentId + div > button')
    submit_button.click()
    
    soup = BeautifulSoup(driver.page_source, "html.parser")

    accordion = soup.find_all("p", class_='MuiTypography-root MuiTypography-body1 MuiTypography-alignJustify css-skiytb')
    bt1.add(accordion[0].text)
    bt2.add(accordion[1].text)

driver.quit()

print("so luong de bai co the tao ra la: ", len(bt1), len(bt2), len(bt1)*len(bt2) )