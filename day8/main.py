
import unittest
from dataclasses import dataclass
import sys
from itertools import cycle
import math

DESTINATION = "ZZZ"

sample_input1 = """AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)"""

sample_input2 = """AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)"""

sample_input3 = """11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)"""

@dataclass
class Node:
    place: str
    left: str
    right: str

    def __str__(self):
        return f"{self.place} = ({self.left}, {self.right})"
    
@dataclass
class NodesCollection:
    nodes: list
    nodes_map: dict
    steps: int = 0

    def next(self, direction):        
        m = self.nodes_map
        if direction == "L":
            next = lambda x: m[m[x.left].place]
        else:
            next = lambda x: m[m[x.right].place]

        new_nodes = [next(node) for node in self.nodes]

        self.steps += 1
        self.nodes = new_nodes
    
    def is_final(self):
        return len(self.nodes) == sum(1 for node in self.nodes if node.place[2] == "Z")

def nodes_to_map(nodes):
    result = {}
    for node in nodes:
        result[node.place] = node

    return result

def parse_line(line):
    line = line.replace(" = (", " ") \
               .replace(", ", " ") \
               .replace(")", "")
    return Node(*list(line.split(" ")))

def find_steps(input, nodes):
    nodes_map = nodes_to_map(nodes)
    instructions = cycle(input)
    steps = 0

    place = "AAA"

    for inst in instructions:
        if place == DESTINATION:
            return steps

        steps += 1

        if inst == "L":
            place = nodes_map[place].left
        else:
            place = nodes_map[place].right

def find_ghost_steps(inputs, nodes_list):
    nodes_map = nodes_to_map(nodes_list)
    instructions = cycle(inputs)

    starting_nodes = [node for node in nodes_map.values() if node.place[2] == "A"]
    values = []
    for node in starting_nodes:
        nodes = NodesCollection(
            [node],
            nodes_map=nodes_map
        )

        for inst in instructions:        
            nodes.next(inst)

            if nodes.is_final():
                steps = nodes.steps
                values.append(steps)
                break

    print(math.lcm(*values))



class TestSuite(unittest.TestCase):
    
    def test_parse_line(self):
        lines = [line.strip() for line in sample_input1.split("\n")]

        for line in lines:
            node = parse_line(line)
            self.assertEqual(str(node), line)

    def test_steps(self):
        inputs = [
            ("RL", 2, sample_input1),
            ("LLR", 6, sample_input2)
        ]

        for input, steps, lines in inputs:
            nodes = [parse_line(line.strip()) for line in lines.split("\n")]

            self.assertEqual(
                steps,
                find_steps(input, nodes)
            )

    def test_ghost_steps(self):
        inputs = "LR"
        nodes = [parse_line(line.strip()) for line in sample_input3.split("\n")]
        steps = find_ghost_steps(inputs, nodes)

        self.assertEqual(6, steps)


def read_lines(file_name):
    with open(file_name) as handle:
        return [
            line.strip()
            for line in handle
        ]
    
def main():
    lines = list(read_lines(sys.argv[1]))
    input = lines[0]
    nodes = [parse_line(line) for line in lines[2:]]
    print(find_steps(input, nodes))

def main2():
    lines = list(read_lines(sys.argv[1]))
    input = lines[0]
    nodes = [parse_line(line) for line in lines[2:]]
    print(find_ghost_steps(input, nodes))

if __name__ == "__main__":
    if len(sys.argv) == 1:
        unittest.main()
    else:
        main2()