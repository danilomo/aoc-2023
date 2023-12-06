import unittest
from dataclasses import dataclass, field
import sys

digits = set("1234567890")

sample_input = """467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598.."""

@dataclass
class Range:
    line: int
    range: tuple
    lines: list = field(hash=False, compare=False)

    def coords(self):
        return (self.line, self.range)

    def in_range(self, i, j):
        lower, upper = self.range
        return i == self.line and (lower <= j <= upper)

    def number(self):
        l, u = self.range
        return int("".join(self.lines[self.line][l:u+1]))
    
    def is_part_number(self):
        line = self.line
        lower, upper = self.range
        for row in [-1 + line, line, 1 + line]:
            for col in range(lower-1, upper + 2):
                if self.lines[row][col] in digits:
                    continue

                if self.lines[row][col] != '.':
                    return True
                
        return False

@dataclass
class Schematic:
    lines: list

    def part_numbers(self):
        for i in range(0, len(self.lines)):
            line = self.lines[i]
            for r in extract_numbers(line):
                range_obj = Range(i, r, self.lines)
                if range_obj.is_part_number():
                    yield range_obj

    def gears(self):
        part_numbers = list(self.part_numbers())
        
        for i in range(0, len(self.lines)):
            for j in range(0, len(self.lines[0])):
                if self.lines[i][j] != "*":
                    continue

                p_numbers = self.check_gears(i, j, part_numbers)
                if len(p_numbers) == 2:
                    yield ((i, j), p_numbers)

    def check_gears(self, row, col, part_numbers):
        result = set()

        for i in [row-1, row, row+1]:
            for j in [col-1, col, col+1]:
                for part in part_numbers:
                    if part.in_range(i, j):
                        result.add(part.number())

        return result


def extract_numbers(line):
    lower = -1
    result = []

    for i in range(0, len(line)):
        if line[i] not in digits and lower < 0:
            continue

        if line[i] not in digits:
            result.append((lower, i-1))
            lower = -1
            continue

        if lower < 0:
            lower = i
            continue

    return result


def parse_schematic(lines):
    lines = list(lines)    
    cols = len(lines[0])
    blanks = ['.', *['.' for _ in range(0, cols)] , '.']
    lines = [
        blanks,
        * [['.', *line, '.'] for line in lines],
        blanks
    ]

    return Schematic(lines)

class TestSuite(unittest.TestCase):

    def test_find_gears(self):
        expected = 467835

        schematic = parse_schematic(sample_input.splitlines())
        gears = [numbers for _, numbers in schematic.gears()]

        result = 0

        for first, second in gears:
            result += first * second

        self.assertEqual(expected, result)


    def test_extract_numbers(self):
        expected = [
            (0, 2), 
            (5, 7)
        ]

        extracted = extract_numbers(sample_input.splitlines()[0])
        self.assertEqual(expected, extracted)


    def test_sum_part_numbers(self):
        schematic = parse_schematic(sample_input.splitlines())
        part_numbers = schematic.part_numbers()

        self.assertEqual(
            4361,
            sum(p.number() for p in part_numbers)
        )

def main():
    with open("input.txt") as handle:
        lines = [line.strip() for line in handle]
        schematic = parse_schematic(lines)
        part_numbers = schematic.part_numbers()
        print(sum(p.number() for p in part_numbers))

def main2():
    with open("input.txt") as handle:
        lines = [line.strip() for line in handle]
        schematic = parse_schematic(lines)
        gears = [numbers for _, numbers in schematic.gears()]

        result = 0

        for first, second in gears:
            result += first * second

        print(result)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        unittest.main()
    else:
        main2()