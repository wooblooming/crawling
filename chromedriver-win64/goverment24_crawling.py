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

def crawl_goverment(max_pages):
    base_url = "https://www.gov.kr/portal/rcvfvrSvc/svcFind/svcSearchAll"
    params = {
        'cityDoArea': 'ALL',
        'siGunGuArea': 'ALL',
        'sidocode': 'ALL',
        'svccd': 'ALL',
        'tccd': 'ALL',
        'meancd': 'ALL',
        'chktype1': '',
        'sortOrder': 'DESC',
        'collection': '',
        'range': '',
        'startDate': '',
        'endDate': '',
        'searchField': '',
        'reQuery': '2',
        'stQuery': '',
        'downOrgCd': '',
        'tmpReQuery': '',
        'tmpExReQuery': '',
        'reSerachQuery': '',
        'realQuery': '',
        'detailLst': '0',
        'sort': 'RANK',
        'query': '',
        'orgSel': 'ALL',
        'showView': 'view22',
        'chktype21': ''
    }
    
    # 페이지별 startCount 값 설정
    for page in range(9):
        params['startCount'] = page * 12
        response = requsets.get(base_url, params=params)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 필요한 데이터 추출 (예: 제목)
            titles = soup.select('CSS_SELECTOR_FOR_TITLE')
            for title in titles:
                print(title.get_text(strip=True))
        else:
            print(f"페이지 {page + 1} 로드 실패: {response.status_code}")