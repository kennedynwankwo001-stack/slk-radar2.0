# main.py
import json
import os
import requests
from datetime import datetime
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

STATE_FILE = "state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=4)

def send_telegram_alert(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("Telegram alert sent successfully!")
        else:
            print(f"Failed to send Telegram alert: {response.text}")
    except Exception as e:
        print(f"Error sending alert: {e}")

def run_radar_scan():
    print(f"[{datetime.now()}] SLK Radar scan started...")
    
    # Load bot's memory
    state = load_state()
    
    # Test pair list
    pairs = ["EUR/AUD", "EUR/USD", "GBP/JPY"]
    
    for pair in pairs:
        print(f"Checking {pair}...")
        
        # Example test trigger for EUR/AUD
        if pair == "EUR/AUD" and "EUR/AUD" not in state:
            alert_message = (
                "🚨 *SLK SETUP CONFIRMED*\n\n"
                "• *Pair:* EUR/AUD\n"
                "• *Bias:* Bullish\n"
                "• *Level:* 1.62345 (Bullish OCL)\n"
                "• *Score:* 5/5 (Strong DRD + Sweep)\n"
                "• *H4 Breakout:* Confirmed\n\n"
                "*(Waiting for H4 retest confirmation)*"
            )
            send_telegram_alert(alert_message)
            
            # Save to state memory
            state[pair] = {"status": "CONFIRMED", "bias": "BULLISH"}
            save_state(state)

    print("Scan complete. Memory saved.")

if __name__ == "__main__":
    run_radar_scan()
  
