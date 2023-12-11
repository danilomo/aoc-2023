import unittest
import sys

sample_input = """0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45"""

def parse_line(line):
    return [int(val.strip()) for val in line.split(" ")]

def next_line(predictions):
    result = []
    for i in range(1, len(predictions)):
        result.append(predictions[i] - predictions[i - 1])

    return result

def top(l):
    return l[len(l) - 1]

def extrapolate(predictions):
    lines = get_lines(predictions)
    lines.reverse()
    lines[0].append(0)
    for i in range(1, len(lines)):
        lines[i].append(top(lines[i]) + top(lines[i - 1]))

    return top(top(lines))


def get_lines(predictions):
    lines = [predictions]
    while True:
        next = next_line(top(lines))
        lines.append(next)
        if all(val == 0 for val in next):   
            break

    return lines


class TestSuite(unittest.TestCase):
    def test_next_line(self):
        preds = [0, 3, 6, 9, 12, 15]
        next = [3, 3, 3, 3, 3]

        self.assertEqual(next, next_line(preds))

    def test_next_lines(self):
        preds = [1, 3, 6, 10, 15, 21]
        expected = [
            [1, 3, 6, 10, 15, 21],
            [2, 3, 4, 5, 6],
            [1, 1, 1, 1],
            [0, 0, 0],
        ]

        self.assertEqual(expected, get_lines(preds))

    def test_extrapolate(self):
        lines = (line.strip() for line in sample_input.split("\n"))
        self.assertEqual(
            [18, 28, 68],
            [extrapolate(input) for input in (parse_line(line) for line in lines)],
        )


def read_lines(file_name):
    with open(file_name) as handle:
        return [line.strip() for line in handle]

def main():
    lines = list(read_lines(sys.argv[1]))
    print(sum(extrapolate(input) for input in (parse_line(line) for line in lines)))

def main2():
    lines = list(read_lines(sys.argv[1]))
    print(sum(extrapolate(list(reversed(input))) for input in (parse_line(line) for line in lines)))


if __name__ == "__main__":
    if len(sys.argv) == 1:
        unittest.main()
    else:
        main2()