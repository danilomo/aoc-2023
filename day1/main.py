import sys
from dataclasses import dataclass
import re

digit_set = set("0123456789")

digit_map = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'eightwo': '82',
    'oneight': '18',
    'twone': '21'
}

def transform(string):
    m = re.findall('(1|2|3|4|5|6|7|8|9|twone|eightwo|oneight|one|two|three|four|five|six|seven|eight|nine)', string)
    return "".join([
        digit_map.get(i, i) for i in m
    ])

import unittest
import random

class Test1(unittest.TestCase):

    def test_rona(self):
        for _ in range(0, 90_000):
            r = random.randint(1, 9999999)
            r = str(r).replace('0', '')
            string = r.replace("1", "one").replace("2", "two").replace("3", "three").replace("4", "four").replace("5", "five").replace("6", "six").replace("7", "seven")
            string = string.replace("8", "eight").replace("9", "nine")
            t = transform(string)


            self.assertEqual(int("".join(t)), int(r))

    def test_roninha(self):
        input = "onetwothreightfoursevenineightwo"
        print(input, transform(input))

#unittest.main()


if __name__ == "__main__":
    total = 0

    for line in map(str.rstrip, sys.stdin):
        digits = transform(line)

        val = int(digits[0] + digits[-1])

        print(line, digits, val)

        total += val

    print(total)