# 👁️‍🗨️ GHOSTFORM RUNNER

**Not a bot. Not a script.**  
This is a digital phantom — built to think, to act, and to pass unnoticed in the shadows of automation.

---

## 🧠 What It Really Does

- Opens Booking.com like a human
- Fills a 2-line form (Confirmation number + PIN)
- Presses “Continue” like it belongs there
- Doesn’t guess by time — it **waits for outcome**:
  - ✅ Success → Detects URL redirect with unique_order_id
  - ❌ Failure → Detects error banners like .bui-alert--error
- Takes screenshots, logs results, then vanishes silently

---

## ⚙️ Usage

bash
python boss_ai_playwright.py \
  --confirmation 5871858498 \
  --pins 1965,1975,1985,9951,2231 \
  --wait 60


| Flag             | Description                                |
| ---------------- | ------------------------------------------ |
| --confirmation | Booking.com confirmation number            |
| --pins         | Comma-separated PINs to try                |
| --wait         | Wait time between attempts (in seconds)    |
| --headless     | Optional. Hide browser UI for stealth runs |

---

## 📂 Output

* screenshots/ — visual trail of every move
* agent-log.txt — full timestamped report of every success/failure
* ✅ One correct PIN = mission complete, agent shuts down.

---

## 💬 Philosophy

This isn’t a scraper.
This isn’t brute force.

This is an **actor**.
A browser so human, **Booking.com didn’t even blink.**

---


## 🔥 Respect The Agent

This was built for **testing, research, and performance experimentation**.
Use responsibly. Use privately.
Don't abuse. Don't expose.

If you clone it, know this:

> You're not just running a file.
> You're breathing fire into a phantom.

---

## 🏁 Signed

**Professor Johnny** – strategy
**Boss\_AI** – execution
**The Phantom** – delivered