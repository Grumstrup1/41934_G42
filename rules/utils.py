# -----------------------------
# UTILITY FUNCTIONS
# -----------------------------

def categorize_window(area):
    """Return category based on window area in m²."""
    if 0 < area <= 1.5:
        return "small"
    elif 1.5 < area <= 3.0:
        return "medium"
    elif area > 3.0:
        return "large"
    else:
        return "unknown"


def window_type_label(category):
    """Return human-readable label for window category."""
    if category == "small":
        return "Small (≤ 1.5 m²)"
    elif category == "medium":
        return "Medium (1.5 > 3.0 m²)"
    elif category == "large":
        return "Large (≥ 3.0 m²)"
    else:
        return category.capitalize()


def get_material(ifc_window):
    """Return the material name of an IfcWindow, if assigned."""
    material_name = None
    if hasattr(ifc_window, "HasAssociations"):
        for rel in ifc_window.HasAssociations:
            if hasattr(rel, "RelatingMaterial"):
                material_name = getattr(rel.RelatingMaterial, "Name", None)
    return material_name


def match_size(ifc_window, claimed_window, tol=10):
    """Check if IFC window matches claimed window size (consider units_per_window)."""
    width = getattr(ifc_window, "OverallWidth", None)
    height = getattr(ifc_window, "OverallHeight", None)
    if width and height:
        scaled_width = claimed_window["width_mm"] * claimed_window.get("units_per_window", 1)
        return abs(width - scaled_width) <= tol and abs(height - claimed_window["height_mm"]) <= tol
    return False


def match_material(ifc_window, claimed_window):
    """Check if IFC window material matches claimed window material."""
    return get_material(ifc_window) == claimed_window["material"]


def lookup_price(area, price_db=None):
    """Estimate window price based on area and price DB."""
    if price_db is None:
        # Default price DB
        price_db = {
            "small": {"min_area": 0, "max_area": 1.5, "price_per_m2": 4000},
            "medium": {"min_area": 1.5, "max_area": 3.0, "price_per_m2": 6100},
            "large": {"min_area": 3.0, "max_area": float("inf"), "price_per_m2": 9000},
        }

    for category, data in price_db.items():
        if data["min_area"] < area <= data["max_area"]:
            return area * data["price_per_m2"]
    return area * 18000  # fallback
