{playing around with AI}
# Groceries Price Comparison (AI Receipt Checker)

This is a side project I built mostly for fun — and to show/learn how AI + web scraping + a bit of logic can be used to so lve
something simple but useful: **comparing the prices on your grocery receipt with other stores**.

Right now it works with **Oda.no**, but I'm planning to add support for **Meny.no** as-well since these are the only
grocery stores that have prices available online..

---
## What it does

- You take a photo of your **grocery receipt**
- The system uses **OpenAI GPT-4o** to:
    - Extract product names, prices, and quantities
    - Normalize product names (e.g. removes brand names like XTRA or COOP)
- Then it:
    - Searches the same product on **Oda** using Selenium
    - Gets the actual price from Oda
- Finally:
    - It compares both prices using Python logic
    - Tells you where you **overpaid** or **saved**
    - Gives a **final total** of how much you could’ve saved or overpaid
  

The AI doesn’t just extract text — it also decides **which product to compare**.

For example, if your receipt says "Kyllingfilet 1000g" and Oda returns similar items, the AI picks the one that’s the **closest match** based on name and weight.

---

## Tech Stack

- **OpenAI GPT-4o** — for intelligent OCR + product matching
- **Selenium** — scrapes Oda search results
- **Python** — to glue everything together and do real math (because AI is sometimes too “creative”)
---

## Responsible Scraping Notice

This project respects the `robots.txt` policies of the websites it interacts with and is not intended to run at scale or cause any harm to external services. It's designed as a personal experiment for educational purposes only.


