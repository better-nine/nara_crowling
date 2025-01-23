from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# 셀레니움 드라이버 설정
driver = webdriver.Chrome()  # 크롬 드라이버 경로가 PATH에 설정되어 있어야 합니다.
driver.maximize_window()

# G2B 사이트 접속
driver.get("https://www.g2b.go.kr/")

# 팝업 처리
try:
    while True:
        checkboxes = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//input[@type='checkbox' and @title='오늘 하루 이 창을 열지 않음']"))
        )

        if not checkboxes:
            print("더 이상 팝업 없음")
            break

        for checkbox in checkboxes:
            print(checkbox)
            try:
                if checkbox.is_displayed():
                    driver.execute_script("arguments[0].click();", checkbox)
                    print("체크박스 클릭")
                    time.sleep(1)
            except Exception as inner_e:
                print(f"체크박스 클릭 중 오류 발생: {inner_e}")

        checkboxes = driver.find_elements(By.XPATH, "//input[@type='checkbox' and @title='오늘 하루 이 창을 열지 않음']")
        if not checkboxes:
            print("모든 팝업 처리 완료")
            break

except Exception as e:
    print(f"오류 발생: {e}")

menu = driver.find_element(By.LINK_TEXT, "입찰")  # "입찰공고목록" 상위 메뉴

actions = ActionChains(driver)
actions.move_to_element(menu).perform()  # 마우스 오버

# 하위 메뉴 "입찰공고목록" 클릭
time.sleep(1)  # 하위 메뉴가 나타날 때까지 대기
submenu = driver.find_element(By.ID, "mf_wfm_gnb_wfm_gnbMenu_genDepth1_1_genDepth2_0_genDepth3_0_btn_menuLvl3")  # 입찰공고목록 버튼
submenu.click()

# 입찰공고목록 화면 로드 대기
time.sleep(3)

# 상세조건 펼치기 : title 속성이 '토글버튼 접기'인 요소 찾기
# 버튼 클릭
try:
    # 클래스 이름이 'w2wframe udc_srch_toggle'인 요소 모두 가져오기
    elements = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "w2wframe.udc_srch_toggle"))
    )
    # 네 번째 요소 클릭 (index 3, 0부터 시작)
    if len(elements) >= 4:
        target_element = elements[3]  # 네 번째 요소
        target_element.click()
    else:
        print("요소가 4개 이상 존재하지 않습니다.")
except Exception as e:
    print(f"오류 발생: {e}")

# 공고기관 라디오 클릭
notice_agency_radio = driver.find_element(By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_untyGrpGb1_input_0")
notice_agency_radio.click()

time.sleep(1)  # 하위 메뉴가 나타날 때까지 대기
#keywords = ["1421027", "1492000"] #테스트용
# 엑셀 파일 경로
file_path = r"C:\excel\codeInfo.xlsx"

# 엑셀 파일 읽기 (1행을 열 이름으로 설정)
df = pd.read_excel(file_path, header=0)  # header=0은 첫 번째 행(0-index)을 열 이름으로 설정

# 2행부터 값 가져오기
keywords = []

for index, row in df.iterrows():  # DataFrame의 모든 행을 반복
    code = row["수요기관코드"]  # C열 (기관명)
    if pd.notna(code):  # NaN 값 확인 및 제외
        keywords.append(code)

# 결과 출력
print("키워드 목록:", keywords)

# 수요기관코드 입력
for keyword in keywords:
    # 검색 돋보기 아이콘 클릭
    more_search_icon = driver.find_element(By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_btnDmstNmSrch1")
    more_search_icon.click()
    time.sleep(2)  # 클릭 후 대기

    search_box = driver.find_element(By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_FUUB008_01_wframe_popupCnts_ibxSrchDmstCd")
    search_box.clear()
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)  # 검색 결과 로딩 대기

    target_link = driver.find_element(By.XPATH, "//a[contains(text(), '"+str(keyword)+"')]")
    target_link.click()

    # 검색버튼 클릭
    search_icon = driver.find_element(By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_btnS0004")
    search_icon.click()

    # 엑셀다운로드 클릭
    search_icon = driver.find_element(By.ID, "mf_wfm_container_tacBidPbancLst_contents_tab2_body_btnExcelDown4")
    search_icon.click()

    # 이후 작업 수행
    time.sleep(3)  # 라디오 버튼 클릭 후 대기

    # '조회된 데이터가 없습니다.' 텍스트 확인
    no_data_elements = driver.find_elements(By.XPATH, "//*[contains(text(), '조회된 데이터가 없습니다.')]")

    if no_data_elements:
        print(f"키워드 '{keyword}'에 대한 결과: 데이터가 없습니다.")
        # 알림 확인 후 버튼 클릭
        # value 속성이 '확인'인 input 요소 찾기
        confirm_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//input[@type='button' and @value='확인']"))
        )

        # 버튼 클릭
        confirm_button.click()
        print("확인 버튼을 클릭했습니다.")
    else:
        print(f"키워드 '{keyword}'에 대한 결과: 데이터가 존재합니다.")

# 크롬 드라이버 종료
driver.quit()
print("크롤링 및 저장이 완료되었습니다.")
