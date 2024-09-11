from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import Select
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
    EC.element_to_be_clickable((By.CSS_SELECTOR, '.ly_sub_cnt.colm3-ty1.clear dl:nth-of-type(1) .nano.has-scrollbar .nano-content.dev-main ul li:nth-child(6)'))
)
first_li_in_first_dl.click()
time.sleep(2)

# 두 번째 dl의 첫 번째 li 클릭
first_li_in_second_dl = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '.ly_sub_cnt.colm3-ty1.clear dl:nth-of-type(2) .nano.has-scrollbar .nano-content.dev-sub ul:nth-child(2) li:nth-child(12)'))
)
first_li_in_second_dl.click()
time.sleep(2)

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

# 최신순 으로 변경
new_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, '.tplJobListFunc.clear .tplJobManBtn .tplSltBx-wrap div:nth-of-type(1)'))
)
new_button.click()
time.sleep(2)

# # 클릭 후, Select 클래스를 사용하여 '등록일순'을 선택하는 부분 추가
# select_element = WebDriverWait(driver, 10).until(
#     EC.element_to_be_clickable((By.CSS_SELECTOR, '.tplJobListFunc.clear .tplJobManBtn .tplSltBx-wrap div:nth-of-type(1) .tplSlt'))  
# )

try:
    # 드롭다운 내 '등록일순' 옵션을 클릭하는 부분
    # 먼저 드롭다운 내부의 옵션을 찾습니다. (등록일순의 value가 '2'임)
    register_date_option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, '#orderTab option[value="2"]'))
    )
    register_date_option.click()  # '등록일순' 옵션을 실제로 클릭
    time.sleep(2)

except TimeoutException:
    print("Failed to locate the '등록일순' option within the specified time.")
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
with open('9월11일_게임제작.csv', 'w', newline='', encoding='utf-8') as csvfile:
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