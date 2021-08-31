import random
from score import fitness
from grow import new_random_code, grow_tree, point_mutate
from timeit import default_timer as timer
import multiprocessing

POPULATION_SIZE = 50
GENERATIONS = 100
CODE_LENGTH = 200
N_SAVE = 10
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
            print(n)
            save = population[:N_SAVE]
            for i in range(N_SAVE, POPULATION_SIZE):
                population[i] = random.choice(save).copy()
                for _ in range(N_MUTATE):
                    point_mutate(population[i])
        except KeyboardInterrupt:
            break

    from draw import draw

    # print(*grow_tree(population[0]))
    # print(population[0])
    draw(*grow_tree(population[0]))
    import tkinter

    tkinter.mainloop()