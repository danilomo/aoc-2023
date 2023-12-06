import functools

sample_input = {
    "time": [7,  15,   30],
    "distance": [9,  40,  200]
}

def sorvete(v, t):
    return v * t

def ways_to_win(time, record):
    total = 0
    for t in range(1, time):
        if sorvete(t, time - t) > record:
            total += 1

    return total

prod = lambda x, y: x * y

def solve_pt1(input):
    print(
        functools.reduce(
            prod,
            (
                ways_to_win(input["time"][i], input["distance"][i]) 
                for i in range(0, len(input["time"]))
            )
        )
    ) 

def solve_pt2(input):
    time = "".join(str(val) for val in input["time"])
    distance = "".join(str(val) for val in input["distance"])

    print(ways_to_win(time, distance))