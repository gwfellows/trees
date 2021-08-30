import random
from score import fitness
from grow import new_random_code, grow_tree, point_mutate

POPULATION_SIZE = 2000
GENERATIONS = 2000
CODE_LENGTH = 200
N_SAVE = 20
N_MUTATE = 4

if __name__ == "__main__":
    population = [new_random_code(CODE_LENGTH) for _ in range(POPULATION_SIZE)]
    for n in range(GENERATIONS):
        try:
            print(n, fitness(*grow_tree(population[0])))
            population.sort(key=lambda code: fitness(*grow_tree(code)), reverse=True)
            save = population[:N_SAVE]
            for i in range(N_SAVE, POPULATION_SIZE):
                population[i] = random.choice(save).copy()
                for _ in range(N_MUTATE):
                    point_mutate(population[i])
        except KeyboardInterrupt:
            break

    from draw import draw

    print(*grow_tree(population[0]))
    print(population[0])
    draw(*grow_tree(population[0]))
    import tkinter

    tkinter.mainloop()
