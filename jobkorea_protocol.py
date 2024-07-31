import jobkorea
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

file_path = 'C:/Users/wjwj9/Desktop/chromedriver-win64_0717/chromedriver-win64/jobkorea_link6.txt'

output_file = 'jobkorea6.csv'
columns = ['지원 회사 이름', '지원 시기', '직무명']
data_rows = []
max_qna_length = 0

driver = webdriver.Chrome()
jobkorea.login_protocol(driver=driver)
# jobkorea.link_crawl(driver=driver)

with open(file_path, 'r') as file:
    while True: # 7354개
        file_url = file.readline().strip()
        if not file_url:
            break
        
        # 자소서 크롤링
        data = jobkorea.self_introduction_crawl(driver=driver,file_url=file_url)
        
        # 'QnA' 키가 없을 경우에 대한 예외 처리
        if 'QnA' not in data:
            print(f"Error: 'QnA' key not found for URL {file_url}")
            continue
        
        # 크롤링 데이터 처리
        qna_columns = []
        qna_length = len(data['QnA'])
        if qna_length > max_qna_length:
            max_qna_length = qna_length
            
        # for i in range(len(data['QnA'])):
        #     qna_columns.append(f'질문{i+1}')
        #     qna_columns.append(f'답변{i+1}')
        
        row = [data['지원 회사 이름'], data['지원 시기'], data['직무명']]
        for qna in data['QnA']:
            row.append(qna[0])
            row.append(qna[1])
        
        data_rows.append(row)

#모든 행의 열 수를 맞추기 위해 빈 문자열로 채움
for row in data_rows:
    while len(row) < 3 + max_qna_length * 2:
        row.append("")

# 동적으로 생성된 열 이름 추가
for i in range(max_qna_length):
        columns.append(f'질문{i+1}')
        columns.append(f'답변{i+1}')
        
# 데이터 프레임 생성 및 csv 저장
df = pd.DataFrame(data_rows, columns=columns + qna_columns)
df.to_csv(output_file, index=False, encoding='utf-8-sig')

print ("Data saved to", output_file)