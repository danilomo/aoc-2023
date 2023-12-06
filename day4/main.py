import unittest
from dataclasses import dataclass
import sys

@dataclass
class Entry:
    id: int
    winning: list
    my_numbers: list

    def __str__(self):
        winning = " ".join(str(val) for val in self.winning)
        my_numbers = " ".join(str(val) for val in self.my_numbers)
        return f"Card {self.id}: {winning} | {my_numbers}"
    
    def points(self):
        winning = set(self.winning)
        mynums = set(self.my_numbers)
        points = winning.intersection(mynums)

        if not points:
            return 0
        
        total = 1
        for _ in points:
            total *= 2

        return total // 2
    
    def matches(self):
        winning = set(self.winning)
        mynums = set(self.my_numbers)
        points = winning.intersection(mynums)
        return len(points)

class TestSuite(unittest.TestCase):
    lines = """Card 1: 41 48 83 86 17 | 83 86 6 31 17 9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3: 1 21 53 59 44 | 69 82 63 72 16 21 14 1
Card 4: 41 92 73 84 69 | 59 84 76 51 58 5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""

    def test_parse_lines(self):
        lines = TestSuite.lines.split("\n")
        for line in lines:
            entry = parse_line(line)
            self.assertEqual(
                line,
                str(entry)
            )
    
    def test_score(self):
        entries = [
            parse_line(line)
            for line in TestSuite.lines.split("\n")
        ]

        values = {
            1: 8,
            2: 2,
            3: 2,
            4: 1,
            5: 0,
            6: 0
        }

        for entry in entries:
            points = entry.points()
            self.assertEqual(
                values[entry.id],
                points
            )

    def test_total_cards(self):
        entries = [
            parse_line(line)
            for line in TestSuite.lines.split("\n")
        ]

        total_cards = compute_total_cards(entries)
        self.assertEqual(30, total_cards)      

def read_lines(file_name):
    with open(file_name) as handle:
        return [
            line.strip()
            for line in handle
        ]
    
def parse_numbers(line):
    return list(
        int(val.strip())
        for val in line.split(" ")
        if val
    )
    
def parse_line(line):
    line = line.strip()
    left, right = line.split(":")
    id = int(left.replace("Card ", ""))

    left, right = right.split("|")

    return Entry(
        id,
        parse_numbers(left),
        parse_numbers(right)
    )




def compute_total_cards(entries):
    indices = list(range(0, len(entries)))
    total = 0

    while len(indices) > 0:
        index = indices.pop()

        if index >= len(entries):
            continue
        
        total += 1

        matches = entries[index].matches()

        if matches == 0:
            continue

        for i in range(index+1, index+1+matches):        
            indices.append(i)

    return total

def main():
    input = sys.argv[1]
    entries = (parse_line(line) for line in read_lines(input))
    total = 0
    for entry in entries:
        total += entry.points()
    
    print(total)

def main2():
    input = sys.argv[1]
    entries = list(parse_line(line) for line in read_lines(input))

    print(compute_total_cards(entries))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        unittest.main()
    else:
        main2()