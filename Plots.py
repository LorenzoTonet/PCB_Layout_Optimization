import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPolygon, Circle as MplCircle
from matplotlib.collections import PatchCollection
from shapely.geometry import Polygon, MultiPolygon, Point, GeometryCollection, LineString
import math
from typing import Tuple

vec2D = Tuple[float, float]


def _shapely_to_mpl_patches(shape, edgecolor='black', facecolor='none', linewidth=1.5):
    """
    Converte una geometria Shapely in una lista di matplotlib.patches compatibili.
    Gestisce Polygon, MultiPolygon, Point (buffer come cerchio), LineString, GeometryCollection.
    """
    patches = []

    if shape is None or shape.is_empty:
        return patches

    geom_type = shape.geom_type

    if geom_type == 'Polygon':
        exterior_coords = list(shape.exterior.coords)
        patches.append(MplPolygon(exterior_coords, closed=True, fill=(facecolor != 'none'),
                                 edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth))
        # gestisci fori (interiors)
        for interior in shape.interiors:
            interior_coords = list(interior.coords)
            # per i fori aggiungiamo con facecolor equal a background -> qui li disegniamo come patch riempita
            patches.append(MplPolygon(interior_coords, closed=True, fill=True,
                                     edgecolor=edgecolor, facecolor='white', linewidth=linewidth))

    elif geom_type == 'MultiPolygon':
        for poly in shape.geoms:
            patches.extend(_shapely_to_mpl_patches(poly, edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth))

    elif geom_type == 'Point':
        # rappresenta come cerchio usando il buffer radius se ha .buffer
        # se il punto è stato creato come buffer, potremmo avere un Polygon -> qui trattiamo il Point come piccolo marker
        # se vuoi trattare Point come cerchio con un raggio, usare shape.buffer(r)
        r = 0.5  # default tiny radius; ma di solito non arriverà qui perché usi Point.buffer per i cerchi
        patches.append(MplCircle((shape.x, shape.y), radius=r, edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth))

    elif geom_type == 'LineString':
        coords = list(shape.coords)
        patches.append(MplPolygon(coords, closed=False, fill=False, edgecolor=edgecolor, linewidth=linewidth))

    elif geom_type == 'GeometryCollection':
        for geom in shape.geoms:
            patches.extend(_shapely_to_mpl_patches(geom, edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth))

    else:
        # fallback generico: prova a prendere .exterior se esiste
        try:
            exterior_coords = list(shape.exterior.coords)
            patches.append(MplPolygon(exterior_coords, closed=True, fill=(facecolor != 'none'),
                                     edgecolor=edgecolor, facecolor=facecolor, linewidth=linewidth))
        except Exception:
            # non sappiamo come disegnare questa geometria; ignoriamo
            pass

    return patches


def plot_pcb(pcb, show_pins=True, show_links=True, component_facecolor='none'):
    """
    Plot robusto che disegna le geometrie Shapely ritornate da comp.get_shape(),
    etichetta componenti e pin, ed eventualmente disegna i link (netlist).
    """
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.set_xlim(0, pcb.width)
    ax.set_ylim(0, pcb.height)
    ax.set_aspect('equal')
    ax.set_title("PCB Layout")

    all_patches = []
    patch_labels = []

    for comp in pcb.components:
        shape = comp.get_shape()  # shapely geometry (Polygon, MultiPolygon, ecc.)

        # crea i patch matplotlib per questa shape
        patches = _shapely_to_mpl_patches(shape, edgecolor='black', facecolor=component_facecolor, linewidth=1.2)

        # aggiungili all'asse
        for p in patches:
            ax.add_patch(p)

        # etichetta il centro del componente
        cx, cy = comp.position
        ax.text(cx, cy, comp.id, ha='center', va='center', fontsize=9, zorder=10)

        # pin: usa absolute_x/absolute_y (assicurati che update_absolute_pin_position sia già stato chiamato)
        if show_pins:
            for pin in comp.pins:
                if getattr(pin, 'absolute_x', None) is None or getattr(pin, 'absolute_y', None) is None:
                    # se non calcolato, calcola al volo (metodo della tua classe)
                    comp.update_absolute_pin_position()
                px = pin.absolute_x
                py = pin.absolute_y
                ax.plot(px, py, marker='o', color='k', markersize=4, zorder=12)
                ax.text(px + 0.5, py + 0.5, pin.id, fontsize=7, ha='left', va='bottom', zorder=13)

    # opzionale: disegna i link tra pin con linee (se presenti)
    if show_links and hasattr(pcb, 'links') and pcb.links:
        for p1, p2 in pcb.links:
            if None in (p1.absolute_x, p1.absolute_y, p2.absolute_x, p2.absolute_y):
                # assicura calcolo posizioni pin
                p1_comp = next((c for c in pcb.components if p1 in c.pins), None)
                p2_comp = next((c for c in pcb.components if p2 in c.pins), None)
                if p1_comp: p1_comp.update_absolute_pin_position()
                if p2_comp: p2_comp.update_absolute_pin_position()

            ax.plot([p1.absolute_x, p2.absolute_x], [p1.absolute_y, p2.absolute_y],
                    linestyle='-', linewidth=0.8, color='gray', zorder=5)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.show()
