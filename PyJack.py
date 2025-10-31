import random
import os
import time
import sys

# NOTE: using unicode suits, if your terminal font glitches, swap to "S H D C".
# not sure how to add color btw
suits = ["♠", "♥", "♦", "♣"]
values = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
    "A": 11,
}

# config (tweak these if the pacing feels off)
stepmode = False
stepDelay = 0.9

initial_coins = 100
num_decks = 6
cutratio = 0.20


def clearconsole():
    # quick screen wipe, ANSI fallback if the shell ignores cls/clear
    cmd = "cls" if os.name == "nt" else "clear"
    code = os.system(cmd)
    if code != 0:

        sys.stdout.write("\033[2J\033[H")
        sys.stdout.flush()


def pause():
    # small breather between actions, in stepmode we wait for Enter
    if stepmode:
        input("Press Enter to continue...")
    else:
        time.sleep(stepDelay)


def formathand(hand):
    # visually bracket cards like: [A♠] [10♥]
    return ' '.join(f'[{card}]' for card in hand)


def createdeck():
    # plain 52-card deck, no jokers, face cards worth 10, Ace starts at 11
    deck = [f"{value}{suit}" for value in values for suit in suits]
    return deck





def createshoe(num_decks):
    # build N decks into one shoe, single shuffle is good enough here
    deck = []
    for _ in range(num_decks):
        deck.extend(createdeck())

    random.shuffle(deck)
    # debug: print(deck[:5])
    # might seed rng  here if tests feel flaky
    return deck


def reshuffleshoe(deck, num_decks):
    # rebuilds and reshuffles the shoe when cards run low.
    deck.clear()
    deck.extend(createshoe(num_decks))
    print("New shoe... shuffled")
    # debug: print(deck[:5]) # looks random-ish? good enough


def dealcard(deck):
    # deal 1 card from the current shoe.
    if not deck:  # shouldn't happen, we reshuffle before rounds, but be safe
        raise RuntimeError("Shoe is empty unexpectedly")
    return deck.pop()


def calculatehandvalue(hand):
    total = 0
    aces = 0
    for card in hand:
        rank = card[:-1]
        total += values[rank]
        if rank == "A":
            aces += 1
    # idk if there's a cleaner loop here, this is simple and safe
    while total > 21 and aces:
        total -= 10
        aces -= 1
    return total


def issoft17(hand):
    # soft 17 = 17 where at least one Ace still counts as 11
    total = calculatehandvalue(hand)
    if total != 17:
        return False
    ranks = [c[:-1] for c in hand]
    if "A" not in ranks:
        return False


    hard_total = sum(values[r] if r != "A" else 1 for r in ranks)
    return hard_total == 7


def initialhand(deck):
    # deal two each; we keep it simple (no peek rules etc.)
    player_hand = []
    dealer_hand = []
    player_hand.append(dealcard(deck))
    dealer_hand.append(dealcard(deck))
    player_hand.append(dealcard(deck))
    dealer_hand.append(dealcard(deck))


    return player_hand, dealer_hand


def playerTurn(player_hand, deck):
    # basic loop: player hits/stands, no splits/doubles yet
    while True:
        total = calculatehandvalue(player_hand)
        if total > 21:
            print(f"Your hand: {' '.join(f'[{c}]' for c in player_hand)} (Total: {total})")
            print("Busted!")
            return player_hand, True, False
        print(f"Your hand: {formathand(player_hand)} (Total: {total})")

        # TODO: split hands and double down (basic features missing on purpose for now).
        # might revisit input UX later if we add more options

        user_input = input("Options: Hit (h) / Stand (s) ").lower().strip()
        if user_input == "hit" or user_input == "h":
            player_hand.append(dealcard(deck))
            continue
        elif user_input == "stand" or user_input == "s":
            return player_hand, False, True
        else:
            print('Invalid option. Type "Hit/h" or "Stand/s".')
            continue


def dealer_turn(dealer_hand, deck, hit_on_soft_17=False):
    print("Dealer's turn...")
    pause()
    total = calculatehandvalue(dealer_hand)
    # some tables hit soft 17, the flag flips that behavior
    while total < 17 or (total == 17 and hit_on_soft_17 and issoft17(dealer_hand)):
        dealer_hand.append(dealcard(deck))
        total = calculatehandvalue(dealer_hand)
        print("Dealer draws: [{}] (Total: {})".format(dealer_hand[-1], total), flush=True)
        pause()
    if total > 21:
        return dealer_hand, True, False
    else:
        return dealer_hand, False, True


def compareHands(player_hand, dealer_hand):
    # decide outcome, push means tie, no money moves
    # (no side bets here)

    player_total = calculatehandvalue(player_hand)
    dealer_total = calculatehandvalue(dealer_hand)
    if player_total > 21:
        print(f"Player busts with {player_total}! Dealer wins.")
        return "Dealer Wins"

    elif dealer_total > 21:
        print(f"Dealer busts with {dealer_total}! You win.")
        return "You Win"

    elif player_total == dealer_total:
        print(f"Push! Both have {player_total}.")
        return "Push"

    elif player_total > dealer_total:
        print(f"You win! {player_total} vs {dealer_total}.")
        return "You Win"

    else:
        print(f"Dealer wins! {dealer_total} vs {player_total}.")
        return "Dealer Wins"


