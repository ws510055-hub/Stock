import time
import pandas as pd
import requests
import json
import yfinance as yf
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import urllib3

# 忽略 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# --- 設定區 ---
LINE_ACCESS_TOKEN = 'EbEgyG52sePy8BeieKun2lHDJDBLr9N8H9ORHORCZd6vAhSYaTr8raat3W2sVHImc7kdTATt0uq2+kMPB0SUEL2PO26hegmO6oxMRruuqNmIdujHEsS7heVbOFtnC0+mFOepeixszQkywbXhTz2TEwdB04t89/1O/w1cDnyilFU='
LINE_USER_ID = 'U7f344cc462b486e48afcd88dc3a64343'

# Goodinfo 篩選網址
TARGET_URL = "https://goodinfo.tw/tw/StockList.asp?SEARCH_WORD=&SHEET=%E4%BA%A4%E6%98%93%E7%8B%80%E6%B3%81&SHEET2=%E6%97%A5&RPT_TIME=%E6%9C%80%E6%96%B0%E8%B3%87%E6%96%99&MARKET_CAT=%E8%87%AA%E8%A8%82%E7%AF%A9%E9%81%B8&INDUSTRY_CAT=%E6%88%91%E7%9A%84%E6%A2%9D%E4%BB%B6&STOCK_CODE=&RANK=0&SORT_FIELD=%5B%E6%88%90%E4%BA%A4%5D&SORT=DOWN&FL_SHEET=%E4%BA%A4%E6%98%93%E7%8B%80%E6%B3%81&FL_SHEET2=%E6%97%A5&FL_MARKET=%E4%B8%8A%E5%B8%82%2F%E4%B8%8A%E6%AB%83&FL_ITEM0=&FL_VAL_S0=&FL_VAL_E0=&FL_VAL_CHK0=&FL_ITEM1=&FL_VAL_S1=&FL_VAL_E1=&FL_VAL_CHK1=&FL_ITEM2=&FL_VAL_S2=&FL_VAL_E2=&FL_VAL_CHK2=&FL_ITEM3=&FL_VAL_S3=&FL_VAL_E3=&FL_VAL_CHK3=&FL_ITEM4=&FL_VAL_S4=&FL_VAL_E4=&FL_VAL_CHK4=&FL_ITEM5=&FL_VAL_S5=&FL_VAL_E5=&FL_VAL_CHK5=&FL_ITEM6=&FL_VAL_S6=&FL_VAL_E6=&FL_VAL_CHK6=&FL_ITEM7=&FL_VAL_S7=&FL_VAL_E7=&FL_VAL_CHK7=&FL_ITEM8=&FL_VAL_S8=&FL_VAL_E8=&FL_VAL_CHK8=&FL_ITEM9=&FL_VAL_S9=&FL_VAL_E9=&FL_VAL_CHK9=&FL_ITEM10=&FL_VAL_S10=&FL_VAL_E10=&FL_VAL_CHK10=&FL_ITEM11=&FL_VAL_S11=&FL_VAL_E11=&FL_VAL_CHK11=&FL_RULE0=KD%7C%7C%E6%97%A5KD%E9%BB%83%E9%87%91%E4%BA%A4%E5%8F%89%40%40%E6%97%A5KD%E7%9B%B8%E4%BA%92%E4%BA%A4%E5%8F%89%40%40KD%E9%BB%83%E9%87%91%E4%BA%A4%E5%8F%89&FL_RULE_CHK0=&FL_RULE1=&FL_RULE_CHK1=&FL_RULE2=&FL_RULE_CHK2=&FL_RULE3=&FL_RULE_CHK3=&FL_RULE4=&FL_RULE_CHK4=&FL_RULE5=&FL_RULE_CHK5=&FL_RANK0=&FL_RANK1=&FL_RANK2=&FL_RANK3=&FL_RANK4=&FL_RANK5=&FL_FD0=%E6%88%90%E4%BA%A4%E5%BC%B5%E6%95%B8+%28%E5%BC%B5%29%7C%7C1%7C%7C0%7C%7C%3E%7C%7C%E6%97%A5%E5%9D%87%E6%88%90%E4%BA%A4%E5%BC%B5%E6%95%B8%28%E5%BC%B5%29%E2%80%93%E8%BF%915%E6%97%A5%7C%7C1%7C%7C0&FL_FD1=%E6%88%90%E4%BA%A4%E5%83%B9+%28%E5%85%83%29%7C%7C1%7C%7C0%7C%7C%3E%7C%7C%E5%9D%87%E7%B7%9A%E4%BD%8D%E7%BD%AE%28%E5%85%83%29%E2%80%9320%E6%97%A5%7C%7C1%7C%7C0&FL_FD2=%7C%7C1%7C%7C0%7C%7C%3D%7C%7C%7C%7C1%7C%7C0&FL_FD3=%7C%7C1%7C%7C0%7C%7C%3D%7C%7C%7C%7C1%7C%7C0&FL_FD4=%7C%7C1%7C%7C0%7C%7C%3D%7C%7C%7C%7C1%7C%7C0&FL_FD5=%7C%7C1%7C%7C0%7C%7C%3D%7C%7C%7C%7C1%7C%7C0&MY_FL_RULE_NM=123"

# 熱門題材
HOT_KEYWORDS = [
    '半導體', 'AI', '伺服器', '散熱', '機器人', 
    '航運', '重電', '能源', '矽光子', 'CoWoS', 
    '蘋果', '車用', 'IC設計', '記憶體'
]

def send_line(msg):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
    }
    payload = {'to': LINE_USER_ID, 'messages': [{'type': 'text', 'text': msg}]}
    # 包在 try-except 避免連網路失敗程式崩潰
    try:
        requests.post('https://api.line.me/v2/bot/message/push', headers=headers, data=json.dumps(payload), verify=False)
    except:
        pass

