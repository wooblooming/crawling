import csv
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def find_element_with_retry(driver, by, value, max_attempts=5, timeout=10):
    for attempt in range(max_attempts):
        try:
            return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        except (TimeoutException, StaleElementReferenceException):
            if attempt == max_attempts - 1:
                raise

def find_elements_with_retry(driver, by, value, max_attempts=5, timeout=10):
    for attempt in range(max_attempts):
        try:
            elements = WebDriverWait(driver, timeout).until(EC.presence_of_all_elements_located((by, value)))
            if elements:
                return elements
        except (TimeoutException, StaleElementReferenceException):
            if attempt == max_attempts - 1:
                raise
    return []

def clean_text(text):
    cleaned_text = re.sub(r'<br\s*/?>', ' ', text)
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
    return cleaned_text.strip()

def crawl_quasarzone(start_page, end_page):
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-extensions')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    base_url = 'https://quasarzone.com/bbs/qf_hwjoin?page='
    
    with open('quasarzone_data_61to90.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["연번", "제목", "날짜", "글 내용", "댓글 내용"])
        
        post_number = 1
        for page in range(start_page, end_page + 1):
            try:
                driver.get(f"{base_url}{page}")
                time.sleep(5)
                
                posts = find_elements_with_retry(driver, By.CSS_SELECTOR, 'div.dabate-type-list > table > tbody > tr > td > p > a')
                
                for i, post in enumerate(posts):
                    try:
                        post = find_elements_with_retry(driver, By.CSS_SELECTOR, 'div.dabate-type-list > table > tbody > tr > td > p > a')[i]
                        driver.execute_script("arguments[0].scrollIntoView(true);", post)
                        post.click()
                        time.sleep(3)
                        
                        title = find_element_with_retry(driver, By.CSS_SELECTOR, 'div.common-view-area > dl > dt > div > h1.title').text
                        date = find_element_with_retry(driver, By.CSS_SELECTOR, 'span.date').text
                        content = clean_text(find_element_with_retry(driver, By.CSS_SELECTOR, 'div.common-view-area > dl > dd > div.view-content').text)
                        
                        comments = find_elements_with_retry(driver, By.CSS_SELECTOR, 'div.reply-list > ul > li')
                        comment_texts = []
                        for comment in comments[:2]:
                            try:
                                comment_text = comment.find_element(By.CSS_SELECTOR, 'div.reply-list-inner > div.reply-con-area > div.mid-text-area').text
                                comment_texts.append(clean_text(comment_text))
                            except NoSuchElementException:
                                continue
                            if len(comment_texts) == 2:
                                break
                        
                        all_comments = ' || '.join(comment_texts)
                        
                        writer.writerow([post_number, title, date, content, all_comments])
                        post_number += 1
                        
                        driver.back()
                        time.sleep(3)
                    except Exception as e:
                        print(f"Error on page {page}, post {post_number}: {e}")
                        driver.get(f"{base_url}{page}")
                        time.sleep(5)
                        continue
            except Exception as e:
                print(f"Error on page {page}: {e}")
                continue
                
    driver.quit()

# 사용자로부터 시작 페이지와 끝 페이지 입력 받기
start_page = 61
end_page = 90

try:
    crawl_quasarzone(start_page, end_page)
except Exception as e:
    print(f"An error occurred: {e}")