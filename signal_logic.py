def evaluate_signal(trend: str, rsi: float, is_choppy: bool = False) -> dict:
    reasons = []

    if is_choppy or trend == "SIDEWAYS":
        reasons.append("মার্কেট সাইডওয়েজ বা অস্পষ্ট অবস্থায় আছে")
        return {
            "signal": "NO SIGNAL",
            "confidence": "Low",
            "reasons": reasons,
        }

    if trend == "UP":
        if rsi < 30:
            reasons.append("আপট্রেন্ড সক্রিয়, তবে RSI ৩০-এর নিচে (ওভারসোল্ড/রিভার্সাল ঝুঁকি)")
            return {
                "signal": "NO SIGNAL",
                "confidence": "Medium",
                "reasons": reasons,
            }
        if 30 <= rsi <= 48:
            reasons.append("আপট্রেন্ডে সুস্থ পুলব্যাক দেখা যাচ্ছে")
            reasons.append(f"RSI ({rsi}) বাই জোনের অনুকূলে আছে")
            return {
                "signal": "BUY",
                "confidence": "Medium-High",
                "reasons": reasons,
            }
        if rsi > 75:
            reasons.append(f"RSI ({rsi}) অনেক বেশি (ওভারবট), চেজ করা ঝুঁকিপূর্ণ")
            return {
                "signal": "NO SIGNAL",
                "confidence": "Medium",
                "reasons": reasons,
            }

    if trend == "DOWN":
        if rsi > 70:
            reasons.append("ডাউনট্রেন্ড সক্রিয়, তবে RSI ৭০-এর ওপরে (ওভারবট/রিভার্সাল ঝুঁকি)")
            return {
                "signal": "NO SIGNAL",
                "confidence": "Medium",
                "reasons": reasons,
            }
        if 52 <= rsi <= 70:
            reasons.append("ডাউনট্রেন্ডে পুলব্যাক বা রেজিস্ট্যান্সের কাছাকাছি চাপ")
            reasons.append(f"RSI ({rsi}) সেল জোনের অনুকূলে আছে")
            return {
                "signal": "SELL",
                "confidence": "Medium-High",
                "reasons": reasons,
            }
        if rsi < 25:
            reasons.append(f"RSI ({rsi}) অনেক নিচে (ওভারসোল্ড), চেজ করা ঝুঁকিপূর্ণ")
            return {
                "signal": "NO SIGNAL",
                "confidence": "Medium",
                "reasons": reasons,
            }

    reasons.append("পর্যাপ্ত স্পষ্ট কনফার্মেশন পাওয়া যায়নি")
    return {
        "signal": "NO SIGNAL",
        "confidence": "Low",
        "reasons": reasons,
          }
