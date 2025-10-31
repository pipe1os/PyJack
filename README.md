# 🃏 Pyjack

A simple blackjack game written in python that you can play in your terminal.  


---

## TL;DR

```bash
python PyJack.py
```
> When prompted, choose **Bets (b)** or **No‑bets (n)** mode.

If your file has a different name, run it as:
```bash
python <your_script_name>.py
```

---

## What You Get

- **Two modes**
  - **No‑bets:** just play hands and track **W/L/P**.
  - **Bets:** start with coins, place bets each round, and get paid (or lose!) accordingly.
- **Multiple‑deck shoe** with cut card: auto‑reshuffle when the shoe hits the cut (%).
- **Soft‑17 logic**: dealer **hits on soft 17 in Bets mode**, **stands in No‑bets** (configurable flag).
- **Natural Blackjack payout:** **3:2** (1.5×) in Bets mode.
- **Unicode suits** (`♠ ♥ ♦ ♣`) for a clean look.
- **No dependencies** — runs on Python 3.x with the standard library.

---

## Requirements

- Python **3.8+** recommended (uses only stdlib: `random`, `os`, `time`, `sys`).

---

## How to Play

1. **Start the script** and pick a mode:
   - **Bets (b):** you’ll be asked your bet every hand (or `0/q` to quit).
   - **No‑bets (n):** quick rounds with a simple scoreboard.
2. **Your turn:** type **`h`** / **`hit`** to draw, **`s`** / **`stand`** to hold.
3. **Dealer plays** following the configured soft‑17 rule.
4. **Result shows** with totals and your score/coins.

Example round prompt:
```
Place your bet (balance 100, 0/q to quit):
Options: Hit (h) / Stand (s)
Play again? y/n
```

---

## Rules Implemented

- Aces count as **11** unless you’d bust — then they drop to **1** (auto‑adjusted).
- Dealer draws until **17+**; optionally **hits soft 17** (config flag).
- **Blackjack** detection on initial deal for both sides.
- Outcomes: **Win / Lose / Push**.  
- **No splits / double‑down / insurance** (by design for now)

---

## Config You Can Tweak (top of the file)

```python
stepmode = False     # True = wait for Enter between steps (good for demos)
stepDelay = 0.9      # Delay between dealer actions when stepmode=False

initial_coins = 100  # Starting bankroll (Bets mode)
num_decks = 6        # Shoe size
cutratio = 0.20      # Reshuffle when shoe <= 20% of original
```
Dealer behavior per mode:
- **No‑bets:** `hit_on_soft_17=False`
- **Bets:** `hit_on_soft_17=True`

---

## What the code does

- **Deck & shoe:** builds `num_decks` × 52 cards, shuffles once; **auto‑reshuffles** when remaining cards ≤ `initial_size * cutratio`.
- **Hand value:** tallies ranks with Aces as 11, then downgrades Aces to 1 as needed to avoid busts.
- **Soft‑17 check:** “soft” = total 17 with at least one Ace still counted as 11.
- **Payments:**  
  - Win = `+bet`,  
  - **Natural blackjack** = `+round(bet * 1.5)`,  
  - Lose = `-bet`,  
  - Push = `0`.


## License

Do whatever you want for personal/learning use.
