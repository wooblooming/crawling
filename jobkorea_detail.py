from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import csv
import time

driver = webdriver.Chrome()

# 웹사이트 열기
url = 'https://www.jobkorea.co.kr/recruit/joblist?menucode=duty'
driver.get(url)

# 페이지 하단까지 스크롤하는 함수
def scroll_to_bottom():
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.END)
    time.sleep(2)

# # 첫 번째 dl의 첫 번째 li 클릭
# first_li_in_first_dl = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.CSS_SELECTOR, '.ly_sub_cnt.colm3-ty1.clear dl:nth-of-type(1) .nano.has-scrollbar .nano-content.dev-main ul li:nth-child(16)'))
# )
# first_li_in_first_dl.click()
# time.sleep(2)

# # 두 번째 dl의 첫 번째 li 클릭
# first_li_in_second_dl = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.CSS_SELECTOR, '.ly_sub_cnt.colm3-ty1.clear dl:nth-of-type(2) .nano.has-scrollbar .nano-content.dev-sub ul:nth-child(2) li:first-child'))
# )
# first_li_in_second_dl.click()
# time.sleep(2)

# # 두 번째 dl의 첫 번째 li 클릭
# first_li_in_second_dl = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.CSS_SELECTOR, '.ly_sub_cnt.colm3-ty1.clear dl:nth-of-type(2) .nano.has-scrollbar .nano-content.dev-sub ul:nth-child(2) li:nth-child(2)'))
# )
# first_li_in_second_dl.click()
# time.sleep(2)

# # 두 번째 dl의 첫 번째 li 클릭
# first_li_in_second_dl = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.CSS_SELECTOR, '.ly_sub_cnt.colm3-ty1.clear dl:nth-of-type(2) .nano.has-scrollbar .nano-content.dev-sub ul:nth-child(2) li:nth-child(3)'))
# )
# first_li_in_second_dl.click()
# time.sleep(2)

# # 두 번째 dl의 첫 번째 li 클릭
# first_li_in_second_dl = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.CSS_SELECTOR, '.ly_sub_cnt.colm3-ty1.clear dl:nth-of-type(2) .nano.has-scrollbar .nano-content.dev-sub ul:nth-child(2) li:nth-child(8)'))
# )
# first_li_in_second_dl.click()
# time.sleep(2)

# 첫 번째 dl의 첫 번째 li 클릭
first_li_in_first_dl = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '.ly_sub_cnt.colm3-ty1.clear dl:nth-of-type(1) .nano.has-scrollbar .nano-content.dev-main ul li:nth-child(8)'))
)
first_li_in_first_dl.click()
time.sleep(2)

# 두 번째 dl의 첫 번째 li 클릭
first_li_in_second_dl = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '.ly_sub_cnt.colm3-ty1.clear dl:nth-of-type(2) .nano.has-scrollbar .nano-content.dev-sub ul:nth-child(2) li:first-child'))
)
first_li_in_second_dl.click()
time.sleep(2)

# 두 번째 dl의 첫 번째 li 클릭
first_li_in_second_dl = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '.ly_sub_cnt.colm3-ty1.clear dl:nth-of-type(2) .nano.has-scrollbar .nano-content.dev-sub ul:nth-child(2) li:nth-child(4)'))
)
first_li_in_second_dl.click()
time.sleep(2)

# # 세 번째 dl의 첫 번째 li 클릭
# first_li_in_second_dl = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.CSS_SELECTOR, '.ly_sub_cnt.colm3-ty1.clear dl:nth-of-type(3) .nano.has-scrollbar .nano-content.dev-keyword ul:nth-child(2) li:nth-child(3)'))
# )
# first_li_in_second_dl.click()
# time.sleep(2)

# # 두 번째 dl의 첫 번째 li 클릭
# first_li_in_second_dl = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.CSS_SELECTOR, '.ly_sub_cnt.colm3-ty1.clear dl:nth-of-type(2) .nano.has-scrollbar .nano-content.dev-sub ul:nth-child(2) li:nth-child(15)'))
# )
# first_li_in_second_dl.click()
# time.sleep(2)

# btnSet의 버튼 클릭
btn_set = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '.resultSetWrap .listWrap.clear dd.btnSet'))
)
btn_set.click()
time.sleep(4)
# 테이블 로드를 위해 하단으로 스크롤
scroll_to_bottom()

# 현재 페이지에서 채용 정보 추출하는 함수
def extract_job_details():
    jobs = []
    rows = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#dev-gi-list .tplJobListWrap.devTplTabBx .tplList.tplJobList table tbody tr'))
    )
    for row in rows:
        try:
            try:
                company_element = row.find_element(By.CSS_SELECTOR, 'td.tplCo > a.link.normalLog')
            except NoSuchElementException:
                company_element = row.find_element(By.CSS_SELECTOR, 'td.tplCo > a')
            company = company_element.text
            title_element = row.find_element(By.CSS_SELECTOR, '.tplTit .titBx strong a')
            title = title_element.text
            link = title_element.get_attribute('href')
            jobs.append([company, title, link])
        except Exception as e:
            print(f"Error extracting job details: {e}")
            continue
    return jobs

# 페이지네이션 버튼 클릭 함수
def click_pagination_button(index):
    pagination_buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#dvGIPaging .tplPagination.newVer ul li'))
    )
    pagination_buttons[index].click()
    time.sleep(2)

# 다음 페이지 세트로 이동하는 함수
def go_to_next_page_set():
    next_button = WebDriverWait(driver, 10).until(
         EC.element_to_be_clickable((By.CSS_SELECTOR, '#dvGIPaging .tplPagination.newVer p a.tplBtn.btnPgnNext'))
    )
    next_button.click()
    time.sleep(2)

# CSV 파일에 채용 정보 저장
with open('job_물류무역.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['회사명','직무명', '링크'])

    for _ in range(3):  # 처음 10페이지 순회
        job_details = extract_job_details()
        csvwriter.writerows(job_details)
        
        # 페이지네이션 버튼 1에서 10까지 클릭
        for i in range(10):
            click_pagination_button(i)
            job_details = extract_job_details()
            csvwriter.writerows(job_details)

        go_to_next_page_set()

# 드라이버 종료
driver.quit()