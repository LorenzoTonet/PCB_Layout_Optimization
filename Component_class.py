from dataclasses import dataclass
from typing import Tuple, List
from shapely.geometry import Point, Polygon
from shapely.affinity import rotate, translate
import math

vec2D = Tuple[float, float]


@dataclass
class Pin:
    id: str
    relative_x: float
    relative_y: float
    absolute_x: float = None
    absolute_y: float = None


class Component:
    def __init__(self, id:str, shape:str, size_x:float, size_y:float, pins:list[Pin], position: vec2D, rotation: float = 0.0, temp_gradient = None):
        self.id = id
        self.shape = shape
        self.size_x = size_x
        self.size_y = size_y
        self.pins = pins
        self.position = position
        self.rotation = rotation
        self.temp_gradient = temp_gradient

        self.update_absolute_pin_position()
    
    def get_shape(self):
        """Return the Shapely geometry representing the component."""

        px, py = self.position

        if self.shape == "circle":
            r = max(self.size_x, self.size_y) / 2
            geom = Point(0, 0).buffer(r)  # centered at origin

        else: 
            w, h = self.size_x / 2, self.size_y / 2
            geom = Polygon([
                (-w, -h),
                ( w, -h),
                ( w,  h),
                (-w,  h)
            ])

        geom = rotate(geom, self.rotation, use_radians=False)

        geom = translate(geom, xoff=px, yoff=py)

        return geom

    def intersects(self, other: "Component") -> bool:
        """Detects overlap using Shapely geometry."""
        return self.get_shape().intersects(other.get_shape())

    def rotate(self, angle: float):
        self.rotation = (self.rotation + angle) % 360
        self.update_absolute_pin_position()

    def move(self, new_position: vec2D):
        self.position = new_position
        self.update_absolute_pin_position()

    def get_position(self) -> vec2D:
        return self.position

    def update_absolute_pin_position(self):
            px, py = self.position
            rad = math.radians(self.rotation)

            for pin in self.pins:
                # rotate relative position
                rx = pin.relative_x * math.cos(rad) - pin.relative_y * math.sin(rad)
                ry = pin.relative_x * math.sin(rad) + pin.relative_y * math.cos(rad)

                # translate
                pin.absolute_x = px + rx
                pin.absolute_y = py + ry


            