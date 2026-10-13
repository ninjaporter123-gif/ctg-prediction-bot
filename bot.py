import time
import requests
import urllib.parse
import json

import sys
# Default 10 wins, workflow dispatch inputs irundha adhai eduthukum
TARGET_WINS = int(sys.argv[1]) if len(sys.argv) > 1 else 10
BOT_TOKEN = "8662159068:AAE-FHz_SeJWVLXonnWX7piNRzYl3DLLArw"
CHAT_ID = "-1004446531098"
TARGET_WINS = 10

# Codetabs Fast Proxy Gateway
RAW_API = "https://draw.ar-lottery01.com/WinGo/WinGo_1M/GetHistoryIssuePage.json?pageNo=1&pageSize=10"
ENCODED_URL = urllib.parse.quote(RAW_API)
PROXY_URL = f"https://api.codetabs.com/v1/proxy?quest={ENCODED_URL}"

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
        else:
            print(f"TG Send Error: {data}")
    except Exception as e:
        print(f"TG Connection Error: {e}")
    return None

def tg_edit(msg_id, text):
    try:
        requests.post(
            f"https://api.telegram.org/bot{BOT_TOKEN}/editMessageText",
            json={"chat_id": CHAT_ID, "message_id": msg_id, "text": text, "parse_mode": "HTML"},
            timeout=10
        )
    except Exception as e:
        print(f"TG Edit Error: {e}")

def fetch_history():
    try:
        r = requests.get(PROXY_URL, timeout=12)
        if r.status_code == 200:
            data = r.json()
            if isinstance(data, str):
                data = json.loads(data)
            items = data.get("data", {}).get("list") or data.get("list") or []
            return items
        else:
            print(f"Proxy Status Code: {r.status_code}")
    except Exception as e:
        print(f"Fetch Error: {e}")
    return []

def calculate_2738(history):
    latest_num = int(history[0]["number"])
    count = 5 if (latest_num % 2 != 0) else 6
    num_str = "".join([str(history[i]["number"]) for i in range(count)])
    
    divisor = int(num_str) if int(num_str) > 0 else 1
    scaled = (2738 * (10**24)) // divisor
    dec_str = str(scaled).zfill(24)[:20]
    
    big_digits = [int(c) for c in dec_str if int(c) >= 5]
    small_digits = [int(c) for c in dec_str if int(c) < 5]
    
    if len(big_digits) >= len(small_digits):
        pred_size = "BIG"
        freq = {}
        for d in big_digits:
            freq[d] = freq.get(d, 0) + 1
        sorted_d = sorted([5, 6, 7, 8, 9], key=lambda x: freq.get(x, 0), reverse=True)
        hot = sorted_d[:2]
        chosen = hot[0]
    else:
        pred_size = "SMALL"
        freq = {}
        for d in small_digits:
            freq[d] = freq.get(d, 0) + 1
        sorted_d = sorted([0, 1, 2, 3, 4], key=lambda x: freq.get(x, 0), reverse=True)
        hot = sorted_d[:2]
        chosen = hot[0]
        
    return pred_size, hot, chosen, dec_str

def main():
    print("Session starting on GitHub Cloud...")
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
        
        # Dispatch window :25 - :35
        if 25 <= now_sec <= 35:
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
                    print(f"Dispatched Issue #{target_issue} | Prediction: {pred_size}")
                    
                    time.sleep(35)
                    
                    resolved = False
                    for _ in range(15):
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
                                    result_banner = f"💥 <b>JACKPOT WIN!</b> 💥 Result: {act_num} ({act_size})" if is_jackpot else f"✅ <b>WIN!</b> Result: {act_num} ({act_size})"
                                else:
                                    level += 1
                                    if level > max_level:
                                        max_level = level
                                    result_banner = f"❌ <b>LOSS!</b> Result: {act_num} ({act_size})"
                                
                                updated_card = (
                                    "┏━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
                                    "   👑 <b>CTG GAMING PREDICTION</b> 👑\n"
                                    "┗━━━━━━━━━━━━━━━━━━━━━━━━┛\n\n"
                                    "  🎮 <b>SERVER :</b> WINGO 1 MIN [VIP]\n"
                                    f"  🎯 <b>TARGET ISSUE :</b> #{target_issue}\n\n"
                                    f"  🔮 <b>PREDICTION :</b> {pool_text}\n"
                                    f"  🎲 <b>HOT NUMBERS :</b> {hot[0]} & {hot[1]}\n\n"
                                    f"  📊 <b>CHOSEN DIGIT :</b> {chosen}\n\n"
                                    f"  {result_banner}\n"
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
                                print(f"Issue #{target_issue} Finished: {result_banner.split()[1]}")
                                break
                    if not resolved:
                        print(f"Issue #{target_issue} verification timed out.")
        time.sleep(1)

    final_card = (
        "🎉 <b>SESSION TARGET COMPLETED!</b> 🎉\n"
        "━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🏆 <b>Total Wins:</b> {wins}/{TARGET_WINS}\n"
        f"🔥 <b>Max Level Reached:</b> {max_level}\n"
        "👑 <i>Congratulations to all VIP members!</i>"
    )
    tg_send(final_card)
    print("Session target achieved.")

if __name__ == "__main__":
    main()
    
