import matplotlib.pyplot as plt

def open_ifc(path):
    import ifcopenshell
    try:
        model = ifcopenshell.open(path)
        print("✔ IFC model loaded")
        return model
    except:
        print("❌ Failed to open IFC file")
        return None

# ---------------------------
# Helpers
# ---------------------------
def element_is_external(elem):
    try:
        if hasattr(elem, "IsExternal") and elem.IsExternal is not None:
            return bool(elem.IsExternal)
    except:
        pass
    return False

def element_is_load_bearing(elem):
    try:
        if hasattr(elem, "LoadBearing") and elem.LoadBearing is not None:
            return bool(elem.LoadBearing)
    except:
        pass
    return False

def get_quantity_area(elem):
    """Extract area from IfcQuantityArea if available"""
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

# ---------------------------
# Option 1: Count elements
# ---------------------------
def count_elements(model):
    counts = {
        "WINDOW": len(model.by_type("IfcWindow")),
        "DOOR": len(model.by_type("IfcDoor")),
        "INTERNAL_WALL": 0,
        "EXTERNAL_WALL": 0,
        "FLOOR": len(model.by_type("IfcSlab")),
        "CEILING": len(model.by_type("IfcCovering")),
        "ROOF": len(model.by_type("IfcRoof")),
        "CURTAIN_WALL": len(model.by_type("IfcCurtainWall"))
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

# ---------------------------
# Option 2: Calculate areas
# ---------------------------
def calculate_areas(model, default_areas):
    """
    Calculates areas using:
    - IFC Quantity Area if available (for walls, slabs, coverings, roofs)
    - OverallHeight x OverallWidth for windows/doors
    - Fallback default if no geometry
    Returns areas dict or None if user cancels
    """
    areas = {k: 0.0 for k in default_areas.keys()}
    missing_count = {k: 0 for k in default_areas.keys()}

    def calc_area(elem, elem_type):
        # Use IFC Quantity Area if available for walls/slabs/coverings/roofs
        if elem_type in ["INTERNAL_WALL", "EXTERNAL_WALL", "FLOOR", "CEILING", "ROOF"]:
            q_area = get_quantity_area(elem)
            if q_area:
                return q_area, False
        # For windows/doors use OverallHeight * OverallWidth
        height = getattr(elem, "OverallHeight", None)
        width = getattr(elem, "OverallWidth", None) or getattr(elem, "OverallLength", None)
        if height and width:
            return float(height)/1000 * float(width)/1000, False
        # fallback
        return default_areas[elem_type], True

    # Windows
    for w in model.by_type("IfcWindow"):
        area, missing = calc_area(w, "WINDOW")
        areas["WINDOW"] += area
        if missing:
            missing_count["WINDOW"] += 1

    # Doors
    for d in model.by_type("IfcDoor"):
        area, missing = calc_area(d, "DOOR")
        areas["DOOR"] += area
        if missing:
            missing_count["DOOR"] += 1

    # Walls
    walls = model.by_type("IfcWall") + model.by_type("IfcWallStandardCase")
    for wall in walls:
        if element_is_load_bearing(wall):
            continue
        elem_type = "EXTERNAL_WALL" if element_is_external(wall) else "INTERNAL_WALL"
        area, missing = calc_area(wall, elem_type)
        areas[elem_type] += area
        if missing:
            missing_count[elem_type] += 1

    # Floors
    for f in model.by_type("IfcSlab"):
        if element_is_load_bearing(f):
            continue
        area, missing = calc_area(f, "FLOOR")
        areas["FLOOR"] += area
        if missing:
            missing_count["FLOOR"] += 1

    # Ceilings
    for c in model.by_type("IfcCovering"):
        if element_is_load_bearing(c):
            continue
        area, missing = calc_area(c, "CEILING")
        areas["CEILING"] += area
        if missing:
            missing_count["CEILING"] += 1

    # Roofs
    for r in model.by_type("IfcRoof"):
        if element_is_load_bearing(r):
            continue
        area, missing = calc_area(r, "ROOF")
        areas["ROOF"] += area
        if missing:
            missing_count["ROOF"] += 1

    # Curtain walls
    for cw in model.by_type("IfcCurtainWall"):
        area, missing = calc_area(cw, "CURTAIN_WALL")
        areas["CURTAIN_WALL"] += area
        if missing:
            missing_count["CURTAIN_WALL"] += 1

    # Summarize missing geometry
    missing_summary = {k: v for k, v in missing_count.items() if v > 0}
    if missing_summary:
        print("\n⚠ Warning: Some elements had no geometry or quantity data:")
        for k, v in missing_summary.items():
            print(f"   {v} {k.replace('_',' ').title()} element(s)")
        proceed = input("Do you want to continue using default values for these? (y/n): ")
        if proceed.lower() != "y":
            print("Calculation cancelled by user.")
            return None

    return areas

# ---------------------------
# Cost estimation
# ---------------------------
def estimate_cost(counts_or_areas, prices):
    return sum(counts_or_areas[k] * prices.get(k,0) for k in counts_or_areas)

# ---------------------------
# Pie chart
# ---------------------------
def show_cost_pie_chart(counts_or_areas, prices):
    labels = []
    values = []
    for k in counts_or_areas:
        cost = counts_or_areas[k] * prices.get(k,0)
        if cost > 0:
            labels.append(k.replace("_"," ").title())
            values.append(cost)
    if not values:
        print("No costs available to show!")
        return
    plt.figure(figsize=(7,7))
    plt.pie(values, labels=labels, autopct="%1.1f%%")
    plt.title("Cost Distribution of Architectural Elements")
    plt.show()
