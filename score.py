from shapely.strtree import STRtree
from shapely.geometry import Point, LineString

LEAF_COST = 10
LEAF_MAX_GAIN = 100
NO_LEAF_COST = 10000000
EXPANDING_PAST_WINDOW_COST = 2000


def make_rtree(leaf_positions, branch_positions, r):
    return STRtree(
        [Point(x, y).buffer(r, resolution=1) for x, y in leaf_positions]
        + [LineString([(x1, y1), (x2, y2)]) for x1, y1, x2, y2 in branch_positions]
    )


def shadows(x, y, sx, sy, rtree):
    # print(rtree.query(LineString([(x, y), (sx, sy)])))
    return len(rtree.query(LineString([(x, y), (sx, sy)])))


def fitness(
    leaf_positions,
    branch_positions,
    sx=300,
    sy=300,
    sx2=-300,
    sy2=300,
    r=5,
):
    fitness = 0

    geom = make_rtree(leaf_positions, branch_positions, r)

    if len(leaf_positions) == 0:
        fitness -= NO_LEAF_COST

    for x, y in leaf_positions:
        fitness -= LEAF_COST

        if x < -400 or x > 400 or y > 400 or y < 0:
            fitness -= EXPANDING_PAST_WINDOW_COST

        if shadows(x, y, sx, sy, geom) < 3:
            fitness += LEAF_MAX_GAIN

        if shadows(x, y, sx2, sy2, geom) < 3:
            fitness += LEAF_MAX_GAIN

    return fitness