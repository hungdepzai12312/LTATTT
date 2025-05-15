import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager

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
    
    time.sleep(1)  # Chờ nội dung load sau khi nhấn nút
    
    # Lấy danh sách các đoạn văn bản hiển thị đề bài
    accordion1 = driver.find_element(By.CSS_SELECTOR, 'h3.MuiAccordion-heading.css-14m00pi')
    accordion1.click()
    accordion = driver.find_elements(By.CSS_SELECTOR, 'p.MuiTypography-root.MuiTypography-body1.MuiTypography-alignJustify.css-skiytb')
    print(accordion[0].text) 
    print(accordion[1].text)# Đảm bảo có đủ phần tử cần lấy
    bt1.add(accordion[0].text)
    bt2.add(accordion[1].text)

driver.quit()

print("Số lượng đề bài có thể tạo ra là:", len(bt1), len(bt2), len(bt1) * len(bt2))
