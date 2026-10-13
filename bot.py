import sys
import time
import requests
import json

# TELEGRAM BOT CONFIG
BOT_TOKEN = "8662159068:AAE-FHz_SeJWVLXonnWX7piNRzYl3DLLArw"
CHAT_ID = "-1004446531098"

# Target wins parameter (Default 10)
TARGET_WINS = int(sys.argv[1]) if len(sys.argv) > 1 else 10

API_URL = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json?pageNo=1&pageSize=10"

# Real browser spoof headers
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://dhaniwin0.com",
    "Referer": "https://dhaniwin0.com/",
    "Sec-Ch-Ua": '"Not-A.Brand";v="99", "Chromium";v="124"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "cross-site"
}

session = requests.Session()
session.headers.update(HEADERS)

def tg_send(text):
    try:
        r = requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text, "parse_mode": "HTML"},
            timeout=10
        )
        data = r.json()
        if data.get("ok"):
            return data["result"]["message_id"]
        print(f"TG Send Error: {data}")
    except Exception as e:
        print(f"TG Send Exception: {e}")
    return None

def tg_edit(msg_id, text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText",
            json={"chat_id": CHAT_ID, "message_id": msg_id, "text": text, "parse_mode": "HTML"},
            timeout=10
        )
    except Exception as e:
        print(f"TG Edit Exception: {e}")

def fetch_history():
    # Method 1: Direct fetch with browser headers
    try:
        r = session.get(API_URL, timeout=6)
        if r.status_code == 200:
            data = r.json()
            items = data.get("data", {}).get("list") or data.get("list") or []
            if items:
                return items
    except Exception:
        pass

    # Method 2: High-speed proxy fallback
    try:
        r2 = requests.get(f"https://api.allorigins.win/raw?url={API_URL}", timeout=6)
        if r2.status_code == 200:
            data = r2.json()
            if isinstance(data, str):
                data = json.loads(data)
            items = data.get("data", {}).get("list") or data.get("list") or []
            if items:
                return items
    except Exception:
        pass

    return []

def calculate_2738(history):
    latest_num = int(history[0]["number"])
    count = 5 if (latest_num % 2 != 0) else 6
    num_str = "".join([str(history[i]["number"]) for i in range(min(count, len(history)))])
    
    divisor = int(num_str) if int(num_str or 0) > 0 else 1
    scaled = (2738 * (10**24)) // divisor
    dec_str = str(scaled).zfill(24)[:20]
    
    big_digits = [int(c) for c in dec_str if int(c) >= 5]
    small_digits = [int(c) for c in dec_str if int(c) < 5]
    
    if len(big_digits) >= len(small_digits):
        pred_size = "BIG"
        freq = {d: big_digits.count(d) for d in set(big_digits)}
        sorted_d = sorted([5, 6, 7, 8, 9], key=lambda x: freq.get(x, 0), reverse=True)
        hot = sorted_d[:2]
        chosen = hot[0]
    else:
        pred_size = "SMALL"
        freq = {d: small_digits.count(d) for d in set(small_digits)}
        sorted_d = sorted([0, 1, 2, 3, 4], key=lambda x: freq.get(x, 0), reverse=True)
        hot = sorted_d[:2]
        chosen = hot[0]
        
    return pred_size, hot, chosen, dec_str

