import random
from score import fitness
from grow import new_random_code, grow_tree, point_mutate
import multiprocessing

POPULATION_SIZE = 800
GENERATIONS = 2000
CODE_LENGTH = 200
N_SAVE = 20
N_MUTATE = 4


def score_code(code):
    return fitness(*grow_tree(code))


if __name__ == "__main__":
    population = [new_random_code(CODE_LENGTH) for _ in range(POPULATION_SIZE)]
    for n in range(GENERATIONS):
        try:
            p = multiprocessing.Pool(4)
            fitnesses = p.map(score_code, population)
            population = [
                x
                for _, x in sorted(
                    zip(fitnesses, population), key=lambda p: p[0], reverse=True
                )
            ]
            print("{:.2f}%".format(100 * (n + 1) / GENERATIONS).zfill(7))
            save = population[:N_SAVE]
            for i in range(N_SAVE, POPULATION_SIZE):
                population[i] = random.choice(save).copy()
                for _ in range(N_MUTATE):
                    point_mutate(population[i])
        except KeyboardInterrupt:
            break

    from draw import draw

    draw(*grow_tree(population[0]), score_code(population[0]))