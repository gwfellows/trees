import numpy as np
from collections import deque
from math import sin, cos

MININT8 = np.iinfo(np.int8).min
MAXINT8 = np.iinfo(np.int8).max


def new_random_code(length):
    return np.random.randint(
        low=MININT8,
        high=MAXINT8,
        size=length,
        dtype=np.int8,
    )


def point_mutate(code):
    code[np.random.randint(0, code.shape[0])] = np.random.randint(
        low=MININT8, high=MAXINT8, dtype=np.int8
    )


def safe_pop(stack, default=0):
    try:
        return stack.pop()
    except IndexError:
        return default


def grow_bud(pos, code, n):
    offspring = []
    history = deque()
    ang = 0
    stack = deque()
    x, y = pos

    for instruction in code:
        if instruction >= 0:  # number
            stack.append(int(instruction))
        else:
            instruction %= 12
            instruction += 1
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
