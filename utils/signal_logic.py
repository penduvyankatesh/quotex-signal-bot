import numpy as np

def generate_signal(df):
    latest = df.iloc[-1]
    prev = df.iloc[-2]

    confidence = 0
    signal = None

    # RSI
    if latest['RSI'] < 30:
        confidence += 20
        signal = "BUY"
    elif latest['RSI'] > 70:
        confidence += 20
        signal = "SELL"

    # EMA Crossover
    if latest['EMA20'] > latest['EMA50']:
        confidence += 20
        if signal == "BUY": confidence += 10
    else:
        confidence += 20
        if signal == "SELL": confidence += 10

    # Bollinger
    if latest['close'] < latest['BB_LOWER']:
        signal = "BUY"
        confidence += 15
    elif latest['close'] > latest['BB_UPPER']:
        signal = "SELL"
        confidence += 15

    # Candle pattern (simple)
    if latest['close'] > prev['close'] and latest['close'] > latest['EMA20']:
        if signal == "BUY": confidence += 10
    elif latest['close'] < prev['close'] and latest['close'] < latest['EMA20']:
        if signal == "SELL": confidence += 10

    # Volume spike
    if latest['volume'] > df['volume'].rolling(20).mean().iloc[-1] * 1.5:
        confidence += 10

    return signal, min(confidence, 100)
