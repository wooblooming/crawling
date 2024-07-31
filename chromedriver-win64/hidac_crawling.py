import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from openpyxl import Workbook


wb = Workbook()
ws = wb.active

driver = webdriver.Chrome()

# # 최대 페이지 수 설정
# max_pages = 10
# base_url = 'https://hidoc.co.kr/healthqna/list?page={page}'

def crawl_hidoc_qna(max_pages):
    base_url = "https://hidoc.co.kr/healthqna/list?page="
    all_data = [] # 모든 질문과 답변을 저장 할 리스트
    ws.append(["질문","답변"])
    for page in range(1, max_pages + 1):
        driver.get(f"{base_url}{page}")
        time.sleep(2)  # 페이지가 완전히 로드될 때까지 잠시 대기
        
        # 현재 페이지의 모든 질문 링크 가져오기
        question_links = driver.find_elements(By.CSS_SELECTOR, "div.main_head > div.cont > a")
        for q_link in question_links:
            # 질문 페이지로 이동
            q_link.click()
            time.sleep(2)  # 페이지 로드 대기
            # 질문과 답변 추출
            question = driver.find_element(By.CSS_SELECTOR, "strong.tit").text
            answer = driver.find_element(By.CSS_SELECTOR, "div.answer_body > div.cont > div.desc").text
            print(f"질문: {question}\n답변: {answer}\n")
            ws.append([question,answer])
            # 이전 페이지로 돌아가기
            driver.back()
            time.sleep(2)
try:
    crawl_hidoc_qna(1)  # 첫 페이지의 질문과 답변 크롤링
except Exception as e:
    print(e)
finally:
    driver.quit()  # 작업 완료 후 브라우저 닫기
    wb.save("hidac.csv")  