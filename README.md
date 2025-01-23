# python_crowling

# 나라장터 크롤링 (2025.01.23)

## ! 주의사항 !

- **셀레니움 동작 중 셀레니움 창에 마우스 오버 금지!**
    - **나라장터 홈페이지에 마우스 오버로 동작하는 부분들과 작업 충돌이 일어남**

## < 발주목록 >

### 데이터 크롤링

1. 파이참 실행
2. nara_crowling.py 수행
3. 다운로드 폴더에서 다운받은 크롤링 파일 확인

- 검색 조건을 추가하고 싶으면 keywords 배열에 단어를 추가하면 됨

```python
search_box = driver.find_element(By.ID, "mf_wfm_container_txtBizNm")  # 실제 검색 박스 ID
keywords = ["웹사이트", "홈페이지", "누리집", "대국민"]
```

## < 입찰목록 >

### 데이터 크롤링 (엑셀 파일 내 수행기관 코드로 검색)

```python
# 엑셀 파일 경로
file_path = r"C:\excel\codeInfo.xlsx"
```

1. 파이참 실행
2. nara_crowling_bid.py 수행
3. 다운로드 폴더에서 다운받은 크롤링 파일 확인

### 엑셀 파일 취합

1. nara_crowling_bid_sort.py 수행 전 파일 저장경로 변경 필요

```python
# 폴더 경로 설정
folder_path =  r"C:\excel\수행일자" 
output_file = r"C:\excel\수행일자\merged_output.xlsx"
```

1. nara_crowling_bid_sort.py 수행
2. 저장된 파일 확인

### 엑셀파일 내 데이터 변경 (일자 구분)

1. excel_sort.py 수행 전 파일 저장경로 변경 필요

```python
# 엑셀 파일 불러오기
input_file = r"C:\excel\수행일자\merged_output.xlsx" # 입력 파일명
output_file = r"C:\excel\수행일자\merged_output_sort.xlsx"  # 출력 파일명
```

1. excel_sort.py 수행
2. 저장된 파일 확인
