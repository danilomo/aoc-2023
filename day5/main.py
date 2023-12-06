import unittest
from dataclasses import dataclass
import sys
from multiprocessing import Pool

sample = """seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4"""

class TestSuite(unittest.TestCase):
    
    def _test_parse_input(self):
        lines = sample.split("\n")
        input = parse_input(lines)

        #self.assertEqual({79, 14, 55, 13}, input.seeds)
        self.assertEqual(
            input.maps["humidity-to-location"],
            Map([
                Range(60, 56, 37),
                Range(56, 93, 4)
            ])
        )

    def _test_map_value(self):
        map = Map(
            ranges=[
                Range(dst_inf=50, inf=98, length=2), 
                Range(dst_inf=52, inf=50, length=48)
            ]
        )

        self.assertEqual(map.get(98), 50)
        self.assertEqual(map.get(99), 51)
        self.assertEqual(map.get(100), 100)

    def test_parse_input(self):
        lines = sample.split("\n")
        input = parse_input(lines)  
        min_location = float('inf')

        for i, j in input.seed_ranges():
            min_location = min(
                min_location,
                min(input.locations(range(i,i+j)))
            )

        self.assertEqual(min_location, 46)
            
             

def parse_line_map(line):
    values = (int(val.strip()) for val in line.split(" "))
    dst_inf, inf, length = values
    return Range(dst_inf, inf, length)

def parse_input(lines):
    seeds_line = lines[0].replace("seeds: ", "")
    seeds = list(int(val.strip()) for val in seeds_line.split(" "))
    maps = {}
    current_map = ""
    for line in lines[1:]:
        if line == "":
            continue

        if "map" in line:
            current_map = line.replace(" map:", "")
            continue

        if current_map not in maps:
            maps[current_map] = []

        maps[current_map].append(parse_line_map(line))

    return Input(
        seeds=seeds,
        maps={key: Map(values) for key, values in maps.items()}
    )

map_names = [
    "seed-to-soil", 
    "soil-to-fertilizer", 
    "fertilizer-to-water", 
    "water-to-light", 
    "light-to-temperature", 
    "temperature-to-humidity", 
    "humidity-to-location"
]

@dataclass
class Input:
    seeds: list
    maps: dict

    def locations(self, seeds):
        return (
            self.traverse(seed)
            for seed in seeds
        )
    
    def traverse(self, seed):
        input = seed
        for name in map_names:
            output = self.maps[name].get(input)
            if not output:
                return None
            input = output

        return input
    
    def seed_ranges(self):
        for chunk in chunks(self.seeds, 2):
            yield chunk

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

@dataclass
class Map:
    ranges: list

    def get(self, key):
        for range in self.ranges:
            result = range.get(key)
            if result:
                return result

        return key

@dataclass
class Range:    
    dst_inf: int
    inf: int
    length: int

    def get(self, key):
        if self.inf <= key < self.inf + self.length:
            diff = key - self.inf
            return self.dst_inf + diff
        return None

def read_lines(file_name):
    with open(file_name) as handle:
        return [
            line.strip()
            for line in handle
        ]

lines = read_lines(sys.argv[1])
input = parse_input(lines)  
ranges = list(input.seed_ranges())

def compute_min(r):
    i, j = r
    m = min(input.locations(range(i,i+j)))
    print(">", m, "for", r)
    return m

if __name__ == "__main__":
    if len(sys.argv) == 1:
        unittest.main()
    else:
        with Pool(8) as p:
            m = min(p.map(compute_min, ranges))
            print(m)