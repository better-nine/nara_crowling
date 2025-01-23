from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

driver = webdriver.Chrome()
driver.maximize_window()
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

# 상단 메뉴 "발주"에 마우스 오버
time.sleep(3)  # 페이지 로드 대기
menu = driver.find_element(By.LINK_TEXT, "발주")  # "발주" 상위 메뉴

actions = ActionChains(driver)
actions.move_to_element(menu).perform()  # 마우스 오버

# 하위 메뉴 "발주목록" 클릭
time.sleep(3)  # 하위 메뉴가 나타날 때까지 대기
submenu = driver.find_element(By.ID, "mf_wfm_gnb_wfm_gnbMenu_genDepth1_0_genDepth2_0_btn_menuLvl2")  # 발주목록 버튼
submenu.click()

# 발주목록 화면 로드 대기
time.sleep(3)

# 라디오 버튼 선택
radio_button = driver.find_element(By.ID, "mf_wfm_container_radSrchTy_input_1")
radio_button.click()

# 이후 작업 수행
time.sleep(2)  # 라디오 버튼 클릭 후 대기
search_box = driver.find_element(By.ID, "mf_wfm_container_txtBizNm")  # 실제 검색 박스 ID
keywords = ["웹사이트", "홈페이지", "누리집", "대국민"]

for keyword in keywords:
    search_box.clear()
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)  # 검색 결과 로딩 대기

    # 엑셀 다운로드 버튼 클릭
    excel_download_button = driver.find_element(By.ID, "mf_wfm_container_btnExcelDwnld")
    excel_download_button.click()
    time.sleep(3)  # 다운로드 완료 대기

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
