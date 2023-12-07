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

card_values = {
    "T": 10,
    "J": 11,
    "Q": 12,
    "K": 13,
    "A": 14
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
    
    def test_compare(self):
        hands1 = [
            "33332",
            "77888"
        ]
        hands2 = [
            "2AAAA",
            "77788"
        ]

        for i in range(0, len(hands1)):
            h1 = create_hand(hands1[i])
            h2 = create_hand(hands2[i])
            self.assertTrue(h1.cards > h2.cards)

    def test_hand(self):
        hand_types = list(range(1, 8))
        hands = [
            create_hand(hand)
            for hand in [
                "23456",
                "A23A4",
                "23432",
                "TTT98",
                "23332",
                "AA8AA",
                "AAAAA"
            ]
        ]

        for i in range(0, len(hands)):
            self.assertEqual(hand_types[i], hands[i].hand_type(), f"Wrong card type for card f{hands[i].cards}")

    def test_parse_input(self):
        lines = [line.strip() for line in sample_input.split("\n")]
        cards = [
            create_hand("32T3K", 765),
            create_hand("T55J5", 684),
            create_hand("KK677", 28),
            create_hand("KTJJT", 220),
            create_hand("QQQJA", 483),
        ]
        for i in range(0, len(cards)):
            self.assertEqual(cards[i], parse_line(lines[i]))

    def test_sort_ranks(self):
        hands = [parse_line(line.strip()) for line in sample_input.split("\n")]
        hands.sort(key=lambda h: (h.hand_type(), h.cards))

        total = total_bid_sum(hands)
        self.assertEqual(total, 6440)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        unittest.main()
    else:
        main()