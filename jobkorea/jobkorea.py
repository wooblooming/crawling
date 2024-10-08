from selenium import webdriver
from selenium.webdriver.common.by import By
from collections import OrderedDict
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import UnexpectedAlertPresentException, NoAlertPresentException, TimeoutException
from bs4 import BeautifulSoup
import pandas as pd
import re

def _get_urls_to_detail_page(driver:webdriver.Chrome) -> list[str]:
    for page in range(1,30):
        driver.get(
            (
                "https://www.jobkorea.co.kr"
                f"/starter/passassay?schTxt=&Page={page}"
            )
        )

        driver.implicitly_wait(3)
        paper_list = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, 
                "/html/body/div[4]/div[2]/div[2]/div[5]/ul",
            ))
        )
        driver.implicitly_wait(3)

        urls = paper_list.find_elements(By.TAG_NAME,'a')
        for url in urls:
            if 'selfintroduction' not in url.get_attribute('href'):
                array.append(url.get_attribute('href'))
    
    array = list(OrderedDict.fromkeys(array))
    return array

def save_url_list(driver:webdriver.Chrome):    
    array= _get_urls_to_detail_page(driver)
    with open("C:/Users/wjwj9/Desktop/chromedriver-win64_0717/chromedriver-win64/jobkorea_link6.txt", 'w') as f:
        for content in array:
            f.write(content+'\n')
        f.close()


def login_protocol(driver:webdriver.Chrome): # 로그인해야지 로그인창때문에 크롤링 멈추는거 막을 수 있음
    driver.get("https://www.jobkorea.co.kr/")
    driver.find_element(By.XPATH,"/html/body/div[3]/div/div[2]/div[1]/div/ul[2]/ul/li[1]/a").click()
    driver.find_element(By.ID,"M_ID").send_keys("rkddnwls98")
    driver.find_element(By.ID,"M_PWD").send_keys("dkdlel1599!")
    driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/div[1]/form/fieldset/section[3]/button").click()
    driver.implicitly_wait(3)
    print("login success")
    

def clean_html(html_text):
    # BS4를 이용해서 <br> 태그를 공백으로 대체
    soup = BeautifulSoup(html_text, 'html.parser')   
    for br in soup.find_all('br'):
        br.replace_with(' ')
    text = ' '.join(soup.get_text().split())
    # 글자수 N자MByte 패턴제거
    text = re.sub(r'글자수 \d+자\d+Byte', '', text).strip()
    return text


def split_season_and_job(season_text):
    if '신입' in season_text:
        split_point = season_text.index('신입') + len('신입')
    elif '인턴' in season_text:
        split_point = season_text.index('인턴') + len('인턴')
    else:
        split_point = len(season_text)
        
    return season_text[:split_point].strip(), season_text[split_point:].strip()


def is_alert_present(driver:webdriver.Chrome):
    try:
        # 알림 감지 및 처리
        WebDriverWait(driver, 3).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        print("Alert present: ", alert.text)
        alert.accept()
        return True
    except TimeoutException:
        pass
    return False


def parse_application_details(
    driver:webdriver.Chrome,
): 
    user_info_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.XPATH, '//*[@id="container"]/div[2]/div[1]/div[1]/h2'
        ))
    )
    company_name = user_info_element.find_element(By.TAG_NAME,'a').text
    application_period = user_info_element.find_element(By.TAG_NAME,'em').text
    support_period, job_title = split_season_and_job(application_period)

    return {
        '지원 회사 이름' : company_name,
        '지원 시기' : support_period,
        '직무명' : job_title,
    }

def parse_qnas(
    driver:webdriver.Chrome,
):
    paper = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "qnaLists"))
    )
    questions = paper.find_elements(By.TAG_NAME,'dt')
    answers = paper.find_elements(By.TAG_NAME, 'dd')
    
    qna_pairs = []
    
    for index in range(len(questions)):
        # 질문 크롤링
        question_elem = questions[index]
        question = question_elem.find_element(By.CLASS_NAME,'tx').text
        if question == "":
            question_elem.find_element(By.TAG_NAME,'button').click()
            question = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME,'tx'))
            ).text
        question = clean_html(question)
        print(f"Question {index + 1}: {question}")
        
        # 답변 크롤링
        answer_elem = answers[index]
        try:
            answer = answer_elem.find_element(By.CLASS_NAME, 'tx').get_attribute('innerHTML')
        except:
            question_elem.find_element(By.TAG_NAME, 'button').click()
            answer = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'tx'))
            ).get_attribute('innerHTML')
        
        answer = clean_html(answer)
        qna_pairs.append((question, answer))
        print(f"Answer {index + 1}: {answer}")

    return {
        'QnA' : qna_pairs
    }


def self_introduction_crawl(
    driver:webdriver.Chrome,
    file_url: str,
) :
    print("current URL : "+ file_url)
    driver.get(file_url)
    
    if is_alert_present(driver):
        return {
            '지원 회사 이름': '',
            '지원 시기': '',
            '직무명': '',
            'QnA': []
        }

    return {
        **parse_application_details(driver),
        **parse_qnas(driver),
    }
