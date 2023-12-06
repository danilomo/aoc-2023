import unittest
from dataclasses import dataclass
import sys
import functools

class TestSuite(unittest.TestCase):

    lines = """Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green"""

    quantities = {
        "red": 12,
        "green": 13,
        "blue": 14
    }

    def test_parse_line(self):
        input = "Game 1: 20 green, 3 red, 2 blue; 9 red, 16 blue, 18 green; 6 blue, 19 red, 10 green; 12 red, 19 green, 11 blue"
        entry = parse_line(input)
        expected = Game(
            id = 1,
            sets=[
                [(20, "green"), (3, "red"), (2, "blue")],
                [(9, "red"), (16, "blue"), (18, "green")],
                [(6, "blue"), (19, "red"), (10, "green")],
                [(12, "red"), (19, "green"), (11, "blue")]
            ]
        )
        self.assertEqual(
            entry,
            expected
        )

    def test_parse_lines_wo_breaking(self):
        file_name = "input.txt"
        lines = read_lines(file_name)
        for l in lines:
            g = parse_line(l)
            tostr = str(g)
            self.assertEqual(l, tostr)

    def test_game_possible(self):
        possible = {1, 2, 5}

        for line in TestSuite.lines.split("\n"):
            game = parse_line(line)

            if game.id in possible:
                self.assertTrue(game.is_possible(TestSuite.quantities))
            else:
                self.assertFalse(game.is_possible(TestSuite.quantities))

    def test_compute_power(self):
        powers = {
            1: 48,
            2: 12,
            3: 1560,
            4: 630,
            5: 36
        }

        for line in TestSuite.lines.split("\n"):
            game = parse_line(line)
            result = game.fewest_cubes(TestSuite.quantities)
            self.assertEqual(powers[game.id], power(result))

    def test_compute_power2(self):
        file_name = "input.txt"
        lines = read_lines(file_name)

        for line in lines:
            game = parse_line(line)
            p = power(game.fewest_cubes(TestSuite.quantities))
            self.assertTrue(p > 0)

def read_lines(file_name):
    with open(file_name) as handle:
        return [
            line.strip()
            for line in handle
        ]

def parse_set(input):
    cubes = input.split(",")
    result = []
    for c in cubes:
        val, color = c.strip().split(" ")
        result.append((int(val), color))
    return result

def parse_line(line):
    try:
        return parse_line_aux(line)
    except:
        raise Exception(f"Invalid input |{line}|")

def parse_line_aux(line):
    left, right = line.strip().split(":")
    id = int(
        left.replace("Game ", "")
    )

    input_sets = right.split(";")
    sets = [
        parse_set(input_set)
        for input_set in input_sets
    ]

    return Game(
        id=id,
        sets=sets
    )

def set_to_str(set):
    return ", ".join(
        f"{val} {color}" for val, color in set
    )

@dataclass
class Game:
    id: int
    sets: list

    def fewest_cubes(self, info):
        quantities = {
            "red": 0,
            "green": 0,
            "blue": 0
        }    

        for set in self.sets:
            for val, color in set:
                quantities[color] = max(val, quantities[color])

        return { col: val for col, val in quantities.items() if val > 0 }

    def __str__(self) -> str:
        sets = "; ".join(
            set_to_str(set) for set in self.sets
        )

        return f"Game {self.id}: {sets}"
    
    def is_possible(self, info):
        for set in self.sets:
            for val, color in set:
                if info[color] < val:
                    return False
                
        return True
    
def power(result):    
    p = 1
    for v in result.values():
        p *= v
    
    return p

quantities = {
    "red": 12,
    "green": 13,
    "blue": 14
}

input = "input.txt"

def main():
    games = (parse_line(line) for line in read_lines(input))
    valid_games = (
        game.id
        for game in games
        if game.is_possible(quantities)
    )

    print(sum(valid_games))

def main2():
    games = (parse_line(line) for line in read_lines(input))
    powers = (
        power(game.fewest_cubes(quantities))
        for game in games
    )
    print(sum(powers))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        unittest.main()
    else:
        main2()