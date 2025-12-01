import random
import math

from shapely.geometry import Polygon, Point
from shapely.affinity import rotate, translate
from typing import List, Tuple, Dict, Optional
from Component_class import Component, Pin

vec2D = Tuple[float, float]
Link = Tuple[Pin, Pin]

def man_distance(p1: vec2D, p2: vec2D) -> float:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def eucl_distance(p1: vec2D, p2: vec2D) -> float:
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def hybrid_distance(p1: vec2D, p2: vec2D, alpha: float = 0.5, beta: float = 0.5) -> float:
    return alpha*eucl_distance(p1, p2) + beta*man_distance(p1, p2)


class PCB:
    def __init__(self, max_width: float, max_height: float, components: List[Component], links: List[Link] = []):
        self.width = max_width
        self.height = max_height
        self.components = components
        self.links = links

    def random_placement(self):
        for comp in self.components:
            x = random.uniform(comp.size_x / 2, self.width - comp.size_x / 2)
            y = random.uniform(comp.size_y / 2, self.height - comp.size_y / 2)
            rand_angle = random.uniform(0, 360)

            comp.move((x, y))
            comp.rotate(rand_angle)

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
        for p1, p2 in self.links:
            pos1 = (p1.absolute_x, p1.absolute_y)
            pos2 = (p2.absolute_x, p2.absolute_y)
            dist += hybrid_distance(pos1, pos2, alpha=0.3, beta=0.7)
        return dist


    def calculate_max_temp(self):
        pass
    
    def resolve_conflicts(self):
        overlaps = self.detect_overlaps()
        if not overlaps:
            return 0
        for compA, compB, area in overlaps:
            # Move compB away from compA
            ax, ay = compA.position
            bx, by = compB.position
            angle = math.atan2(by - ay, bx - ax)
            distance = math.sqrt(area)
            new_bx = bx + math.cos(angle) * distance
            new_by = by + math.sin(angle) * distance
            compB.move((new_bx, new_by))

    def detect_overlaps(self):
        overlaps = []
        shapes = {comp: comp.get_shape() for comp in self.components}

        for i, compA in enumerate(self.components):
            shapeA = shapes[compA]
            for compB in self.components[i + 1:]:
                shapeB = shapes[compB]

                if shapeA.intersects(shapeB):
                    overlap_area = shapeA.intersection(shapeB).area
                    overlaps.append((compA, compB, overlap_area))

        return overlaps