import pandas as pd

# 엑셀 파일 불러오기
input_file = r"C:\excel\2025-01-16\merged_output.xlsx" # 입력 파일명
output_file = r"C:\excel\2025-01-16\merged_output_sort.xlsx"  # 출력 파일명

# 데이터 읽기
df = pd.read_excel(input_file, engine='openpyxl')
# 엑셀 파일의 두 번째 시트 읽기
df = pd.read_excel(input_file, sheet_name=1, engine='openpyxl')  # 두 번째 시트는 1 (0부터 시작)

# 컬럼 이름 확인
print("엑셀 컬럼 이름 확인:", df.columns)

# H열에 해당하는 컬럼 이름 반영 (확인 후 수정)
h_column_name = "게시일시(입찰마감일시)"  # 정확한 컬럼 이름으로 수정 필요
h_column = df[h_column_name][0:]  # 2번 행부터 가져오기


# 데이터 처리 함수
def split_date_time(cell_value):
    if pd.isna(cell_value):
        return pd.Series([None, None, None, None])  # 빈 셀 처리

    try:
        # 값에서 필요한 부분 추출
        first_space = cell_value.find(" ")  # 첫 번째 공백 위치
        first_parenthesis = cell_value.find("(")  # 첫 번째 '(' 위치
        last_parenthesis = cell_value.rfind(")")  # 마지막 ')' 위치
        second_space = cell_value.find(" ", first_parenthesis)  # 첫 번째 '(' 이후 첫 공백 위치

        # 게시일자와 게시일시
        posting_date = cell_value[:first_space]  # 첫 번째 공백 이전
        posting_time = cell_value[first_space + 1:first_parenthesis].strip()  # 첫 번째 공백과 '(' 사이

        # 입찰마감일자와 입찰마감일시 계산
        if (
                first_parenthesis != -1
                and last_parenthesis != -1
                and " " in cell_value[first_parenthesis + 1:last_parenthesis]
        ):
            # '(' 이후와 마지막 ')' 사이에 공백이 있는 경우
            bid_close_date = cell_value[first_parenthesis + 1:second_space].strip()  # '(' 이후와 두 번째 공백 사이
            bid_close_time = cell_value[second_space + 1:last_parenthesis].strip()  # 두 번째 공백과 ')' 사이
        else:
            # '('와 ')' 사이에 공백이 없거나 값이 없는 경우
            bid_close_date, bid_close_time = None, None

        return pd.Series([posting_date, posting_time, bid_close_date, bid_close_time])
    except Exception as e:
        return pd.Series([None, None, None, None])  # 에러 발생 시 None 반환


# 각 셀 데이터를 4개 컬럼으로 분리
df_split = h_column.apply(split_date_time)

# 컬럼 이름 지정
df_split.columns = ["게시일자", "게시일시", "입찰마감일자", "입찰마감일시"]

# 결과 저장
df_split.to_excel(output_file, index=False, engine='openpyxl')

print(f"분리된 데이터가 '{output_file}'에 저장되었습니다.")