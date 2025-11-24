import ifcopenshell
import ifcopenshell.geom
import numpy as np
import matplotlib.pyplot as plt


settings = ifcopenshell.geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)


def open_ifc(path):
    try:
        model = ifcopenshell.open(path)
        print("IFC model loaded successfully.")
        return model
    except:
        print("Failed to open IFC file.")
        return None


def element_is_external(elem):
    try:
        if hasattr(elem, "IsExternal") and elem.IsExternal is not None:
            return bool(elem.IsExternal)
    except:
        pass
    name = str(getattr(elem, "Name", "")).lower()
    return "exterior" in name


def element_is_load_bearing(elem):
    try:
        if hasattr(elem, "LoadBearing") and elem.LoadBearing is not None:
            return bool(elem.LoadBearing)
    except:
        pass
    return False


def get_quantity_area(elem):
    if not hasattr(elem, "IsDefinedBy"):
        return None

    for rel in elem.IsDefinedBy:
        pset = rel.RelatingPropertyDefinition
        if pset and pset.is_a("IfcElementQuantity"):
            for q in getattr(pset, "Quantities", []):
                if q.is_a("IfcQuantityArea"):
                    try:
                        return float(q.AreaValue)
                    except:
                        continue
    return None


def compute_projected_area(verts, faces, axis=2):
    verts2d = np.delete(verts, axis, axis=1)
    area = 0.0
    for f in faces:
        v0, v1, v2 = verts2d[f]
        area += abs(np.cross(v1 - v0, v2 - v0)) / 2.0
    return area


def geom_area(elem, elem_type):
    try:
        shape = ifcopenshell.geom.create_shape(settings, elem)
        geom = shape.geometry
        verts = np.array(geom.verts).reshape((-1, 3))
        faces = np.array(geom.faces).reshape((-1, 3))

        if elem_type in ["INTERNAL_WALL", "EXTERNAL_WALL"]:
            area_xz = compute_projected_area(verts, faces, axis=1)
            area_yz = compute_projected_area(verts, faces, axis=0)
            return max(area_xz, area_yz) * 0.5

        if elem_type in ["CEILING", "ROOF", "FLOOR"]:
            area_xy = compute_projected_area(verts, faces, axis=2)
            return area_xy * 0.5

        return 0.0

    except:
        return 0.0


def count_elements(model):
    counts = {
        "WINDOW": len(model.by_type("IfcWindow")),
        "DOOR": len(model.by_type("IfcDoor")),
        "INTERNAL_WALL": 0,
        "EXTERNAL_WALL": 0,
        "FLOOR": len(model.by_type("IfcSlab")),
        "CEILING": len(model.by_type("IfcCovering")),
        "ROOF": len(model.by_type("IfcRoof")),
        "CURTAIN_WALL": len(model.by_type("IfcCurtainWall")),
    }

    walls = model.by_type("IfcWall") + model.by_type("IfcWallStandardCase")
    for wall in walls:
        if element_is_load_bearing(wall):
            continue
        if element_is_external(wall):
            counts["EXTERNAL_WALL"] += 1
        else:
            counts["INTERNAL_WALL"] += 1

    return counts


def calculate_areas(model, default_areas):
    areas = {k: 0.0 for k in default_areas.keys()}
    approximated = {k: 0 for k in default_areas.keys()}
    defaulted = {k: 0 for k in default_areas.keys()}

    def calc_area(elem, elem_type):
        q_area = get_quantity_area(elem)
        if q_area:
            return q_area, False, False

        if elem_type in ["WINDOW", "DOOR"]:
            h = getattr(elem, "OverallHeight", None)
            w = getattr(elem, "OverallWidth", None) or getattr(elem, "OverallLength", None)
            if h and w:
                return float(h) / 1000 * float(w) / 1000, False, False

        g_area = geom_area(elem, elem_type)
        if g_area > 0:
            return g_area, True, False

        return default_areas.get(elem_type, 1.0), False, True

    def add_area(elems, key):
        for e in elems:
            if key in ["INTERNAL_WALL", "EXTERNAL_WALL"] and element_is_load_bearing(e):
                continue
            area, approx, def_used = calc_area(e, key)
            areas[key] += area
            if approx:
                approximated[key] += 1
            if def_used:
                defaulted[key] += 1

    add_area(model.by_type("IfcWindow"), "WINDOW")
    add_area(model.by_type("IfcDoor"), "DOOR")

    walls = model.by_type("IfcWall") + model.by_type("IfcWallStandardCase")
    for w in walls:
        if element_is_load_bearing(w):
            continue
        key = "EXTERNAL_WALL" if element_is_external(w) else "INTERNAL_WALL"
        area, approx, def_used = calc_area(w, key)
        areas[key] += area
        if approx:
            approximated[key] += 1
        if def_used:
            defaulted[key] += 1

    add_area(model.by_type("IfcSlab"), "FLOOR")
    add_area(model.by_type("IfcCovering"), "CEILING")
    add_area(model.by_type("IfcRoof"), "ROOF")
    add_area(model.by_type("IfcCurtainWall"), "CURTAIN_WALL")

    printed = False

    if any(approximated.values()):
        print("\nThe following elements were approximated using geometric projections:")
        for k, c in approximated.items():
            if c > 0:
                print(f"{k.replace('_',' ').title()}: {c}")
        printed = True

    if any(defaulted.values()):
        print("\nThe following elements used default area values:")
        for k, c in defaulted.items():
            if c > 0:
                print(f"{k.replace('_',' ').title()}: {c}")
        printed = True

    if printed:
        input("\nPress Enter to continue...")

    return areas


def estimate_cost(areas, prices):
    return sum(areas[k] * prices.get(k, 0) for k in areas)


def show_cost_pie_chart(areas, prices):
    labels = []
    values = []
    for k in areas:
        cost = areas[k] * prices.get(k, 0)
        if cost > 0:
            labels.append(k.replace("_", " ").title())
            values.append(cost)

    if not values:
        print("No cost data to show.")
        return

    plt.figure(figsize=(7, 7))
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("Cost Distribution of Architectural Elements")
    plt.show()
