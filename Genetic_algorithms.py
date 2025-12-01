import matplotlib.pyplot as plt
import random

from PCB_class import PCB
from Component_class import Component, Pin
from Plots import plot_pcb


def generate_random_population(pcb_template: PCB, population_size: int) -> list[PCB]:
    population = []
    for _ in range(population_size):
        
        new_pcb = PCB(
            max_width=pcb_template.width,
            max_height=pcb_template.height,
            components=[Component(
                id=comp.id,
                shape=comp.shape,
                size_x=comp.size_x,
                size_y=comp.size_y,
                pins=comp.pins,
                position=comp.position,
                rotation=comp.rotation
            ) for comp in pcb_template.components],
            links=pcb_template.links
        )
        new_pcb.random_placement()
        population.append(new_pcb)
    return population

def crossover(parent1: PCB, parent2: PCB) -> PCB:
    pass

def mutate_rotation(pcb: PCB, mutation_rate: float = 0.1):
    if random.random() < mutation_rate:
        comp = random.choice(pcb.components)
        angle = random.choice([90,180,270])
        comp.rotate(angle)
        pcb.resolve_conflicts()

