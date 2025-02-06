from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os
import numpy as np


driver = webdriver.Chrome()


file_path = ('/Users/shin-yoonhwan/vscode/stock_data/data/proceeded_data/filled_na.csv')
basic_df = pd.read_csv(file_path, index_col=None)
basic_file = pd.DataFrame(basic_df['Ticker'].unique().tolist())




def take_detail_info(len_date, ticker): # len_date -> 분기 개수 선택
    list = []
    for date in range(len_date):
        info_list = [ticker]
        selector_date = f'#container > div.sub_mid.tabs_area > div > div.scroll_table_wrap > div > table > thead > tr > th:nth-child({date+3}) > span'
        navi_date = driver.find_element(By.CSS_SELECTOR, selector_date)
        info_list.append(navi_date.text)
        for info_kind in [1, 2, 6, 7, 10, 11 ,12, 13]:
            try:
                selector = f'#container > div.sub_mid.tabs_area > div > div.scroll_table_wrap > div > table > tbody > tr:nth-child({info_kind}) > td:nth-child({date+3})'
                navi = driver.find_element(By.CSS_SELECTOR, selector)
                info = navi.text
                info_list.append(info)
            except Exception as e:
                print(f'정보 찾지 못함 : {e}')
                info_list.append(np.nan)
        list.append(info_list)
    print(list)
    return list

def connect_link():

    list = []
    for i in range(3):
        time.sleep(3)
        ticker = basic_file.loc[0][i]
        driver.get(f"https://www.choicestock.co.kr/search/invest/{ticker}/MRQ")
        time.sleep(1)
  
        try:
            info_list = take_detail_info(25, ticker)
            list.extend(info_list)

        except Exception as e:
            print(f"클릭 중 오류 발생: {e}")
            print('새로고침 해주세요')
                


    make_df(list)
            
            

    
        
        

def make_df(df):
    columns = ['Ticker', 'Quarter', 'EPS', 'BPS', 'PER', 'PBR', 'ROE', 'ROA', 'ROIC', 'Debt_ratio']
    shit = pd.DataFrame(df, columns=columns)
    shit.to_csv('test_detail.csv', index=False)
    print("데이터 저장 완료: detail_data.csv")

    


connect_link()