import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon, Circle as MplCircle

import numpy as np
from typing import Tuple

vec2D = Tuple[float, float]


def _shapely_to_mpl_patches(shape, edgecolor='black', facecolor='none', linewidth=1.5):

    patches = []

    if shape is None or shape.is_empty:
        return patches

    geom_type = shape.geom_type

    if geom_type == 'Polygon':
        exterior_coords = list(shape.exterior.coords)
        patches.append(MplPolygon(exterior_coords, closed=True, fill=(facecolor != 'none'),
                                 edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth))
        
        for interior in shape.interiors:
            interior_coords = list(interior.coords)

            patches.append(MplPolygon(interior_coords, closed=True, fill=True,
                                     edgecolor=edgecolor, facecolor='white', linewidth=linewidth))

    elif geom_type == 'MultiPolygon':
        for poly in shape.geoms:
            patches.extend(_shapely_to_mpl_patches(poly, edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth))

    elif geom_type == 'Point':
        r = 0.5
        patches.append(MplCircle((shape.x, shape.y), radius=r, edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth))

    elif geom_type == 'LineString':
        coords = list(shape.coords)
        patches.append(MplPolygon(coords, closed=False, fill=False, edgecolor=edgecolor, linewidth=linewidth))

    elif geom_type == 'GeometryCollection':
        for geom in shape.geoms:
            patches.extend(_shapely_to_mpl_patches(geom, edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth))

    else:
        try:
            exterior_coords = list(shape.exterior.coords)
            patches.append(MplPolygon(exterior_coords, closed=True, fill=(facecolor != 'none'),
                                     edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth))
        except Exception:
            pass

    return patches


def plot_pcb(
    pcb,
    show_pins=True,
    show_links=True,
    show_temp=False,
    temp_resolution=100,
    temp_alpha=0.6,
    component_facecolor='none'
):
    """
    Plot del PCB con componenti, pin, link e opzionalmente la mappa termica.
    
    FIXED: Now correctly handles pcb.components as a dictionary.
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, pcb.width)
    ax.set_ylim(0, pcb.height)
    ax.set_aspect('equal')
    ax.set_title("PCB Layout")

    if show_temp:
        _, T = pcb.calculate_max_temp(temp_resolution)

        xs = np.linspace(0, pcb.width, temp_resolution)
        ys = np.linspace(0, pcb.height, temp_resolution)

        ax.imshow(
            T,
            origin='lower',
            extent=[0, pcb.width, 0, pcb.height],
            cmap='inferno',
            alpha=temp_alpha
        )

        cbar = plt.colorbar(ax.images[-1], ax=ax, label="Temperature")
        cbar.ax.tick_params(labelsize=8)

    for comp_id in pcb.components:
        comp = pcb.components[comp_id]
        shape = comp.get_shape()

        patches = _shapely_to_mpl_patches(
            shape,
            edgecolor='black',
            facecolor=component_facecolor,
            linewidth=1.2,
        )
        for p in patches:
            ax.add_patch(p)

        cx, cy = comp.position
        ax.text(cx, cy, comp.id, ha='center', va='center', fontsize=9, zorder=10)

        if show_pins:
            for pin in comp.pins:
                
                if pin.absolute_x is None or pin.absolute_y is None:
                    comp.update_absolute_pin_position()

                px = pin.absolute_x
                py = pin.absolute_y

                ax.plot(px, py, marker='o', color='k', markersize=4, zorder=12)
                ax.text(px + 0.5, py + 0.5, pin.id,
                        fontsize=7, ha='left', va='bottom', zorder=13)

    if show_links and hasattr(pcb, 'links') and pcb.links:
        for (c1_id, p1_id), (c2_id, p2_id) in pcb.links:

            comp1 = pcb.components[c1_id]
            comp2 = pcb.components[c2_id]

            pin1 = next(p for p in comp1.pins if p.id == p1_id)
            pin2 = next(p for p in comp2.pins if p.id == p2_id)

            if pin1.absolute_x is None or pin2.absolute_x is None:
                comp1.update_absolute_pin_position()
                comp2.update_absolute_pin_position()

            ax.plot(
                [pin1.absolute_x, pin2.absolute_x],
                [pin1.absolute_y, pin2.absolute_y],
                linestyle='-',
                linewidth=0.8,
                color='gray',
                zorder=5,
            )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()