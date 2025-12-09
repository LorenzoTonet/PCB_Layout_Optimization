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
        
        # componenti cloni
        self.components = {c.id: c.clone() for c in components}

        # link identitativi
        self.links = [
            ((c1, p1), (c2, p2))
            for ((c1, p1), (c2, p2)) in links
        ]
    
    def clone(self):
        return PCB(
            max_width=self.width,
            max_height=self.height,
            components=[c.clone() for c in self.components.values()],
            links=[link for link in self.links]
        )
    
    def random_placement(self):
        for comp in self.components:
            x = random.uniform(self.components[comp].size_x / 2, self.width - self.components[comp].size_x / 2)
            y = random.uniform(self.components[comp].size_y / 2, self.height - self.components[comp].size_y / 2)
            rand_angle = random.uniform(0, 360)

            self.components[comp].move((x, y))
            self.components[comp].rotate(rand_angle)

    def get_pin(self, comp_id, pin_id):
        comp = self.components[comp_id]
        return next(p for p in comp.pins if p.id == pin_id)

    def calculate_occupied_area(self):
        xs = []
        ys = []

        for comp in self.components:
            shape = comp.get_shape()
            minx, miny, maxx, maxy = shape.bounds
            xs.extend([minx, maxx])
            ys.extend([miny, maxy])

        return (max(xs) - min(xs)) * (max(ys) - min(ys))

    def total_pin_distance(self):
        dist = 0
        for (c1, p1), (c2, p2) in self.links:
            pin1 = self.get_pin(c1, p1)
            pin2 = self.get_pin(c2, p2)

            pos1 = (pin1.absolute_x, pin1.absolute_y)
            pos2 = (pin2.absolute_x, pin2.absolute_y)

            dist += hybrid_distance(pos1, pos2, alpha=0.3, beta=0.7)

        return dist
    
    def resolve_conflicts(self, max_iterations: int = 50):
        for _ in range(max_iterations):
            overlaps = self.detect_overlaps()
            print(overlaps)
            if not overlaps:
                return 0
            for compA, compB, area in overlaps:
                # Move compB away from compA
                ax, ay = self.components[compA].position
                bx, by = self.components[compB].position
                angle = math.atan2(by - ay, bx - ax)
                distance = math.sqrt(area) +1
                new_bx = bx + math.cos(angle) * distance
                new_by = by + math.sin(angle) * distance
                self.components[compB].move((new_bx, new_by))

    def detect_overlaps(self):
        """Fixed version that handles dictionary components correctly."""
        overlaps = []
        
        # Convert dict to list for iteration
        comp_ids = list(self.components.keys())
        
        # Pre-compute shapes
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
        xs = np.linspace(0, self.width, resolution)
        ys = np.linspace(0, self.height, resolution)

        X, Y = np.meshgrid(xs, ys)

        T = np.zeros_like(X)

        for c in self.components:
            T += self.components[c].thermal_field(X, Y)

        max_temp = float(T.max())

        return max_temp, T