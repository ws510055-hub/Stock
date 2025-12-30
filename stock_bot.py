import time
import pandas as pd
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import urllib3

# 忽略 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 您的 LINE 設定 ---
LINE_ACCESS_TOKEN = 'EbEgyG52sePy8BeieKun2lHDJDBLr9N8H9ORHORCZd6vAhSYaTr8raat3W2sVHImc7kdTATt0uq2+kMPB0SUEL2PO26hegmO6oxMRruuqNmIdujHEsS7heVbOFtnC0+mFOepeixszQkywbXhTz2TEwdB04t89/1O/w1cDnyilFU='
LINE_USER_ID = 'U7f344cc462b486e48afcd88dc3a64343'

# --- Goodinfo 設定 ---
TARGET_URL = "https://goodinfo.tw/tw/StockList.asp?SEARCH_WORD=&SHEET=%E4%BA%A4%E6%98%93%E7%8B%80%E6%B3%81&SHEET2=%E6%97%A5&RPT_TIME=%E6%9C%80%E6%96%B0%E8%B3%87%E6%96%99&MARKET_CAT=%E8%87%AA%E8%A8%82%E7%AF%A9%E9%81%B8&INDUSTRY_CAT=%E6%88%91%E7%9A%84%E6%A2%9D%E4%BB%B6&STOCK_CODE=&RANK=0&SORT_FIELD=%5B%E6%88%90%E4%BA%A4%5D&SORT=DOWN&FL_SHEET=%E4%BA%A4%E6%98%93%E7%8B%80%E6%B3%81&FL_SHEET2=%E6%97%A5&FL_MARKET=%E4%B8%8A%E5%B8%82%2F%E4%B8%8A%E6%AB%83&FL_ITEM0=&FL_VAL_S0=&FL_VAL_E0=&FL_VAL_CHK0=&FL_ITEM1=&FL_VAL_S1=&FL_VAL_E1=&FL_VAL_CHK1=&FL_ITEM2=&FL_VAL_S2=&FL_VAL_E2=&FL_VAL_CHK2=&FL_ITEM3=&FL_VAL_S3=&FL_VAL_E3=&FL_VAL_CHK3=&FL_ITEM4=&FL_VAL_S4=&FL_VAL_E4=&FL_VAL_CHK4=&FL_ITEM5=&FL_VAL_S5=&FL_VAL_E5=&FL_VAL_CHK5=&FL_ITEM6=&FL_VAL_S6=&FL_VAL_E6=&FL_VAL_CHK6=&FL_ITEM7=&FL_VAL_S7=&FL_VAL_E7=&FL_VAL_CHK7=&FL_ITEM8=&FL_VAL_S8=&FL_VAL_E8=&FL_VAL_CHK8=&FL_ITEM9=&FL_VAL_S9=&FL_VAL_E9=&FL_VAL_CHK9=&FL_ITEM10=&FL_VAL_S10=&FL_VAL_E10=&FL_VAL_CHK10=&FL_ITEM11=&FL_VAL_S11=&FL_VAL_E11=&FL_VAL_CHK11=&FL_RULE0=KD%7C%7C%E6%97%A5KD%E9%BB%83%E9%87%91%E4%BA%A4%E5%8F%89%40%40%E6%97%A5KD%E7%9B%B8%E4%BA%92%E4%BA%A4%E5%8F%89%40%40KD%E9%BB%83%E9%87%91%E4%BA%A4%E5%8F%89&FL_RULE_CHK0=&FL_RULE1=&FL_RULE_CHK1=&FL_RULE2=&FL_RULE_CHK2=&FL_RULE3=&FL_RULE_CHK3=&FL_RULE4=&FL_RULE_CHK4=&FL_RULE5=&FL_RULE_CHK5=&FL_RANK0=&FL_RANK1=&FL_RANK2=&FL_RANK3=&FL_RANK4=&FL_RANK5=&FL_FD0=%E6%88%90%E4%BA%A4%E5%BC%B5%E6%95%B8+%28%E5%BC%B5%29%7C%7C1%7C%7C0%7C%7C%3E%7C%7C%E6%97%A5%E5%9D%87%E6%88%90%E4%BA%A4%E5%BC%B5%E6%95%B8%28%E5%BC%B5%29%E2%80%93%E8%BF%915%E6%97%A5%7C%7C1%7C%7C0&FL_FD1=%E6%88%90%E4%BA%A4%E5%83%B9+%28%E5%85%83%29%7C%7C1%7C%7C0%7C%7C%3E%7C%7C%E5%9D%87%E7%B7%9A%E4%BD%8D%E7%BD%AE%28%E5%85%83%29%E2%80%9320%E6%97%A5%7C%7C1%7C%7C0&FL_FD2=%7C%7C1%7C%7C0%7C%7C%3D%7C%7C%7C%7C1%7C%7C0&FL_FD3=%7C%7C1%7C%7C0%7C%7C%3D%7C%7C%7C%7C1%7C%7C0&FL_FD4=%7C%7C1%7C%7C0%7C%7C%3D%7C%7C%7C%7C1%7C%7C0&FL_FD5=%7C%7C1%7C%7C0%7C%7C%3D%7C%7C%"m():
    print("🚀 啟動 Selenium 瀏覽器 (雲端模式)...")
    
    chrome_options = Options()
    # --- 雲端執行關鍵設定 ---
    chrome_options.add_argument("--headless") # 雲端無螢幕，必須開啟
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print(f"🔗 前往 Goodinfo: {TARGET_URL}")
        driver.get(TARGET_URL)
        time.sleep(10) # 雲端網路有時較慢，延長等待
        
        print("📥 正在讀取網頁表格...")
        dfs = pd.read_html(driver.page_source)
        
        target_df = None
        for df in dfs:
            if '名稱' in str(df.columns) and '成交' in str(df.columns) and 'K值' in str(df.columns):
                target_df = df
                break
        
        if target_df is None:
            print("❌ 找不到表格")
            return None

        # 資料清理
        df = target_df.copy()
        df = df[df['名稱'] != '名稱']
        
        # 簡易欄位名稱處理
        df.columns = [str(c).replace("('", "").replace("')", "").replace(",", "") for c in df.columns]
        
        for col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '').str.replace('↗', '').str.replace('↘', '').str.replace('+', '')
        
        # 動態尋找欄位
        vol_col = [c for c in df.columns if '張數' in c][0]
        price_col = [c for c in df.columns if '成交' in c and '張' not in c and '值' not in c][0]
        k_col = [c for c in df.columns if 'K值' in c][0]
        
        df[vol_col] = pd.to_numeric(df[vol_col], errors='coerce')
        df[price_col] = pd.to_numeric(df[price_col], errors='coerce')
        df[k_col] = pd.to_numeric(df[k_col], errors='coerce')
        
        return df, vol_col, price_col, k_col

    except Exception as e:
        print(f"❌ Selenium 錯誤: {e}")
        return None
    finally:
        driver.quit()