def play_round(deck, hit_on_soft_17=False):
    # one full hand; lots of early returns to keep it readable
    player_hand, dealer_hand = initialhand(deck)
    print(f"Dealer shows: [{dealer_hand[0]}][?]")
    p0 = calculatehandvalue(player_hand)
    d0 = calculatehandvalue(dealer_hand)

    if p0 == 21 and d0 == 21:
        pause()
        print(f"Push! Both have Blackjack: You {formathand(player_hand)} vs Dealer {dealer_hand}")

        return "Push", False
    elif p0 == 21:
        print("Blackjack! You win.")

        return "You Win", True
    elif d0 == 21:
        print(f"Dealer has Blackjack: {formathand(dealer_hand)} (21). Dealer wins.")

        return "Dealer Wins", False
    player_hand, p_busted, _ = playerTurn(player_hand, deck)
    if p_busted:
        print("You busted! Dealer Wins.")

        return "Dealer Wins", False
    dealer_hand, d_busted, _ = dealer_turn(dealer_hand, deck, hit_on_soft_17=hit_on_soft_17)
    if d_busted:
        print("Dealer busted! You Win.")

        return "You Win", False

    pause()

    print(f"Dealer's hand: {formathand(dealer_hand)} (Total: {calculatehandvalue(dealer_hand)})", flush=True)

    pause()

    print(f"Your hand: {formathand(player_hand)} ({calculatehandvalue(player_hand)})", flush=True)

    pause()

    result = compareHands(player_hand, dealer_hand)
    # print("Final compare -> " + result) # quick trace
    return result, False


def bet(coins):
    while True:
        raw = input(f"Place your bet (balance {coins}, 0/q to quit): ").strip().lower()
        if raw in ("0", "q", "quit", "exit"):
            return None
        try:
            amt = int(raw)
        except ValueError:
            print("Please enter a numeric bet amount.")
            continue
        if not (1 <= amt <= coins):
            print(f"Bet must be between 1 and {coins}.")
            continue
        return amt


def resolvepayment(result, bet, natbj=False):
    bet = int(bet)
    if result == "You Win":
        payment = bet
        if natbj:
            payment = int(round(bet * 1.5))
        return payment
    elif result == "Dealer Wins":
        return -bet
    elif result == "Push":
        return 0
    else:
        return 0


def gameloop_nobet(deck, initial_size, cutratio, num_decks):
    w = 0
    l = 0
    p = 0
    rnd = 1
    while True:
        if len(deck) <= int(initial_size * cutratio):
            reshuffleshoe(deck, num_decks)
            initial_size = len(deck)
        clearconsole()
        print(f"🔹 Round: {rnd} 🔹") # keeping it simple for now
        print(f"Score: W {w} / L {l} / P {p}\n")
        result, _ = play_round(deck, hit_on_soft_17=False)
        if result == "You Win":
            w += 1
        elif result == "Dealer Wins":
            l += 1
        else:
            p += 1
        pause()
        print("Round Summary: Result = %s" % result.title())
        print(f"Score: W {w} / L {l} / P {p}")
        again = input("Play again? y/n ").lower().strip()
        if again not in ("y", "yes"):
            break
        else:
            clearconsole()
        rnd += 1
    print(f"Final score: W {w} / L {l} / P {p}")


def gameloop_bets(deck, coins, initial_size, cutratio, num_decks):
    # money mode, not a casino simulator, just enough to test strategy
    w = 0
    l = 0
    p = 0
    rnd = 1
    while coins > 0:
        print(f"Your coins: {coins}")
        player_bet = bet(coins)
        if player_bet is None:
            break
        clearconsole()
        print(f"🔹 Round: {rnd} 🔹")
        print(f"Current Coins: {coins} | Bet: {player_bet}")
        print(f"Score: W {w} / L {l} / P {p}\n")
        if len(deck) <= int(initial_size * cutratio):
            reshuffleshoe(deck, num_decks)
            initial_size = len(deck)
        result, natbj = play_round(deck, hit_on_soft_17=True)
        delta = resolvepayment(result, player_bet, natbj)
        coins += delta
        if result == "You Win":
            w += 1
        elif result == "Dealer Wins":
            l += 1
        else:
            p += 1
        pause()
        print(f"Round Summary: Result = {result.title()} | Δ: {delta:+} | Coins: {coins}")
        print(f"Score: W {w} / L {l} / P {p}")
        again = input("Play again? y/n ").lower().strip()
        if again not in ("y", "yes"):
            break
        else:
            clearconsole()
        rnd += 1
    # TODO: add insurance, splits, and doubling options later.
    print(f"Final Score: W {w} / L {l} / P {p} | Final coins: {coins}")


if __name__ == "__main__":
    # entry point
    # TODO: CLI flags/env for config, maybe --seed for reproducible runs? idk
    mode = input("Mode: Bets(b) or No-bets(n)? ").lower().strip()
    with_bets = mode in ("b", "bets")
    deck = createshoe(num_decks)
    initial_size = len(deck)
    if with_bets:
        gameloop_bets(deck, initial_coins, initial_size, cutratio, num_decks)
    else:
        gameloop_nobet(deck, initial_size, cutratio, num_decks)
