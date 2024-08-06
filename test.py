import pandas as pd
import numpy as np

# 랜덤 숫자 생성
data = np.random.randint(20, 251, size=2700)

# 데이터프레임 생성
df = pd.DataFrame(data, columns=['RandomNumbers'])

# CSV 파일로 저장
df.to_csv('random_numbers.csv', index=False)

print("CSV 파일이 성공적으로 저장되었습니다.")