def get_goodinfo_data_selenium():
    print("🚀 啟動 Selenium...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless") 
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        print("🔗 連線 Goodinfo...")
        driver.get(TARGET_URL)
        time.sleep(15) # 等待載入
        
        # 1. 檢查網頁標題 (Debug 用)
        print(f"📄 Page Title: {driver.title}")
        if "Access Denied" in driver.title or "無法連上" in driver.title:
            return "BLOCKED", None, None, None

        # 2. 嘗試讀取表格
        try:
            dfs = pd.read_html(driver.page_source)
        except ValueError:
            return "NO_TABLE", None, None, None
        
        target_df = None
        for df in dfs:
            if '名稱' in str(df.columns) and '成交' in str(df.columns):
                target_df = df
                break
        
        if target_df is None:
            return "NO_MATCH", None, None, None

        # 3. 資料清理
        df = target_df.copy()
        df = df[df['名稱'] != '名稱']
        df.columns = [str(c).replace("('", "").replace("')", "").replace(",", "") for c in df.columns]
        
        for col in df.columns:
            df[col] = df[col].astype(str).str.replace(',', '').str.replace('+', '').str.replace('↘', '').str.replace('↗', '')
        
        # 4. 找欄位
        try:
            vol_col = [c for c in df.columns if '張數' in c][0]
            price_col = [c for c in df.columns if '成交' in c and '張' not in c and '值' not in c][0]
            
            df[vol_col] = pd.to_numeric(df[vol_col], errors='coerce')
            df[price_col] = pd.to_numeric(df[price_col], errors='coerce')
            
            return "SUCCESS", df, vol_col, price_col
        except:
            return "COL_ERROR", None, None, None

    except Exception as e:
        print(f"❌ Selenium Error: {e}")
        return "ERROR", None, None, None
    finally:
        driver.quit()

def check_theme_score(row, vol_col):
    name = str(row['名稱'])
    vol = row[vol_col]
    score = vol / 10000 
    tag = ""
    
    # 檢查股名是否命中關鍵字
    for k in HOT_KEYWORDS:
        if k in name:
            score += 10
            tag = k
            break
    return score, tag

def get_sector_from_yf(code):
    # 輔助函式：用 yfinance 查產業 (加上防呆)
    try:
        ticker = yf.Ticker(f"{code}.TW")
        # 簡單檢查一下是否有 news，有就代表抓到了
        if ticker.news:
            return ticker.news[0]['title']
        
        # 沒抓到試試看上櫃
        ticker = yf.Ticker(f"{code}.TWO")
        if ticker.news:
            return ticker.news[0]['title']
    except:
        pass
    return ""

def main():
    print("開始執行...")
    status, df, vol_col, price_col = get_goodinfo_data_selenium()
    
    today = time.strftime("%Y/%m/%d")

    # --- 錯誤處理區 (傳 LINE 告知失敗原因) ---
    if status == "BLOCKED":
        send_line(f"⚠️ {today} 執行失敗：雲端 IP 被 Goodinfo 封鎖。")
        return
    elif status == "NO_TABLE" or status == "NO_MATCH":
        send_line(f"📊 {today} 策略執行完成：今日無符合「KD金叉+爆量+站月線」之股票。")
        return
    elif status != "SUCCESS":
        send_line(f"⚠️ {today} 執行錯誤，代碼: {status}。請檢查 GitHub Logs。")
        return
        
    # --- 成功取得資料，開始分析 ---
    # 1. 初步過濾
    candidates = df[(df[vol_col] > 800) & (df[price_col] > 10)].copy()
    
    if candidates.empty:
        send_line(f"📊 {today} 篩選後無量大(>800張)標的。")
        return

    # 2. 取前 15 名做詳細檢查
    top_15 = candidates.sort_values(by=vol_col, ascending=False).head(15)
    
    final_list = []
    
    for index, row in top_15.iterrows():
        code = row['代號']
        name = row['名稱']
        
        score, tag = check_theme_score(row, vol_col)

        # 🔥 ETF 殺手邏輯 🔥
        # 1. 踢掉 '0' 開頭 (如 0050, 00940)
        # 2. 踢掉長度不是 4 碼的 (權證、特別股、債券)
        if code.startswith('0') or len(code) != 4:
            continue
        
        # 如果沒標籤，用 yfinance 查新聞 (只查前15名避免超時)
        if not tag:
            news_title = get_sector_from_yf(code)
            for k in HOT_KEYWORDS:
                if k in news_title:
                    score += 5
                    tag = k
                    break
        
        final_list.append({
            'code': code,
            'name': name,
            'price': row[price_col],
            'vol': row[vol_col],
            'score': score,
            'tag': tag
        })
        
    # 3. 排序取前 3
    final_df = pd.DataFrame(final_list)
    best_3 = final_df.sort_values(by='score', ascending=False).head(3)

    msg = f"🔥 【Goodinfo 強勢題材股】 {today}\n"
    msg += "策略：KD金叉 + 爆量 + 站月線 + 題材\n\n"
    
    for idx, row in best_3.iterrows():
        icon = "🔥" if row['tag'] else "🔴"
        tag_str = f"[{row['tag']}]" if row['tag'] else ""
        
        msg += f"{icon} {row['name']} ({row['code']}) {tag_str}\n"
        msg += f"   💰 股價: {row['price']}\n"
        msg += f"   📊 張數: {int(row['vol'])}\n"
        msg += f"   🚀 訊號: 強勢起漲\n\n"
        
    msg += "(Github Actions 自動執行)"
    send_line(msg)
    print("執行完成，已發送 LINE。")

if __name__ == "__main__":
    main()
