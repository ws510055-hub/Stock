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
TARGET_URL = "https://goodinfo.tw/tw/StockList.asp?RPT_TIME=&MARKET_CAT=%E6%99%BA%E6%85%A7%E9%81%B8%E8%82%A1&INDUSTRY_CAT=%E6%97%A5KD%E4%BD%8E%E6%96%BC20%E9%BB%83%E9%87%91%E4%BA%A4%E5%8F%89%40%40%E6%97%A5KD%E7%9B%B8%E4%BA%92%E4%BA%A4%E5%8F%89%40%40KD%E4%BD%8E%E6%96%BC20%E9%BB%83%E9%87%91%E4%BA%A4%E5%8F%89"

def get_goodinfo_data_selenium():
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