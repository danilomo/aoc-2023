import unittest
from dataclasses import dataclass
import sys
import functools

sample_input="""32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

FIVE_A_KIND = 7
FOUR_A_KIND = 6
FULL_HOUSE = 5
THREE_A_KIND = 4
TWO_PAIR = 3
ONE_PAIR = 2
HIGH_CARD = 1
JOKER = 0

card_values = {
    "T": 10,
    "Q": 11,
    "K": 12,
    "A": 13,
    "J": 0
}

def create_hand(hand, bid=0):
    return Hand([
        int(card_values.get(card, card))
        for card in hand
    ], bid)

@dataclass
class Hand:
    cards: list
    bid: int = 0

    def hand_type(self):
        counts = {}
        for card in self.cards:
            if card not in counts:
                counts[card] = 1
                continue
            counts[card] += 1

        joker_count = counts.get(JOKER, 0)

        if joker_count == 5:
            return FIVE_A_KIND
        
        if JOKER in counts:
            del counts[JOKER]
        
        max_repeat = max(counts.items(), key=lambda i: i[1])[0]
        counts[max_repeat] += joker_count

        values = list(counts.values())
        values.sort()

        if values == [5]:
            return FIVE_A_KIND
        elif values == [1, 4]:
            return FOUR_A_KIND
        elif values == [2, 3]:
            return FULL_HOUSE
        elif values == [1, 1, 3]:
            return THREE_A_KIND
        elif values == [1, 2, 2]:
            return TWO_PAIR
        elif values == [1, 1, 1, 2]:
            return ONE_PAIR
        else:
            return HIGH_CARD
        
def parse_line(line):
    left, right = line.split(" ")
    return create_hand(
        left,
        int(right)
    )


def total_bid_sum(hands):
    indices = range(1, len(hands)+1)

    return sum(
        hand.bid * rank
        for hand, rank in zip(hands, indices)
    )

def read_lines(file_name):
    with open(file_name) as handle:
        return [
            line.strip()
            for line in handle
        ]

def main():
    lines = read_lines(sys.argv[1])
    hands = [parse_line(line) for line in lines]
    hands.sort(key=lambda h: (h.hand_type(), h.cards))

    total = total_bid_sum(hands)  
    print(total)  

class TestSuite(unittest.TestCase):

    def test_joker(self):
        rows = [
            ("J1234", ONE_PAIR),
            ("32T3K", ONE_PAIR),
            ("KK677", TWO_PAIR),
            ("T55J5", FOUR_A_KIND),
            ("KTJJT", FOUR_A_KIND),
            ("QQQJA", FOUR_A_KIND),
            ("JJJJJ", FIVE_A_KIND),
            ("96J66", FOUR_A_KIND),
            ("J6569", THREE_A_KIND),
            ("JKK92", THREE_A_KIND)            
        ]

        for row in rows:
            h = create_hand(row[0])
            t = row[1]
            self.assertEqual(h.hand_type(), t, f"Wrong type for {h}")

    def test_sort_ranks(self):
        hands = [parse_line(line.strip()) for line in sample_input.split("\n")]
        hands.sort(key=lambda h: (h.hand_type(), h.cards))

        total = total_bid_sum(hands)
        self.assertEqual(total, 5905)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        unittest.main()
    else:
        main()