def main():
    print(f"Session starting on GitHub Cloud for {TARGET_WINS} wins...")
    init_card = (
        "👑 <b>CTG OFFICIAL</b> 👑\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        "🚀 <b>AKAZA VIP SESSION COMMENCED!</b>\n\n"
        f"🎯 <b>Target Goal:</b> {TARGET_WINS} Wins\n"
        "📈 <b>Strategy:</b> 2738 Ratio Engine\n"
        "👑 <i>Prepare your stakes. Starting in next round!</i>"
    )
    tg_send(init_card)
    
    wins = 0
    level = 1
    max_level = 1
    last_predicted_issue = None
    
    while wins < TARGET_WINS:
        now_sec = int(time.time()) % 60
        
        # Dispatch window :08 - :20
        if 8 <= now_sec <= 20:
            history = fetch_history()
            if history:
                curr_issue = int(history[0].get("issueNumber") or history[0].get("period"))
                target_issue = curr_issue + 1
                
                if target_issue != last_predicted_issue:
                    pred_size, hot, chosen, dec_str = calculate_2738(history)
                    pool_text = "🟢 BIG [ 5 - 9 ]" if pred_size == "BIG" else "🔴 SMALL [ 0 - 4 ]"
                    
                    card = (
                        "┏━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
                        "   👑 <b>CTG GAMING PREDICTION</b> 👑\n"
                        "┗━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
                        "  🎮 <b>SERVER :</b> WINGO 1 MIN [VIP]\n"
                        f"  🎯 <b>TARGET ISSUE :</b> #{target_issue}\n\n"
                        f"  🔮 <b>PREDICTION :</b> {pool_text}\n"
                        f"  🎲 <b>HOT NUMBERS :</b> {hot[0]} & {hot[1]}\n\n"
                        f"  📊 <b>CHOSEN DIGIT :</b> {chosen}\n"
                        f"  🔢 <b>DECIMAL (20D) :</b> 0.{dec_str[:8]}...{dec_str[-2:]}\n\n"
                        f"  ⚡ <b>CURRENT LEVEL  :</b> {level}\n"
                        f"  🔥 <b>MAX LEVEL REACHED :</b> {max_level}\n"
                        f"  🏁 <b>WIN PROGRESS :</b> {wins}/{TARGET_WINS}\n"
                        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        "  📩 <b>OFFICIAL HELP :</b> @Gara00077\n"
                        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                        "⏳ <i>Awaiting draw outcome...</i>"
                    )
                    
                    msg_id = tg_send(card)
                    last_predicted_issue = target_issue
                    print(f"Dispatched Card for #{target_issue} [{pred_size}]")
                    
                    time.sleep(35)
                    
                    resolved = False
                    for _ in range(12):
                        time.sleep(2)
                        res_hist = fetch_history()
                        if res_hist:
                            latest_issue = int(res_hist[0].get("issueNumber") or res_hist[0].get("period"))
                            if latest_issue == target_issue:
                                act_num = int(res_hist[0]["number"])
                                act_size = "BIG" if act_num >= 5 else "SMALL"
                                is_win = (act_size == pred_size)
                                is_jackpot = act_num in hot
                                
                                if is_win:
                                    wins += 1
                                    level = 1
                                    banner = f"💥 <b>JACKPOT WIN!</b> 💥 Result: {act_num} ({act_size})" if is_jackpot else f"✅ <b>WIN!</b> Result: {act_num} ({act_size})"
                                else:
                                    level += 1
                                    if level > max_level:
                                        max_level = level
                                    banner = f"❌ <b>LOSS!</b> Result: {act_num} ({act_size})"
                                
                                updated_card = (
                                    "┏━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
                                    "   👑 <b>CTG GAMING PREDICTION</b> 👑\n"
                                    "┗━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
                                    "  🎮 <b>SERVER :</b> WINGO 1 MIN [VIP]\n"
                                    f"  🎯 <b>TARGET ISSUE :</b> #{target_issue}\n\n"
                                    f"  🔮 <b>PREDICTION :</b> {pool_text}\n"
                                    f"  🎲 <b>HOT NUMBERS :</b> {hot[0]} & {hot[1]}\n\n"
                                    f"  📊 <b>CHOSEN DIGIT :</b> {chosen}\n\n"
                                    f"  {banner}\n"
                                    f"  ⚡ <b>CURRENT LEVEL  :</b> {level}\n"
                                    f"  🔥 <b>MAX LEVEL REACHED :</b> {max_level}\n"
                                    f"  🏁 <b>WIN PROGRESS :</b> {wins}/{TARGET_WINS}\n"
                                    "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                                    "  📩 <b>OFFICIAL HELP :</b> @Gara00077\n"
                                    "━━━━━━━━━━━━━━━━━━━━━━━━━━"
                                )
                                if msg_id:
                                    tg_edit(msg_id, updated_card)
                                resolved = True
                                print(f"Settled #{target_issue}: {banner}")
                                break
                    if not resolved:
                        print(f"Verification timeout for #{target_issue}")
        time.sleep(1)

    final_card = (
        "🎉 <b>SESSION TARGET COMPLETED!</b> 🎉\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🏆 <b>Total Wins:</b> {wins}/{TARGET_WINS}\n"
        f"🔥 <b>Max Level Reached:</b> {max_level}\n"
        "👑 <i>Congratulations to all VIP members!</i>"
    )
    tg_send(final_card)
    print("Session target reached.")

if __name__ == "__main__":
    main()
    
