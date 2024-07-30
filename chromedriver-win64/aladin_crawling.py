import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from openpyxl import Workbook
from selenium.webdriver.chrome.options import Options
import logging

# 로깅 설정
logging.basicConfig(filename='crawl_errors.log', level=logging.ERROR, 
                    format='%(asctime)s:%(levelname)s:%(message)s')

# 엑셀 파일 생성
wb = Workbook()
ws = wb.active
ws.append(["연번", "도서명", "저자", "출판사", "금액", "출처"])  # 헤더 추가

# 크롬 드라이버 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  # 브라우저 창을 열지 않고 실행

# 크롬 드라이버 경로 설정
driver = webdriver.Chrome()
driver.get('https://codeit.kr')
# 기본 URL 설정
base_url = 'https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Book&KeyWord=%EC%9E%AC%ED%85%8C%ED%81%AC&KeyRecentPublish=0&OutStock=0&ViewType=Detail&SortOrder=11&CustReviewCount=0&CustReviewRank=0&KeyFullWord=%EC%9E%AC%ED%85%8C%ED%81%AC&KeyLastWord=%EC%9E%AC%ED%85%8C%ED%81%AC&CategorySearch=&chkKeyTitle=&chkKeyAuthor=&chkKeyPublisher=&chkKeyISBN=&chkKeyTag=&chkKeyTOC=&chkKeySubject=&ViewRowCount=25&SuggestKeyWord=&page=1'
page_url_template = 'https://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=Book&KeyWord=%EC%9E%AC%ED%85%8C%ED%81%AC&KeyRecentPublish=0&OutStock=0&ViewType=Detail&SortOrder=11&CustReviewCount=0&CustReviewRank=0&KeyFullWord=%EC%9E%AC%ED%85%8C%ED%81%AC&KeyLastWord=%EC%9E%AC%ED%85%8C%ED%81%AC&CategorySearch=&chkKeyTitle=&chkKeyAuthor=&chkKeyPublisher=&chkKeyISBN=&chkKeyTag=&chkKeyTOC=&chkKeySubject=&ViewRowCount=25&SuggestKeyWord=&page={page}'

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
def crawl_yes24_cash(start_page, end_page):
    for page in range(start_page, end_page + 1):
        url = page_url_template.format(page=page)
        
        print(f"현재 {page} 페이지 크롤링 중...")
        driver.get(url)
        time.sleep(2)  # 페이지 로드 대기
        
        # 페이지 끝까지 스크롤
        scroll_to_bottom()
        
        # 상품 정보 추출
        products_section_1 = driver.find_elements(By.CSS_SELECTOR, 'div.ss_book_list:first-of-type')
        # product_item__MDtDF
        for idx, product in enumerate(products_section_1):
            try:
                # 연번
                연번 = (page - 1) * 25 + idx + 1
                
                # 도서명
                try:
                    도서명 = product.find_element(By.CSS_SELECTOR, 'ul > li > a.bo3').text.strip()
                except Exception as e:
                    도서명 = '도서명 정보 없음'
                    logging.error(f"도서명 추출 실패: {e}")
                    
                # 저자
                try:
                    # ul 요소 내 모든 li 요소 찾기
                    li_elements = product.find_elements(By.CSS_SELECTOR, 'ul > li')
                    li_count = len(li_elements)
                    
                    # li 요소의 개수에 따른 조건부 처리
                    if li_count == 5:
                        # li요소 내 모든 a태그 찾기
                        저자들 = []
                        for li in li_elements:
                            a_elements = li.find_elements(By.CSS_SELECTOR, 'a')
                            a_count = len(a_elements)
                            
                            if a_count == 2:
                                # 저자 = li.find_element(By.CSS_SELECTOR, 'li:nth-of-type(3) > a:first-of-type').text.strip()
                                저자들.append(li.find_element(By.CSS_SELECTOR, 'a:first-of-type').text.strip())
                            elif a_count >= 3:
                                # 저자 = [a.text.strip() for a in a_elements[:-1]]
                                저자들.extend([a.text.strip() for a in a_elements[:-1]])
                                
                    elif li_count == 4:
                        # li 요소 내 모든 a 태그 찾기
                        저자들 = []
                        for li in li_elements:
                            a_elements = li.find_elements(By.CSS_SELECTOR, 'a')
                            a_count = len(a_elements)
                            
                            if a_count == 2:
                                # 저자 = li.find_element(By.CSS_SELECTOR, 'li:nth-of-type(2) > a:first-of-type').text.strip()
                                저자들.append(li.find_element(By.CSS_SELECTOR, 'a:first-of-type').text.strip())
                            elif a_count >= 3:
                                # 저자 = [a.text.strip() for a in a_elements[:-1]]
                                저자들.extend([a.text.strip() for a in a_elements[:-1]])
                    else:
                        저자들 = '저자 정보 없음'
                    저자 = ', '.join(저자들)
                except Exception as e:
                    저자 = '저자 정보 없음'
                    logging.error(f"저자 추출 실패: {e}")

                # 출판사
                try:
                    # ul 요소 내 모든 li 요소 찾기
                    li_elements = product.find_elements(By.CSS_SELECTOR, 'ul > li')
                    li_count = len(li_elements)
                    
                    # li 요소의 개수에 따른 조건부 처리
                    if li_count == 5:
                        출판사 = product.find_element(By.CSS_SELECTOR, 'li:nth-of-type(3) > a:last-of-type').text.strip()
                    elif li_count == 4:
                        출판사 = product.find_element(By.CSS_SELECTOR, 'li:nth-of-type(2) > a:last-of-type').text.strip()
                except Exception as e:
                    출판사 = '출판사 정보 없음'
                    logging.error(f"출판사 추출 실패: {e}")

                # 금액
                try:
                    금액 = product.find_element(By.CSS_SELECTOR, 'ul > li > span.ss_p2').text.strip()
                except Exception as e:
                    금액 = '금액 정보 없음'
                    logging.error(f"금액 추출 실패: {e}")
                # 여기까지 완료
                # 출처
                try:
                    출처 = product.find_element(By.CSS_SELECTOR, 'ul > li > a.bo3').get_attribute('href').strip()
                except Exception as e:
                    출처 = '출처 정보 없음'
                    logging.error(f"출처 추출 실패: {e}")
                # # 도서명
                # 도서명 = product.find_element(By.CSS_SELECTOR, 'div.info_row.info_name > a').text.strip()
                
                # # 저자
                # 저자 = product.find_element(By.CSS_SELECTOR, 'div.info_row.info_pubGrp > span.authPub.info_auth > a').text.strip()
                
                # # 출판사
                # 출판사 = product.find_element(By.CSS_SELECTOR, 'div.info_row.info_pubGrp > span.authPub.info_pub > a').text.strip()
                
                # # 금액
                # 금액 = product.find_element(By.CSS_SELECTOR, 'div.info_row.info_price > strong.txt_num').text.strip()
                
                # # 출처
                # 출처 = product.find_element(By.CSS_SELECTOR, 'div.info_row.info_name > a.gd_name').get_attribute('href').strip()
                
                # 엑셀에 데이터 추가
                ws.append([연번, 도서명, 저자, 출판사, 금액, 출처])
                
                # 콘솔에 출력
                print(f"연번: {연번}, 제품명: {도서명}, 저자: {저자}, 출판사: {출판사}, 금액: {금액}, 출처: {출처}")
            
            except Exception as e:
                print(f"Error: {e}")
                continue
        # products_section_2 = driver.find_elements(By.CSS_SELECTOR, 'div.product_item__MDtDF')
        # for idx, product in enumerate(products_section_2):
        #     try:
        #         # 연번
        #         연번 = (page - 1) * 40 + len(products_section_1) + idx + 1
                
        #         # 제품명
        #         제품명 = product.find_element(By.CSS_SELECTOR, 'div.product_title__Mmw2K').text.strip()
                
        #         # 가격
        #         가격 = product.find_element(By.CSS_SELECTOR, 'span.price').text.strip()
                
        #         # 카테고리
        #         카테고리 = product.find_element(By.CSS_SELECTOR, 'div.product_depth__I4SqY').text.strip()
                
        #         # div.product_title__Mmw2K
        #         # 상세정보
        #         상세정보 = product.find_element(By.CSS_SELECTOR, 'div.product_desc__m2mVJ').text.strip()
        #         # product_desc__m2mVJ
        #         # 엑셀에 데이터 추가
        #         ws.append([연번, 제품명, 가격, 카테고리, 상세정보])
                
        #         # 콘솔에 출력
        #         print(f"연번: {연번}, 제품명: {제품명}, 가격: {가격}, 카테고리: {카테고리}, 상세정보: {상세정보}")
            
        #     except Exception as e:
        #         print(f"Error: {e}")
        #         continue
        # 다음 페이지 로딩 대기
        time.sleep(2)
try:
    crawl_yes24_cash(1, 28)  # O ~ O 페이지까지 크롤링
except Exception as e:
    print(e)
finally:
    driver.quit()  # 브라우저 닫기
    wb.save("aladin_재테크.csv")  # csv 파일 저장
    print("데이터 수집 및 저장 완료")
