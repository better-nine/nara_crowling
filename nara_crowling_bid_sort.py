import os
import pandas as pd
from openpyxl import Workbook


# 폴더 경로 설정
folder_path =  r"C:\excel\2025-01-16"
output_file = r"C:\excel\2025-01-16\merged_output.xlsx"

# 취합한 데이터를 저장할 리스트
merged_data = []

# 엑셀 헤더 양식 정의
headers = [
    "업무구분",
    "업무여부",
    "구분",
    "입찰공고번호",
    "공고명",
    "공고기관",
    "수요기관",
    "게시일시(입찰마감일시)"
]

# 폴더 내 모든 파일 순환
for file_name in os.listdir(folder_path):
    if file_name.endswith('.xlsx') or file_name.endswith('.xls'):
        file_path = os.path.join(folder_path, file_name)
        try:
            # 엑셀 파일 읽기 (A~H열, 6행부터)
            excel_data = pd.read_excel(file_path, usecols='A:H', skiprows=5, header=None)

            # 파일 이름을 데이터에 추가 (옵션)
            excel_data["Source File"] = file_name

            # 데이터 취합
            merged_data.append(excel_data)
        except Exception as e:
            print(f"Error reading {file_name}: {e}")

# 취합된 데이터를 하나의 데이터프레임으로 병합
if merged_data:
    combined_df = pd.concat(merged_data, ignore_index=True)

    # 새 워크북 생성 및 헤더 추가
    wb = Workbook()
    ws = wb.active
    ws.append(headers)

    # 병합된 데이터 추가
    for row in combined_df.itertuples(index=False, name=None):
        ws.append(row)

    # 병합된 데이터를 엑셀 파일로 저장
    wb.save(output_file)
    print(f"Merged data has been saved to {output_file}")
else:
    print("No Excel files found or failed to read any files.")
