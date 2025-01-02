from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os
import numpy as np


driver = webdriver.Chrome()


current_path = os.path.dirname(__file__)
file_path = os.path.join(current_path, '/Users/shin-yoonhwan/vscode/stock_data/data/dropped_basic_info.csv')
basic_file = pd.read_csv(file_path, index_col=None)



def take_detail_info(len_date, ticker): # len_date -> 분기 개수 선택
    list = []
    try:
        for date in range(len_date):
            info_list = [ticker]
            selector_date = f'#container > div.sub_mid.tabs_area > div > div:nth-child(2) > div > table > thead > tr > th:nth-child({date+2}) > span'
            navi_date = driver.find_element(By.CSS_SELECTOR, selector_date)
            info_list.append(navi_date.text)
            for info_kind in [2, 3, 4]:
                if info_kind == 2:
                    for kind in [1, 6, 11]:
                        info_selector = f'#container > div.sub_mid.tabs_area > div > div:nth-child(2) > div > table > tbody > tr:nth-child({kind}) > td:nth-child({date+2})'
                        navi_info = driver.find_element(By.CSS_SELECTOR, info_selector)
                        info_list.append(navi_info.text)
                elif info_kind == 3:
                    for kind in [10, 16, 20]:
                        info_selector = f'#container > div.sub_mid.tabs_area > div > div:nth-child(3) > div > table > tbody > tr:nth-child({kind}) > td:nth-child({date+2})'
                        navi_info = driver.find_element(By.CSS_SELECTOR, info_selector)
                        info_list.append(navi_info.text)
                elif info_kind == 4:
                    for kind in [1, 2, 3]:
                        info_selector = f'#container > div.sub_mid.tabs_area > div > div:nth-child(4) > div > table > tbody > tr:nth-child({kind}) > td:nth-child({date+2})'
                        navi_info = driver.find_element(By.CSS_SELECTOR, info_selector)
                        info_list.append(navi_info.text)
            list.append(info_list)

                

    except Exception as e:
        print(f'정보 찾지 못함 : {e}')
        info_list.append(np.nan)
        list.append(info_list)
    print(list)
    return list

def connect_link():

    list = []
    for i in range(5):
        ticker = basic_file.loc[i+481][2]
        driver.get(f"https://www.choicestock.co.kr/search/financials/{ticker}/MRQ")
        time.sleep(1)
  
        try:
            info_list = take_detail_info(25, ticker)
            list.extend(info_list)
            print(f'{i+1}번째 완료')

        except Exception as e:
            print(f"클릭 중 오류 발생: {e}")
            print(f'{i+1}번째 실패')
    
    make_df(list)    


            
            

    
        
        

def make_df(df):
    columns = ['Ticker', 'Quarter', '매출액', '영업이익', '순이익', '자산총액', '부채총액', '자본총액', '영업활동', '투자활동', '재무활동']
    shit = pd.DataFrame(df, columns=columns)
    shit.to_csv('all_money_info_5.csv', index=False)
    print("데이터 저장 완료: money_info.csv")

    


connect_link()