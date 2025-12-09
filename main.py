from PCB_class import PCB
from Component_class import Component, Pin
from Plots import plot_pcb

from Genetic_algorithms import generate_random_population, crossover, mutate_rotation
from copy import deepcopy


if __name__ == "__main__":
    # ---------------------------------------------------------
    # 1. Definizione dei componenti e dei pin
    # ---------------------------------------------------------
    pin1_c1 = Pin(id="P1", relative_x=-5, relative_y=0)
    pin2_c1 = Pin(id="P2", relative_x=5, relative_y=0)

    comp1 = Component(
        id="C1",
        shape="rect",
        size_x=20, size_y=10,
        pins=[pin1_c1, pin2_c1],
        position=(21, 21),
        temp_gradient_params=(100, 15)
    )

    pin3_c2 = Pin(id="P3", relative_x=0, relative_y=-3)
    pin4_c2 = Pin(id="P4", relative_x=0, relative_y=3)

    comp2 = Component(
        id="C2",
        shape="circle",
        size_x=15, size_y=15,
        pins=[pin3_c2, pin4_c2],
        position=(20, 20),
        temp_gradient_params=(100, 15)
    )

    # ---------------------------------------------------------
    # 2. Creazione della PCB
    #    links → basati su ID, NON su riferimento ai pin
    # ---------------------------------------------------------
    links = [
        (("C1", "P2"), ("C2", "P3"))   # comp1.pin2 <--> comp2.pin3
    ]

    pcb1 = PCB(
        max_width=50,
        max_height=50,
        components=[comp1, comp2],
        links=links
    )

    # ---------------------------------------------------------
    # 3. Manipolazioni iniziali
    # ---------------------------------------------------------
    #pcb1.random_placement()
    plot_pcb(pcb1, show_temp=True)
    pcb1.resolve_conflicts()
    plot_pcb(pcb1, show_temp=True)
