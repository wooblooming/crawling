from jobtoktok import link_crawl, self_introduction_crawl, save_to_csv
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time

file_path = 'C:/Users/wjwj9/Desktop/chromedriver-win64_0717/jobtoktok_link.txt'

#output_file = 'jobkorea6.csv'

driver = webdriver.Chrome()
# jobkorea.login_protocol(driver=driver)
#link_crawl(driver=driver)

with open(file_path, 'r') as file:
    links = file.readlines()

# 결과를 저장할 리스트
all_data = []

# 각 링크에 대해 self_introduction_crawl 실행
for link in links:
    link = link.strip()
    if link:
        data = self_introduction_crawl(driver, link)
        all_data.append(data)
        print(data)
        time.sleep(1)
save_to_csv(all_data, "C:/Users/wjwj9/Desktop/chromedriver-win64_0717/jobtoktok_30.csv")
driver.quit()
