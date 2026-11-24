import json
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import streamlit as st
from signal_logic import evaluate_signal

st.set_page_config(page_title="Real Forex Signal MVP", layout="centered")

HISTORY_FILE = Path("history.json")


def load_history() -> list:
    if not HISTORY_FILE.exists():
        return []
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []


def save_history(records: list) -> None:
    HISTORY_FILE.write_text(
        json.dumps(records, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


now_utc = datetime.now(timezone.utc)
now_bd = now_utc.astimezone(ZoneInfo("Asia/Dhaka"))

st.title("Real Forex Signal MVP")
st.caption(
    f"UTC: {now_utc.strftime('%H:%M:%S')} | "
    f"Dhaka: {now_bd.strftime('%I:%M:%S %p')}"
)

pair = st.text_input("Currency Pair", value="EUR/USD")
trend = st.selectbox("Market Trend", ["UP", "DOWN", "SIDEWAYS"])
rsi = st.slider("RSI (14)", min_value=5.0, max_value=95.0, value=40.0, step=0.5)
is_choppy = st.checkbox("মার্কেট এলোমেলো / সাইডওয়েজ / নিউজ ঝুঁকি আছে?", value=False)

if st.button("Analyze Setup"):
    result = evaluate_signal(trend=trend, rsi=rsi, is_choppy=is_choppy)

    st.subheader(f"Result: {result['signal']}")
    st.write(f"**Confidence:** {result['confidence']}")
    for r in result["reasons"]:
        st.write(f"- {r}")

    history = load_history()
    history.insert(
        0,
        {
            "time_utc": now_utc.strftime("%Y-%m-%d %H:%M:%S"),
            "time_bd": now_bd.strftime("%Y-%m-%d %I:%M:%S %p"),
            "pair": pair.strip().upper(),
            "trend": trend,
            "rsi": rsi,
            "is_choppy": is_choppy,
            "signal": result["signal"],
            "confidence": result["confidence"],
        },
    )
    save_history(history[:50])

st.divider()
st.subheader("সাম্প্রতিক লগ (Recent History)")
history_data = load_history()
if history_data:
    for item in history_data[:10]:
        st.write(
            f"**{item['pair']}** | `{item['signal']}` | "
            f"Trend: {item['trend']} | RSI: {item['rsi']} | "
            f"{item['time_bd']}"
        )
else:
    st.info("এখনো কোনো বিশ্লেষণ সংরক্ষণ করা হয়নি।")
