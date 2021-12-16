import random
import pandas as pd
import numpy as np
import random
from copy import copy
from pprint import pprint

words = set()
NONLAND = {"nonland"}
MOUNTAIN = {"land", "mountain"}
PLAIN = {"land", "plain"}
CREATURE = {"nonland", "creature"}
TWODROP = CREATURE | {"two_drop"}
ALLLAND = MOUNTAIN | PLAIN
AURA = NONLAND | {"aura"} | {"attachment"}
EQUIPMENT = NONLAND | {"equipment"} | {"attachment"}


def to_df(cards):
    global words
    df = pd.DataFrame(columns=words)
    for card in cards:
        list = []
        for ind, word in enumerate(words):
            list.append(word in card)
        df = df.append(pd.Series(list, index=df.columns), ignore_index=True)
    return df


def count(hand, type):
    ans = 0
    for card in hand:
        ans += type in card
    return ans


def eval(hand):
    if count(hand, "land") <= 1:
        return "mana screw"
    if count(hand, "nonland") <= 2:
        return "mana flood"
    if count(hand, "plain") == 0:
        return "color accident"
    if count(hand, "mountain") == 0:
        return "color accident"
    if count(hand, "land") == 2 and count(hand, "two_drop") == 0:
        return "2_land_non_2_drop"
    if count(hand, "land") == 2:
        return "2_land"
    if count(hand, "two_drop") == 0:
        return "non_2_drop"
    return "good"


def simulate(deck):
    TIMES = 100000
    score = {"good": 0}
    for i in range(TIMES):
        hand = random.sample(deck, 7)

        ev = eval(hand)
        score[ev] = score.get(ev, 0) + 1
    ans = sorted(score.items(), reverse=True, key=lambda x: x[1])
    pprint(ans)


def to_deck(deck):
    ans = []
    for card in deck:
        for times in range(card[1]):
            ans.append(card[0])
    global words
    for card in deck:
        words |= card[0]

    return ans


def explore(deck):
    for i in range(len(deck)):
        for j in range(len(deck)):
            if i == j:
                continue
            newdeck = deck.copy()
            newdeck[i][1] += 1
            newdeck[j][1] -= 1
            print(f"+1:{deck[i][0]} -1:{deck[j][0]}")
            simulate(to_deck(newdeck))


deck = [[MOUNTAIN, 8], [PLAIN, 8], [TWODROP, 6], [{"nonland"}, 18]]
simulate(to_deck(deck))
explore(deck)
