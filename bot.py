import os
import time
import pandas as pd
import numpy as np
import requests
import telebot
from utils.indicators import compute_indicators
from utils.signal_logic import generate_signal

# === TELEGRAM BOT CONFIG ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telebot.TeleBot(BOT_TOKEN)

# === SETTINGS ===
SYMBOL = "BTCUSD"
TIMEFRAME = "5s"   # 5 second candles
DATA_POINTS = 60   # last 60 candles

# === FETCHING CANDLE DATA ===
def get_candle_data():
    url = f"https://api.binance.com/api/v3/klines?symbol={SYMBOL}&interval=1s&limit={DATA_POINTS}"
    data = requests.get(url).json()
    df = pd.DataFrame(data, columns=[
        'time', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'qav', 'trades', 'tbbav', 'tbqav', 'ignore'
    ])
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    return df[['close', 'volume']]

# === MAIN LOOP ===
def main():
    last_signal = None

    while True:
        try:
            df = get_candle_data()
            df = compute_indicators(df)
            signal, confidence = generate_signal(df)

            if signal and confidence >= 75:
                msg = f"🔥 *{signal.upper()} SIGNAL* ({confidence}% confidence)\nPair: {SYMBOL}"
                if last_signal != signal:
                    bot.send_message(CHAT_ID, msg, parse_mode="Markdown")
                    last_signal = signal
            else:
                bot.send_message(CHAT_ID, "⏳ No strong signal yet, waiting...", parse_mode="Markdown")

            time.sleep(5)

        except Exception as e:
            print("Error:", e)
            time.sleep(5)

if __name__ == "__main__":
    main()