def filter_best_stocks(df, vol_col, price_col, k_col):
    filtered = df[
        (df[vol_col] > 1000) & 
        (df[price_col] > 10)
    ].copy()
    return filtered.sort_values(by=vol_col, ascending=False).head(3)

def send_line(msg):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
    }
    payload = {'to': LINE_USER_ID, 'messages': [{'type': 'text', 'text': msg}]}
    try:
        requests.post('https://api.line.me/v2/bot/message/push', headers=headers, data=json.dumps(payload), verify=False)
        print("✅ LINE 訊息已發送")
    except Exception as e:
        print(f"❌ 發送失敗: {e}")

def main():
    result = get_goodinfo_data_selenium()
    if result is None:
        send_line("⚠️ Goodinfo 雲端抓取失敗。")
        return
        
    df, vol_col, price_col, k_col = result
    best_stocks = filter_best_stocks(df, vol_col, price_col, k_col)
    
    if best_stocks.empty:
        send_line("📊 今日無量大(>1000張)之 KD 低檔金叉股。")
        return
        
    msg = "☁️ 【雲端自動選股報告】\n"
    msg += "策略：KD低檔金叉 + 量大前3名\n\n"
    
    rank = 1
    for index, row in best_stocks.iterrows():
        name = row['名稱'] if '名稱' in row else "未知"
        code = row['代號'] if '代號' in row else ""
        price = row[price_col]
        vol = row[vol_col]
        k_val = row[k_col]
        
        msg += f"{rank}. {name} ({code})\n"
        msg += f"   💰 股價: {price}\n"
        msg += f"   🔥 張數: {int(vol)}\n"
        msg += f"   📈 K值: {k_val}\n\n"
        rank += 1
        
    msg += "(Github Actions 自動發送)"
    send_line(msg)

if __name__ == "__main__":

    main()

