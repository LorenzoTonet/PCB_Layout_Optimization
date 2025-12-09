import random
import math
import numpy as np

from shapely.geometry import Polygon, Point
from shapely.affinity import rotate, translate
from typing import List, Tuple, Dict, Optional
from Component_class import Component, Pin

vec2D = Tuple[float, float]
Link = Tuple[Pin, Pin]


def man_distance(p1: vec2D, p2: vec2D) -> float:
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def eucl_distance(p1: vec2D, p2: vec2D) -> float:
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def hybrid_distance(p1: vec2D, p2: vec2D, alpha: float = 0.5, beta: float = 0.5) -> float:
    return alpha*eucl_distance(p1, p2) + beta*man_distance(p1, p2)

