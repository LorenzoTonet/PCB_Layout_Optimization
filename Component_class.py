from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
vec2D = Tuple[float, float]


@dataclass
class Pin:
    id: str
    relative_x: float
    relative_y: float

class Component:
    def __init__(self, id:str, shape:str, size_x:float, size_y:float, pins:list[Pin], position: vec2D, rotation: float = 0.0, temp_gradient = None):
        pass