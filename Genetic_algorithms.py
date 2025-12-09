import matplotlib.pyplot as plt
import random

from PCB_class import PCB
from Component_class import Component, Pin
from Plots import plot_pcb
from copy import deepcopy

def generate_random_population(pcb_template: PCB, population_size: int):
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

def crossover(parent1: PCB, parent2: PCB, n: int):
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
    if random.random() < mutation_rate:
        comp = random.choice(list(pcb.components.values()))
        angle = random.choice([90,180,270])
        comp.rotate(angle)
        pcb.resolve_conflicts()

def mutate_position(pcb: PCB, mutation_rate: float = 0.1):
    if random.random() < mutation_rate:
        comp = random.choice(list(pcb.components.values()))
        x = random.uniform(comp.size_x / 2, pcb.width - comp.size_x / 2)
        y = random.uniform(comp.size_y / 2, pcb.height - comp.size_y / 2)
        comp.move((x, y))
        pcb.resolve_conflicts()

