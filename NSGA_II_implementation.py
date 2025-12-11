from PCB_class import PCB

import numpy as np

def evaluate_objectives(pcb: PCB):
    """ Calculate the three fitness functions"""
    max_temp, _ = pcb.calculate_max_temp()
    occupied_area = pcb.calculate_occupied_area()
    pin_distance = pcb.total_pin_distance()
    
    return np.array([max_temp,occupied_area, pin_distance])


def dominates(objectives_a: np.ndarray, objectives_b: np.ndarray):
    """ Check if a solution dominates another"""

    # used < instead of > because its a problem of minimization so its equal to maximize -fitness(x)
    better_or_equal = np.all(objectives_a <= objectives_b)
    strictly_better = np.any(objectives_a < objectives_b)
    
    return better_or_equal and strictly_better

def fast_non_dominated_sort(population_objectives: np.ndarray, verbose: bool = True):
    """
    Algorithm to build fronts and dominaed-sorting
    Algorithm:
    For each solution p, calculate its dominance count (np) (how many solutions dominate it) and create a list Sp of solutions it dominates.

     1) Build the pareto front (solutions not-dominated by other individuals)
     2) Iterate through each solution q in Sp (solutions p dominates)
     3) Decrease q's dominance count (np) by one
     4) If np becomes zero for q, add q to the next front
     5) repeat from 2)
    """
    n = len(population_objectives)
    domination_count = np.zeros(n, dtype=int) 
    dominated_solutions = [[] for _ in range(n)]
    ranks = np.zeros(n, dtype=int)
    fronts = [[]]
    
    # Pareto front
    for i in range(n):
        for j in range(i + 1, n):
            obj_i = population_objectives[i]
            obj_j = population_objectives[j]
            
            if dominates(obj_i, obj_j):
                dominated_solutions[i].append(j)
                domination_count[j] += 1

            elif dominates(obj_j, obj_i):
                dominated_solutions[j].append(i)
                domination_count[i] += 1
        
        if domination_count[i] == 0:
            ranks[i] = 0
            fronts[0].append(i)
    if verbose:
        print(f"Pareto front: {len(fronts[0])} individuals")
    
    # Other fronts building
    current_front_idx = 0

    while current_front_idx < len(fronts) and len(fronts[current_front_idx]) > 0:
        next_front = []
        
        for i in fronts[current_front_idx]:
            for j in dominated_solutions[i]:

                domination_count[j] -= 1

                if domination_count[j] == 0:
                    ranks[j] = current_front_idx + 1
                    next_front.append(j)
        
        if next_front:
            fronts.append(next_front)
            current_front_idx += 1
            if verbose:
                print(f"Front {current_front_idx + 1}: {len(next_front)} individuals")
        else:
            break
    
    if verbose:
        print(f"Number of fronts: {len(fronts)}")
    
    return fronts, ranks


def calculate_crowding_distance(front_indices: list, population_objectives: np.ndarray):
    """
    Calculate the crowding distance in a front
    
    """
    n = len(front_indices)
    if n <= 2:
        return np.full(n, np.inf)
    
    crowding_distances = np.zeros(n)
    n_objectives = len(population_objectives[0])
    
    for m in range(n_objectives):

        obj_values = np.array([population_objectives[i][m] for i in front_indices])
        sorted_indices = np.argsort(obj_values)
        
        # extreme individuals
        crowding_distances[sorted_indices[0]] = np.inf
        crowding_distances[sorted_indices[-1]] = np.inf
        
        obj_range = obj_values[sorted_indices[-1]] - obj_values[sorted_indices[0]]
        
        if obj_range == 0:
            continue
        
        #  crowding distance for all individuals
        for i in range(1, n - 1):
            crowding_distances[sorted_indices[i]] += (
                obj_values[sorted_indices[i + 1]] - obj_values[sorted_indices[i - 1]]
            ) / obj_range
    
    return crowding_distances


def nsga2_select(population: list, population_objectives: np.ndarray, n_select: int):
    """
    Selection based on dominated sorting of the individuals. Inside the same front, solutions are ranked by crowding distance.
    """
    # non-dominated sorting
    fronts, ranks = fast_non_dominated_sort(population_objectives, verbose=False)

    selected_indices = []
    
    for front in fronts:
        if len(selected_indices) + len(front) <= n_select:

            selected_indices.extend(front)
        else:
            crowding_distances = calculate_crowding_distance(front, population_objectives)
            
            # sort by crowding distance descending
            sorted_front_indices = np.argsort(-crowding_distances)

            n_needed = n_select - len(selected_indices)
            selected_from_front = [front[i] for i in sorted_front_indices[:n_needed]]
            selected_indices.extend(selected_from_front)
            break
    
    
    selected_population = [population[i] for i in selected_indices]
    selected_objectives = [population_objectives[i] for i in selected_indices]
    
    return selected_population, selected_objectives


def get_pareto_front(population: list, population_objectives: np.ndarray):
    """
    Return the pareto front of the population
    """
    fronts, _ = fast_non_dominated_sort(population_objectives, verbose=False)
    pareto_indices = fronts[0]
    
    pareto_population = [population[i] for i in pareto_indices]
    pareto_objectives = [population_objectives[i] for i in pareto_indices]
    
    return pareto_population, pareto_objectives


def calculate_crowding_distance_for_population(pop: list, pop_obj: np.ndarray, fronts: list):
    """
    Compute the crowding dist for the entire population
    """
    n = len(pop)
    distances = [0.0] * n

    for front in fronts:
        cd = calculate_crowding_distance(front, pop_obj)
        for k, i in enumerate(front):
            distances[i] = cd[k]

    return distances