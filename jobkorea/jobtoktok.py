from selenium import webdriver
from selenium.webdriver.common.by import By
from collections import OrderedDict
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException, TimeoutException, NoSuchElementException
from bs4 import BeautifulSoup
import pandas as pd
import re

def link_crawl(driver:webdriver.Chrome):
    array= []
    with open("C:/Users/wjwj9/Desktop/chromedriver-win64_0717/jobtoktok_link.txt", 'w') as f:
        for i in range(1,3):
            driver.get("https://www.jobkorea.co.kr/User/Qstn/index?MainType=3&OrderType=3&page="+str(i))
            driver.implicitly_wait(3)
            paper_list = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[4]/div[2]/div/div[1]/div[3]/ul"))
            )
            driver.implicitly_wait(3)
            lis = paper_list.find_elements(By.TAG_NAME, 'li')
            for li in lis:
                if 'background-blue' not in li.get_attribute('class'):
                    try:
                        post_title = li.find_element(By.CLASS_NAME, 'post-title')
                        if post_title.find_element(By.TAG_NAME, 'i'):
                            cont_area = li.find_element(By.CLASS_NAME, 'contArea')
                            a_tag = cont_area.find_element(By.TAG_NAME, 'a')
                            href = a_tag.get_attribute('href')
                            if 'selfintroduction' not in href:
                                array.append(href)
                    except NoSuchElementException:
                        continue
                    
        array = list(OrderedDict.fromkeys(array))
        for content in array:
            f.write(content+'\n')
        f.close()
        
# def login_protocol(driver:webdriver.Chrome): # 로그인해야지 로그인창때문에 크롤링 멈추는거 막을 수 있음
#     driver.get("https://www.jobkorea.co.kr/")
#     driver.find_element(By.XPATH,"/html/body/div[3]/div/div[2]/div[1]/div/ul[2]/ul/li[1]/a").click()
#     driver.find_element(By.ID,"M_ID").send_keys("rkddnwls98")
#     driver.find_element(By.ID,"M_PWD").send_keys("dkdlel1599!")
#     driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/div[1]/form/fieldset/section[3]/button").click()
#     driver.implicitly_wait(3)
#     print("login success")
    
def clean_html(html_text):
    # BS4를 이용해서 <br> 태그를 공백으로 대체
    soup = BeautifulSoup(html_text, 'html.parser')   
    for br in soup.find_all('br'):
        br.replace_with(' ')
    text = ' '.join(soup.get_text().split())
    return text

# def split_season_and_job(season_text):
#     if '신입' in season_text:
#         split_point = season_text.index('신입') + len('신입')
#     elif '인턴' in season_text:
#         split_point = season_text.index('인턴') + len('인턴')
#     else:
#         split_point = len(season_text)
        
#     return season_text[:split_point].strip(), season_text[split_point:].strip()

def self_introduction_crawl(driver:webdriver.Chrome,file_url):
    print("current URL : "+ file_url)
    driver.get(file_url)
    
    try:
        # 질문
        q_info = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div[2]/div[1]'))
        )
        date_area = q_info.find_element(By.CSS_SELECTOR, 'div.post-state > div.post-cell-box')
        spans = date_area.find_elements(By.CLASS_NAME, 'cell')
        if len(spans) > 1:
            views = spans[0].text # 조회수
            date = spans[1].text # 날짜
            print(f"조회수 :{views}, 날짜 :{date}\n")
            
        q_title_element = q_info.find_element(By.CLASS_NAME,'tit')
        q_title_html = q_title_element.get_attribute('outerHTML')
        soup = BeautifulSoup(q_title_html, 'html.parser')
        for i in soup.find_all('i'):
            i.decompose()
        q_title = soup.get_text(strip=True)
        print(f"질문 제목: {q_title}")
        
        q_detail = q_info.find_element(By.CLASS_NAME, 'cont').text
        q_detail = clean_html(q_detail)
        print(f"질문 내용 :{q_detail}")
        
        try:
            q_job_element = q_info.find_element(By.CSS_SELECTOR,'div.labelBx.swiper-wrapper')
            a_tags = q_job_element.find_elements(By.TAG_NAME, 'a')
            q_job = ' / '.join([a.text for a in a_tags])
        except NoSuchElementException:
            q_job = "직무명 없음"
        print(f"직무명 :{q_job}")
        
        # 답변
        a_info = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[2]/div/div[2]/div[2]/div[2]'))
        )
        a_area = a_info.find_element(By.CSS_SELECTOR, 'ul')
        lis = a_area.find_elements(By.TAG_NAME, 'li')
        answers = []
        for li in lis:
            try:
                cont_sec = li.find_element(By.CSS_SELECTOR, 'div.contSec.devContSection ')
                info_bx = cont_sec.find_element(By.CLASS_NAME, 'infoBx')
                span_info = info_bx.find_element(By.CLASS_NAME, 'info').text
                p_cont = cont_sec.find_element(By.CLASS_NAME, 'cont').text
                answer = f"{span_info} - {p_cont}"
                answer = clean_html(answer)
                answers.append(answer)
            except NoSuchElementException:
                continue
        print(f"답변 :{answers}")
        
        
        return {
            '작성일' : date,
            '조회수' : views,
            '직무명' : q_job,
            '질문 제목' : q_title,
            '질문 내용' : q_detail,
            '답변들' : answers
        }
    except TimeoutException:
        print("Timeout occurred while loading the page.")
        return {
            '작성일': '',
            '조회수': '',
            '직무명': '',
            '질문 제목': '',
            '질문 내용': '',
            '답변들': []
        }
def save_to_csv(data, filename):
    # 기본 컬럼
    columns = ['작성일', '조회수', '직무명', '질문 제목', '질문 내용']
    
    # 가장 많은 답변 수를 가진 항목의 답변 수를 확인
    max_answers = max(len(item['답변들']) for item in data)
    
    # 답변 컬럼 추가
    columns.extend([f'답변 {i+1}' for i in range(max_answers)])
    
    # 데이터프레임 생성
    rows = []
    for item in data:
        row = [
            item['작성일'],
            item['조회수'],
            item['직무명'],
            item['질문 제목'],
            item['질문 내용']
        ]
        row.extend(item['답변들'])
        # 답변이 부족한 경우 빈 문자열로 채움
        row.extend([''] * (max_answers - len(item['답변들'])))
        rows.append(row)
    
    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(filename, index=False)
