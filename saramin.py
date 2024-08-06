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
    with open("C:/Users/wjwj9/Desktop/chromedriver-win64_0717/saramin_커리어_link.txt", 'w') as f:
        for i in range(1,67):
            driver.get("https://www.saramin.co.kr/zf_user/company-review-qst-and-ans/sub?page="+str(i)+"&prev=sub&keyword=%EC%BB%A4%EB%A6%AC%EC%96%B4&csn=&cat_mcls=&sort=reg_dt&influencerFl=n&searchType=hashtag&influencer=&type=topic")
            driver.implicitly_wait(3)
            paper_list = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div/div/div[4]/ul/div[1]"))
            )
            lis = paper_list.find_elements(By.TAG_NAME, 'li')
            for li in lis:
                if 'be_image' in li.get_attribute('class'):
                    continue
                urls = li.find_elements(By.TAG_NAME, 'a')
                for url in urls:
                    if 'selfintroduction' not in url.get_attribute('href'):
                        array.append(url.get_attribute('href'))
                    
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
        q_info = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="content"]/div/div[1]/div[1]'))
        )
        date_area = q_info.find_element(By.CSS_SELECTOR, 'div.post_infos > div.post_profile')
        date = date_area.find_element(By.CSS_SELECTOR, 'span.post_date').text
        print(f"날짜 :{date}\n")
        driver.implicitly_wait(3)    
        q_title_element = q_info.find_element(By.CLASS_NAME,'post_top')
        q_title = q_title_element.find_element(By.CSS_SELECTOR, 'h1.qna_subject').text
        print(f"질문 제목: {q_title}")
        
        q_detail_element = q_info.find_element(By.CSS_SELECTOR, 'div.post_cont')
        q_detail = q_detail_element.find_element(By.TAG_NAME, 'div').text
        q_detail = clean_html(q_detail)
        print(f"질문 내용 :{q_detail}")
        

        # 답변
        a_info = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div/div/div/div[1]/div[3]'))
        )
        try:
            a_area = a_info.find_element(By.CSS_SELECTOR, 'ul')
            lis = a_area.find_elements(By.TAG_NAME, 'li')
            answers = []
            for li in lis:
                try:
                    cont_sec = li.find_element(By.CSS_SELECTOR, 'div.wrap_comment > div.comment_view')
                    answer = cont_sec.find_element(By.CSS_SELECTOR, 'span.comment_txt').text
                    answer = clean_html(answer)
                    answers.append(answer)
                    driver.implicitly_wait(3)
                except NoSuchElementException:
                    continue
        except NoSuchElementException:
            answers=['답변 없음']
        if not answers:
            answers.append('답변 없음')
        print(f"답변 :{answers}")
        
        
        return {
            '작성일' : date,
            '질문 제목' : q_title,
            '질문 내용' : q_detail,
            '답변들' : answers
        }
    except TimeoutException:
        print("Timeout occurred while loading the page.")
        return {
            '작성일': '',
            '질문 제목': '',
            '질문 내용': '',
            '답변들': ['답변 없음']
        }
def save_to_csv(data, filename):
    # 기본 컬럼
    columns = ['작성일', '질문 제목', '질문 내용']
    
    # 가장 많은 답변 수를 가진 항목의 답변 수를 확인
    max_answers = max(len(item['답변들']) for item in data)
    
    # 답변 컬럼 추가
    columns.extend([f'답변 {i+1}' for i in range(max_answers)])
    
    # 데이터프레임 생성
    rows = []
    for item in data:
        row = [
            item['작성일'],
            item['질문 제목'],
            item['질문 내용']
        ]
        row.extend(item['답변들'])
        # 답변이 부족한 경우 빈 문자열로 채움
        row.extend([''] * (max_answers - len(item['답변들'])))
        rows.append(row)
    
    df = pd.DataFrame(rows, columns=columns)
    df.to_csv(filename, index=False)
