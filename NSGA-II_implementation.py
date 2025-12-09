
from PCB_class import PCB

import numpy as np

def evaluation(pcb: PCB) -> np.array:
    """Evaluate the PCB layout based on multiple objectives."""

    wire_length = pcb.total_pin_distance()
    max_temperature = pcb.max_temperature()
    pcb_area = pcb.calculate_occupied_area()

    return np.array([wire_length, max_temperature, pcb_area])

def dominates(ind1: np.array, ind2: np.array) -> bool:
    """Check if ind1 dominates ind2."""

    obs1 = evaluation(ind1)
    obs2 = evaluation(ind2)

    return np.all(obs1 <= obs2) and np.any(obs1 < obs2)

def non_dominated_sort(population: list) -> list:

    # pareto front = {rank: [individualas]}
    n = len(population)
    pareto_front = {}

    domination_count = np.zeros(n, dtype=int)
    dominated_solutions = [[] for _ in range(n)]
    ranks = np.zeros(n, dtype=int)
    fronts = [[]]

    for ind1 in range(n):
        for ind2 in range(n):
            if ind1 == ind2:
                continue
            if dominates(population[ind1], population[ind2]):
                dominated_solutions[ind1].append(ind2)
            elif dominates(population[ind2], population[ind1]):
                domination_count[ind1] += 1

        if domination_count[ind1] == 0:
            ranks[ind1] = 0
            fronts[0].append(ind1)

