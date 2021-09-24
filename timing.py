"""
example 1 : 94
example 2 : -30 ish
example 3 : 650
"""

import time
from math import cos, sin
from collections import deque
import pickle


@profile
def safe_pop(stack, default=0):
    try:
        return stack.pop()
    except IndexError:
        return default


@profile
def grow_bud(pos, code, n):
    offspring = []
    history = deque()
    ang = 0
    stack = deque()
    x, y = pos

    for instruction in code:
        if instruction > 12:  # number
            stack.append(instruction - 13)
        else:
            if instruction == 1:  # rotCW
                history.append((x, y, ang))
                ang += safe_pop(stack)
            elif instruction == 2:  # rotCCW
                history.append((x, y, ang))
                ang -= safe_pop(stack)
            elif instruction == 3:  # undo
                x, y, ang = safe_pop(history, (x, y, ang))
            elif instruction == 4:  # move
                history.append((x, y, ang))
                dist = safe_pop(stack)
                x -= sin(ang) * dist
                y += cos(ang) * dist
            elif instruction == 5:  # place
                offspring.append((x, y))
            elif instruction == 6:  # ref n
                stack.append(n)
            elif instruction == 7:  # +
                stack.append(safe_pop(stack) + safe_pop(stack))
            elif instruction == 8:  # -
                stack.append(safe_pop(stack) - safe_pop(stack))
            elif instruction == 9:  # *
                stack.append(safe_pop(stack) * safe_pop(stack))
            elif instruction == 10:  # /
                try:
                    stack.append(safe_pop(stack) / safe_pop(stack, 1))
                except ZeroDivisionError:
                    pass
            elif instruction == 11:  # ref x
                stack.append(x)
            elif instruction == 12:  # ref y
                stack.append(y)

    return offspring


@profile
def grow_tree(code, iters=3):
    bud_positions = [(0, 0)]
    branch_positions = []
    for n in range(iters):
        new_bud_positions = []
        for bud_pos in bud_positions:
            for new_pos in grow_bud(bud_pos, code, n):
                branch_positions.append((*bud_pos, *new_pos))
                new_bud_positions.append(new_pos)
        bud_positions = new_bud_positions
    return bud_positions, branch_positions


for filename in ["test_tree.txt"]:
    with open(filename, "rb") as f:
        grow_times = []
        # score_times = []
        code = pickle.load(f)

        for _ in range(100):
            t1 = time.time()
            grow_tree(code)
            t2 = time.time()
            grow_times.append(t2 - t1)

            # t1 = time.time()
            # w = score.fitness(l, b)
            # t2 = time.time()
            # score_times.append(t2 - t1)

        print("grow time (" + filename + ") :", sum(grow_times) / len(grow_times))
        # print("score time: ", sum(score_times) / len(score_times))