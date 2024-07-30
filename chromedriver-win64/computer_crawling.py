import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from openpyxl import Workbook
from selenium.webdriver.chrome.options import Options

# 엑셀 파일 생성
wb = Workbook()
ws = wb.active
ws.append(["연번", "가격", "상품명", "상세정보"])  # 헤더 추가

# 크롬 드라이버 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 브라우저 창을 열지 않고 실행

# 크롬 드라이버 경로 설정
driver = webdriver.Chrome()
driver.get('https://codeit.kr')
# 기본 URL 설정
base_url = 'https://search.shopping.naver.com/search/all?query=%EB%B8%8C%EB%9E%98%EC%A7%80%EC%96%B4'
page_url_template = 'https://search.shopping.naver.com/search/all?query=%EB%B8%8C%EB%9E%98%EC%A7%80%EC%96%B4&origQuery=%EB%B8%8C%EB%9E%98%EC%A7%80%EC%96%B4&pagingIndex={page}&pagingSize=40&productSet=total&query=%EB%B8%8C%EB%9E%98%EC%A7%80%EC%96%B4&sort=rel&timestamp=&viewType=list'

# 페이지 끝까지 스크롤하는 함수
def scroll_to_bottom():
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 스크롤 후 로딩 대기
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        if new_height == last_height:
            break
        last_height = new_height
        
# 데이터 수집 함수
def crawl_naver_shopping(start_page, end_page):
    for page in range(start_page, end_page + 1):
        url = page_url_template.format(page=page)
        
        print(f"현재 {page} 페이지 크롤링 중...")
        driver.get(url)
        time.sleep(2)  # 페이지 로드 대기
        
        # 페이지 끝까지 스크롤
        scroll_to_bottom()
        
        # 상품 정보 추출
        products_section_1 = driver.find_elements(By.CSS_SELECTOR, 'div.adProduct_item__1zC9h')
        # product_item__MDtDF
        for idx, product in enumerate(products_section_1):
            try:
                # 연번
                연번 = (page - 1) * 40 + idx + 1
                
                # 제품명
                제품명 = product.find_element(By.CSS_SELECTOR, 'div.adProduct_title__amInq').text.strip()
                
                # 가격
                가격 = product.find_element(By.CSS_SELECTOR, 'span.price').text.strip()
                
                # 카테고리
                카테고리 = product.find_element(By.CSS_SELECTOR, 'div.adProduct_depth__s_IUT').text.strip()
                
                # div.product_title__Mmw2K
                # 상세정보
                상세정보 = product.find_element(By.CSS_SELECTOR, 'div.adProduct_desc__uKoBP').text.strip()
                # product_desc__m2mVJ
                # 엑셀에 데이터 추가
                ws.append([연번, 제품명, 가격, 카테고리, 상세정보])
                
                # 콘솔에 출력
                print(f"연번: {연번}, 제품명: {제품명}, 가격: {가격}, 카테고리: {카테고리}, 상세정보: {상세정보}")
            
            except Exception as e:
                print(f"Error: {e}")
                continue
        products_section_2 = driver.find_elements(By.CSS_SELECTOR, 'div.product_item__MDtDF')
        for idx, product in enumerate(products_section_2):
            try:
                # 연번
                연번 = (page - 1) * 40 + len(products_section_1) + idx + 1
                
                # 제품명
                제품명 = product.find_element(By.CSS_SELECTOR, 'div.product_title__Mmw2K').text.strip()
                
                # 가격
                가격 = product.find_element(By.CSS_SELECTOR, 'span.price').text.strip()
                
                # 카테고리
                카테고리 = product.find_element(By.CSS_SELECTOR, 'div.product_depth__I4SqY').text.strip()
                
                # div.product_title__Mmw2K
                # 상세정보
                상세정보 = product.find_element(By.CSS_SELECTOR, 'div.product_desc__m2mVJ').text.strip()
                # product_desc__m2mVJ
                # 엑셀에 데이터 추가
                ws.append([연번, 제품명, 가격, 카테고리, 상세정보])
                
                # 콘솔에 출력
                print(f"연번: {연번}, 제품명: {제품명}, 가격: {가격}, 카테고리: {카테고리}, 상세정보: {상세정보}")
            
            except Exception as e:
                print(f"Error: {e}")
                continue
        # 다음 페이지 로딩 대기
        time.sleep(2)
try:
    crawl_naver_shopping(1, 2)  # 30페이지까지 크롤링
except Exception as e:
    print(e)
finally:
    driver.quit()  # 브라우저 닫기
    wb.save("naver_shopping_data_31to55.csv")  # 엑셀 파일 저장
    print("데이터 수집 및 저장 완료")
