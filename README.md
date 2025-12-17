# PCB Layout Optimization via Multi-Objective GA

In this project, the main task is to optimize the position of components of different shape, dimension and with different pins layout in a rectangular pcb board of given dimension. The objective functions taken into account are
- Maximum temperature reached in the board
- Total distance between pins that needs to be connected
- Total area occupied by components

To solve this multi-objective optimization problem, the project uses a custom implementation of the NSGA-II evolutionary algorithm. Candidate solutions are represented as PCB layouts, and several domain-specific genetic operators are defined to explore the search space effectively:

- Crossover between PCB layouts: combines two parent boards by mixing component positions and orientations in a consistent way, generating children that inherit structural traits from both.

- Rotation mutation: randomly rotates one or more components, allowing the algorithm to explore different pin alignments and spatial configurations.

- Position mutation: perturbs component coordinates on the board, enabling fine-grained local exploration and helping escape premature convergence.

These operators, together with NSGA-II’s non-dominated sorting and crowding distance mechanisms, allow the algorithm to evolve a diverse set of Pareto-optimal PCB layouts balancing thermal, wiring, and area objectives.

---

## File structure

```
PCB_Layout_Optimization/
├── Component_class.py           # Definition of the Component class and the Pin class
├── PCB_class.py                 # Definition of the PCB class (individual)
├── Genetic_algorithms.py        # Functions used for the GA (random population, crossover, different mutations...)
├── NSGA_II_implementation.py    # Functions used for the Multi-objective optimization (NSGAII)
├── Plots.py                     # Plot functions
├── utils.py                     # Utility functions
├── main.py                      # Same as Example_of_use but in a .py file
├── Example_of_use.ipynb         # Example of an entire pipeline as notebook with intermediate plots and results
├── PCB - layout optimization.pdf # Project presentation slides
└── images/                      # Images and results
```

![Example of PCB](images/example_of_pcb.png)
![Population results](images/Evolved_pop_vs_random_pop.png)

---



