import random
from score import fitness
from grow import new_random_code, grow_tree, point_mutate
import multiprocessing
import pickle

"""
test various #s of processes
test out seperate components of tree drawing
"""


POPULATION_SIZE = 100
GENERATIONS = 200000
CODE_LENGTH = 100
N_SAVE = 20
N_MUTATE = 5


def score_code(code):
    return fitness(*grow_tree(code))

if __name__ == "__main__":
    population = [new_random_code(CODE_LENGTH) for _ in range(POPULATION_SIZE)]
    for n in range(GENERATIONS):
        try:
            p = multiprocessing.Pool(1) #should be 8 :(
            fitnesses = p.map(score_code, population)
            population = [
                x
                for _, x in sorted(
                    zip(fitnesses, population), key=lambda p: p[0], reverse=True
                )
            ]
            print("{:.3f}%".format(100 * (n + 1) / GENERATIONS).zfill(8), "{:.3f}".format(sorted(fitnesses)[-1]))
            save = population[:N_SAVE]
            for i in range(N_SAVE, POPULATION_SIZE):
                population[i] = random.choice(save).copy()
                for _ in range(N_MUTATE):
                    point_mutate(population[i])
        except KeyboardInterrupt:
            break

    from draw import draw

    with open("test_tree.txt", "wb") as f:
        pickle.dump(population[0], f)
    draw(*grow_tree(population[0]), score_code(population[0]))