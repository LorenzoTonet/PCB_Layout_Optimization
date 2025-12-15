import random

from PCB_class import PCB


def generate_random_population(pcb_template: PCB, population_size: int):
    """Generate a random PCB population based on a template PCB"""
    population = []
    for _ in range(population_size):

        new_pcb = PCB(
            max_width=pcb_template.width,
            max_height=pcb_template.height,
            components=[c.clone() for c in pcb_template.components.values()],
            links=[link for link in pcb_template.links]
        )

        new_pcb.random_placement()
        new_pcb.resolve_conflicts()
        population.append(new_pcb)

    return population

def crossover(parent1: PCB, parent2: PCB, n: int, crossover_rate: float = 0.9):
    """Perform crossover between two parent PCBs by swapping n components"""
    child1 = parent1.clone()
    child2 = parent2.clone()

    comp_ids = random.sample(list(child1.components.keys()), n)

    for cid in comp_ids:
        c1 = child1.components[cid]
        c2 = child2.components[cid]

        pos1, rot1 = c1.position, c1.rotation
        pos2, rot2 = c2.position, c2.rotation

        c1.position = pos2
        c1.rotation = rot2
        c1.update_absolute_pin_position()

        c2.position = pos1
        c2.rotation = rot1
        c2.update_absolute_pin_position()

    child1.resolve_conflicts()
    child2.resolve_conflicts()

    return child1, child2


def mutate_rotation(pcb: PCB, mutation_rate: float = 0.1):
    """Mutate the rotation of a random component in the PCB with a given mutation rate"""
    if random.random() < mutation_rate:
        comp = random.choice(list(pcb.components.values()))
        angle = random.randint(0,359)
        comp.rotate(angle)
        pcb.resolve_conflicts()

def mutate_position(pcb: PCB, mutation_rate: float = 0.1):
    """Mutate the position of a random component in the PCB with a given mutation rate (can be very impactful)"""
    if random.random() < mutation_rate:

        comp = random.choice(list(pcb.components.values()))

        # to avoid problems with out-of-bound placements
        comp_max_dim = max(comp.size_x, comp.size_y)

        x = random.uniform(comp_max_dim, pcb.width - comp_max_dim)
        y = random.uniform(comp_max_dim, pcb.height - comp_max_dim)
        comp.move((x, y))
        pcb.resolve_conflicts()

def tournament_select(population, ranks, crowding):
    """Select an individual from the population using tournament selection based on ranks and if needed crowding distance"""

    i, j = random.sample(range(len(population)), 2)

    if ranks[i] < ranks[j]:
        return population[i]
    if ranks[j] < ranks[i]:
        return population[j]

    if crowding[i] > crowding[j]:
        return population[i]
    else:
        return population[j]