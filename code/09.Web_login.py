import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.get("https://qldt.utc.edu.vn/congthongtin/login.aspx")

wait = WebDriverWait(driver, 10)

# Chờ và nhập mã sinh viên
username_box = wait.until(EC.presence_of_element_located((By.ID, "username")))
username_box.send_keys("_____________")

# Nhập mật khẩu
password_box = wait.until(EC.presence_of_element_located((By.ID, "password")))
password_box.send_keys("_____________")

# Click đăng nhập
login_button = wait.until(EC.element_to_be_clickable((By.ID, "cms_authenticate_do_login")))
login_button.click()

# Chờ chuyển tiếp
time.sleep(5)

# Truy cập trang cần lấy
driver.get("https://qldt.utc.edu.vn/congthongtin/Index.aspx#tintuc")
time.sleep(5)

# Lấy nội dung HTML
html = driver.page_source
soup1 = BeautifulSoup(html, "html.parser")

titles = soup1.find_all("div",class_ = "slider-item bantin2")
title = titles[0]
name = title.find("a", class_="card-news-title").get_text()
print(name)


driver.quit()
