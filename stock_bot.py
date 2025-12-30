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

# --- 設定 ---
LINE_ACCESS_TOKEN = 'EbEgyG52sePy8BeieKun2lHDJDBLr9N8H9ORHORCZd6vAhSYaTr8raat3W2sVHImc7kdTATt0uq2+kMPB0SUEL2PO26hegmO6oxMRruuqNmIdujHEsS7heVbOFtnC0+mFOepeixszQkywbXhTz2TEwdB04t89/1O/w1cDnyilFU='
LINE_USER_ID = 'U7f344cc462b486e48afcd88dc3a64343'

# 您的自訂篩選網址
TARGET_URL = "https://goodinfo.tw/tw/StockList.asp?SEARCH_WORD=&SHEET=%E4%BA%A4%E6%98%93%E7%8B%80%E6%B3%81&SHEET2=%E6%97%A5&RPT_TIME=%E6%9C%80%E6%96%B0%E8%B3%87%E6%96%99&MARKET_CAT=%E8%87%AA%E8%A8%82%E7%AF%A9%E9%81%B8&INDUSTRY_CAT=%E6%88%91%E7%9A%84%E6%A2%9D%E4%BB%B6&STOCK_CODE=&RANK=0&SORT_FIELD=%5B%E6%88%90%E4%BA%A4%5D&SORT=DOWN&FL_SHEET=%E4%BA%A4%E6%98%93%E7%8B%80%E6%B3%81&FL_SHEET2=%E6%97%A5&FL_MARKET=%E4%B8%8A%E5%B8%82%2F%E4%B8%8A%E6%AB%83&FL_ITEM0=&FL_VAL_S0=&FL_VAL_E0=&FL_VAL_CHK0=&FL_ITEM1=&FL_VAL_S1=&FL_VAL_E1=&FL_VAL_CHK1=&FL_ITEM2=&FL_VAL_S2=&FL_VAL_E2=&FL_VAL_CHK2=&FL_ITEM3=&FL_VAL_S3=&FL_VAL_E3=&FL_VAL_CHK3=&FL_ITEM4=&FL_VAL_S4=&FL_VAL_E4=&FL_VAL_CHK4=&FL_ITEM5=&FL_VAL_S5=&FL_VAL_E5=&FL_VAL_CHK5=&FL_ITEM6=&FL_VAL_S6=&FL_VAL_E6=&FL_VAL_CHK6=&FL_ITEM7=&FL_VAL_S7=&FL_VAL_E7=&FL_VAL_CHK7=&FL_ITEM8=&FL_VAL_S8=&FL_VAL_E8=&FL_VAL_CHK8=&FL_ITEM9=&FL_VAL_S9=&FL_VAL_E9=&FL_VAL_CHK9=&FL_ITEM10=&FL_VAL_S10=&FL_VAL_E10=&FL_VAL_CHK10=&FL_ITEM11=&FL_VAL_S11=&FL_VAL_E11=&FL_VAL_CHK11=&FL_RULE0=KD%7C%7C%E6%97%A5KD%E9%BB%83%E9%87%91%E4%BA%A4%E5%8F%89%40%40%E6%97%A5KD%E7%9B%B8%E4%BA%92%E4%BA%A4%E5%8F%89%40%40KD%E9%BB%83%E9%87%91%E4%BA%A4%E5%8F%89&FL_RULE_CHK0=&FL_RULE1=&FL_RULE_CHK1=&FL_RULE2=&FL_RULE_CHK2=&FL_RULE3=&FL_RULE_CHK3=&FL_RULE4=&FL_RULE_CHK4=&FL_RULE5=&FL_RULE_CHK5=&FL_RANK0=&FL_RANK1=&FL_RANK2=&FL_RANK3=&FL_RANK4=&FL_RANK5=&FL_FD0=%E6%88%90%E4%BA%A4%E5%BC%B5%E6%95%B8+%28%E5%BC%B5%29%7C%7C1%7C%7C0%7C%7C%3E%7C%7C%E6%97%A5%E5%9D%87%E6%88%90%E4%BA%A4%E5%BC%B5%E6%95%B8%28%E5%BC%B5%29%E2%80%93%E8%BF%915%E6%97%A5%7C%7C1%7C%7C0&FL_FD1=%E6%88%90%E4%BA%A4%E5%83%B9+%28%E5%85%83%29%7C%7C1%7C%7C0%7C%7C%3E%7C%7C%E5%9D%87%E7%B7%9A%E4%BD%8D%E7%BD%AE%28%E5%85%83%29%E2%80%9320%E6%97%A5%7C%7C1%7C%7C0&FL_FD2=%7C%7C1%7C%7C0%7C%7C%3D%7C%7C%7C%7C1%7C%7C0&FL_FD3=%7C%7C1%7C%7C0%7C%7C%3D%7C%7C%7C%7C1%7C%7C0&FL_FD4=%7C%7C1%7C%7C0%7C%7C%3D%7C%7C%7C%7C1%7C%7C0&FL_FD5=%7C%7C1%7C%7C0%7C%7C%3D%7C%7C%7C%7C1%7C%7C0&MY_FL_RULE_NM=123"

