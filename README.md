# PCB Layout Optimization via Multi-Objective GA

In this project, the main task is to optimize the position of components of different shape, dimension and with different pins layout in a rectangular pcb board of given dimension. The objective functions taken into account are
- Maximum temperature reached in the board
- Total distance between pins that needs to be collected
- Total area occupied by components

---


![Example of PCB](images/example_of_pcb.png)
![Population results](images/Evolved_pop_vs_random_pop.png)
---

## File structure
 - Compnent_class.py: Definition of the Component class and the Pin class
 - Example_of_use.ipynb: Example of an entire pipeline as notebook with intermediate plots and results
 - Genetic_algorithm.py: Functions used for the GA (random population, crossover, different mutations...)
 - main.py: Same as Example_of_use but in a .py file
 - NSGA_II_implementation.py: Functions used for the Multi-objective optimization (NSGAII)
 - PCB_class.py: Definition of the PCB class (individual)
 - Plots.py
 - utils.py


