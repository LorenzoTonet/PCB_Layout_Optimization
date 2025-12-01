from PCB_class import PCB
from Component_class import Component, Pin
from Plots import plot_pcb

from Genetic_algorithms import generate_random_population, crossover, mutate_rotation

if __name__ == "__main__":
    pin1_c1 = Pin(id="P1", relative_x=-5, relative_y=0)
    pin2_c1 = Pin(id="P2", relative_x=5, relative_y=0)
    comp1 = Component(id="C1", shape="rect", size_x=20, size_y=10, pins=[pin1_c1, pin2_c1], position=(0, 0))

    pin3_c2 = Pin(id="P3", relative_x=0, relative_y=-3)
    pin4_c2 = Pin(id="P4", relative_x=0, relative_y=3)
    comp2 = Component(id="C2", shape="circle", size_x=15, size_y=15, pins=[pin3_c2, pin4_c2], position=(50, 50))

    pcb = PCB(max_width=50, max_height=50, components=[comp1, comp2], links=[(pin2_c1, pin3_c2)])

    pcb.random_placement()
    pcb.resolve_conflicts()
    print(f"Number of collisions: {pcb.detect_overlaps()}")
    print(f"Total pin distance: {pcb.total_pin_distance()}")
    print(f"Total area occupied: {pcb.calculate_occupied_area()}")
    plot_pcb(pcb)

    mutate_rotation(pcb, mutation_rate=1.0)
    pcb.resolve_conflicts()
    print("After mutation:")
    print(f"Number of collisions: {pcb.detect_overlaps()}")
    print(f"Total pin distance: {pcb.total_pin_distance()}")
    print(f"Total area occupied: {pcb.calculate_occupied_area()}")
    plot_pcb(pcb)