def get_goodinfo_data_selenium():
    print("🚀 啟動 Selenium (除錯模式)...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080") # 設定視窗大小，避免跑版
    chrome_options.add_argument("--disable-blink-features=AutomationControlled") # 嘗試避開偵測
    # 模擬真實瀏覽器 Header
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    chrome_options.add_argument("--accept-lang=zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print("🔗 前往 Goodinfo...")
        driver.get(TARGET_URL)
        time.sleep(15) # 等待更久一點
        
        # 除錯關鍵：印出網頁標題
        print(f"📄 網頁標題: {driver.title}")
        
        # 檢查是否被擋
        if "Access Denied" in driver.title or "無法連上" in driver.title:
            return "BLOCKED", None, None, None

        print("📥 正在讀取網頁表格...")
        try:
            dfs = pd.read_html(driver.page_source)
        except ValueError:
            # 這通常代表找不到表格 (可能今日無符合股票)
            return "NO_TABLE", None, None, None
        
        target_df = None
        for df in dfs:
            if '名稱' in str(df.columns) and '成交' in str(df.columns):
                target_df = df
                break
        
        if target_df is None:
            return "NO_MATCH", None, None, None

        # 資料清理
        df = target_df.copy()
        df = df[df['名稱'] != '名稱']
        df.columns = [str(c).replace("('", "").replace("')", "").replace(",", "") for c in df.columns]
        
        for col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '').str.replace('+', '').str.replace('↘', '').str.replace('↗', '')
        
        try:
            vol_col = [c for c in df.columns if '張數' in c][0]
            price_col = [c for c in df.columns if '成交' in c and '張' not in c and '值' not in c][0]
        except:
            return "COL_ERROR", None, None, None
        
        df[vol_col] = pd.to_numeric(df[vol_col], errors='coerce')
        df[price_col] = pd.to_numeric(df[price_col], errors='coerce')
        
        return "SUCCESS", df, vol_col, price_col

    except Exception as e:
        print(f"❌ Selenium 嚴重錯誤: {e}")
        return "ERROR", None, None, None
    finally:
        driver.quit()

def send_line(msg):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
    }
    payload = {'to': LINE_USER_ID, 'messages': [{'type': 'text', 'text': msg}]}
    requests.post('https://api.line.me/v2/bot/message/push', headers=headers, data=json.dumps(payload), verify=False)

def main():
    status, df, vol_col, price_col = get_goodinfo_data_selenium()
    
    print(f"執行狀態代碼: {status}")
    
    today = time.strftime("%Y/%m/%d")

    if status == "BLOCKED":
        send_line(f"⚠️ {today} 失敗：Goodinfo 封鎖了雲端 IP，請改用本機執行。")
        return
    elif status == "NO_TABLE" or status == "NO_MATCH":
        send_line(f"📊 {today} 策略執行完成：\n今日無任何股票符合「KD金叉+爆量+站上月線」。")
        return
    elif status == "ERROR" or status == "COL_ERROR":
        send_line(f"⚠️ {today} 程式執行錯誤，請檢查 GitHub Logs。")
        return
        
    # 成功取得資料，開始排序
    filtered = df[(df[vol_col] > 500) & (df[price_col] > 10)].copy()
    best_stocks = filtered.sort_values(by=vol_col, ascending=False).head(3)
    
    if best_stocks.empty:
        send_line(f"📊 {today} 策略有抓到股票，但成交量皆過低 (<500張)。")
        return

    msg = f"🔥 【Goodinfo 強勢策略】 {today}\n"
    msg += "條件：KD金叉 + 爆量 + 站上月線\n\n"
    
    rank = 1
    for index, row in best_stocks.iterrows():
        name = row['名稱']
        code = row['代號']
        price = row[price_col]
        vol = row[vol_col]
        
        msg += f"{rank}. {name} ({code})\n"
        msg += f"   💰 股價: {price}\n"
        msg += f"   📊 張數: {int(vol)}\n\n"
        rank += 1
        
    msg += "(Github Actions 自動執行)"
    send_line(msg)

if __name__ == "__main__":
    main()
