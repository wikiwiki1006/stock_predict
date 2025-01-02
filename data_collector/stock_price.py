from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd
import os
import numpy as np


driver = webdriver.Chrome()


current_path = os.path.dirname(__file__)
file_path = os.path.join(current_path, '/Users/shin-yoonhwan/vscode/stock_data/data/basic_data/final_ticker.csv')
basic_file = pd.read_csv(file_path, index_col=None)



def take_detail_info(len_date, ticker): # len_date -> 분기 개수 선택
    list = []
    info_list = [ticker]
    for info_kind in [1, 5, 7]:
        try:
            selector = f'#nimbus-app > section > section > section > article > div:nth-child(2) > div.table-container.yf-j5d1ld > table > tbody > tr > td:nth-child({info_kind})'
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
    quarter = ['1724976000&period2=1725321600', '1716768000&period2=1717372800', '1708992000&period2=1709424000', '1701043200&period2=1701561600', '1693094400&period2=1693699200', '1685145600&period2=1685750400','1677456000&period2=1677801600', '1669507200&period2=1670025600', '1661558400&period2=1662163200', '1653609600&period2=1654214400','1645920000&period2=1646265600','1637971200&period2=1638489600','1630022400&period2=1630627200','1622073600&period2=1622678400','1614384000&period2=1614729600','1606435200&period2=1606953600','1598486400&period2=1599091200','1590537600&period2=1591142400','1582761600&period2=1583193600','1574812800&period2=1575331200','1566864000&period2=1567468800','1558915200&period2=1559520000','1551225600&period2=1551571200','1543276800&period2=1543795200','1535328000&period2=1535932800']
    for i in range(100):
        if i % 6 == 0:
            list =[]
            print('리스트 클리어')
        for j in quarter:
            ticker = basic_file.loc[i+54][0]
            driver.get(f"https://finance.yahoo.com/quote/{ticker}/history/?frequency=1mo&period1={j}")
            time.sleep(1)
    
            try:
                info_list = take_detail_info(25, ticker)
                list.extend(info_list)

            except Exception as e:
                print(f"클릭 중 오류 발생: {e}")
                print('새로고침 해주세요')
                


        make_df(list, i, ticker)
            
            

    
        
        

def make_df(df, i, ticker):
    columns = ['Ticker','Quarter', 'price', 'volume']
    shit = pd.DataFrame(df, columns=columns)
    shit.to_csv(f'temporary_stock_volume.csv', index=False)
    if i % 6 == 5:
        shit.to_csv(f'to{ticker}_stock_volume.csv', index=False)
        print('새 파일 저장완료')
    print("데이터 저장 완료: stock_volume.csv")

    


connect_link()