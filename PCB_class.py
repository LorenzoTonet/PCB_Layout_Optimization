import random
import math
import numpy as np

from shapely.geometry import Polygon, Point
from shapely.affinity import rotate, translate
from typing import List, Tuple, Dict, Optional

from Component_class import Component, Pin
from utils import hybrid_distance

vec2D = Tuple[float, float]
Link = Tuple[Pin, Pin]

class PCB:
    def __init__(self, max_width: float, max_height: float, components: List[Component], links: List[Link] = []):
        self.width = max_width
        self.height = max_height
        
        self.components = {c.id: c.clone() for c in components}

        self.links = [
            ((c1, p1), (c2, p2))
            for ((c1, p1), (c2, p2)) in links
        ]
    
    def clone(self):
        """Return an object-clone of the PCB."""
        return PCB(
            max_width=self.width,
            max_height=self.height,
            components=[c.clone() for c in self.components.values()],
            links=[link for link in self.links]
        )
    
    def random_placement(self):
        """Randomly place all components within the boundaries."""
        for comp in self.components:
            x = random.uniform(self.components[comp].size_x / 2, self.width - self.components[comp].size_x / 2)
            y = random.uniform(self.components[comp].size_y / 2, self.height - self.components[comp].size_y / 2)
            rand_angle = random.uniform(0, 360)

            self.components[comp].move((x, y))
            self.components[comp].rotate(rand_angle)

    def get_pin(self, comp_id, pin_id):
        """Return the pin object given component and pin IDs."""
        comp = self.components[comp_id]
        return next(p for p in comp.pins if p.id == pin_id)

    def calculate_occupied_area(self):
        """Calculate the total occupied area (the minimum bounding rectangle) to contain all components."""
        xs = []
        ys = []

        for comp in self.components:
            shape = self.components[comp].get_shape()
            minx, miny, maxx, maxy = shape.bounds
            xs.extend([minx, maxx])
            ys.extend([miny, maxy])

        return (max(xs) - min(xs)) * (max(ys) - min(ys))

    def total_pin_distance(self):
        """Calculate the total distance between linked pins using hybrid distance metric."""
        dist = 0
        for (c1, p1), (c2, p2) in self.links:
            pin1 = self.get_pin(c1, p1)
            pin2 = self.get_pin(c2, p2)

            pos1 = (pin1.absolute_x, pin1.absolute_y)
            pos2 = (pin2.absolute_x, pin2.absolute_y)

            # heuristics based on the busses layout of real PCBs (a weighted sum of Euclidean and Manhattan distances)
            dist += hybrid_distance(pos1, pos2, alpha=0.3, beta=0.7)

        return dist
    
    def resolve_conflicts(self, max_iterations: int = 50):
        """Resolve overlaps between components by moving one of them away from the other."""
        for _ in range(max_iterations):
            overlaps = self.detect_overlaps()
            if not overlaps:
                return 0
            for compA, compB, area in overlaps:

                ax, ay = self.components[compA].position
                bx, by = self.components[compB].position
                angle = math.atan2(by - ay, bx - ax)
                # heuristic based on the overlap area (+1 to avoid near-zero distance)
                distance = math.sqrt(area) +1
                new_bx = bx + math.cos(angle) * distance
                new_by = by + math.sin(angle) * distance
                self.components[compB].move((new_bx, new_by))

    def detect_overlaps(self):
        """Detect overlapping components using Shapely and return a list of tuples (compA_id, compB_id, overlap_area)."""
        overlaps = []
        
        comp_ids = list(self.components.keys())
        
        shapes = {cid: self.components[cid].get_shape() for cid in comp_ids}
        
        for i, compA_id in enumerate(comp_ids):
            shapeA = shapes[compA_id]
            for compB_id in comp_ids[i + 1:]:
                shapeB = shapes[compB_id]
                
                if shapeA.intersects(shapeB):
                    overlap_area = shapeA.intersection(shapeB).area
                    overlaps.append((compA_id, compB_id, overlap_area))
        
        return overlaps
    
    def calculate_max_temp(self, resolution=100):
        """Calculate the maximum temperature on the PCB using a discretization of the space of resolution x resolution."""
        xs = np.linspace(0, self.width, resolution)
        ys = np.linspace(0, self.height, resolution)

        X, Y = np.meshgrid(xs, ys)

        T = np.zeros_like(X)

        for c in self.components:
            T += self.components[c].thermal_field(X, Y)

        max_temp = float(T.max())

        return max_temp, T