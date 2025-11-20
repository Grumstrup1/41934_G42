from collections import Counter
from .utils import categorize_window, lookup_price, match_size, match_material

# -----------------------------
# ANALYSIS FUNCTION
# -----------------------------

def analyze_ifc(model, claimed_windows_db=None):
    """
    Analyze IFC model windows and return counts, total area, cost, and match results.

    Returns:
        windows: list of IfcWindow
        type_counts: Counter per window category
        total_area: total area of all windows
        total_estimated_cost: total estimated cost
        match_results: list of dicts with match info per claimed window
    """
    windows = model.by_type("IfcWindow")
    type_counts = Counter()
    total_area = 0.0
    total_estimated_cost = 0.0

    if claimed_windows_db is None:
        claimed_windows_db = []

    # Prepare matching counters for each claimed window
    match_results = []
    for cw in claimed_windows_db:
        match_results.append({
            "window": cw,
            "size_match": 0,
            "material_match": 0,
            "both_match": 0
        })

    for w in windows:
        height = getattr(w, "OverallHeight", None)
        width = getattr(w, "OverallWidth", None)

        if height and width:
            area = (height / 1000) * (width / 1000)
            total_area += area
            total_estimated_cost += lookup_price(area)

            category = categorize_window(area)
            type_counts[category] += 1

            for result in match_results:
                cw = result["window"]
                if match_size(w, cw):
                    result["size_match"] += 1
                if match_material(w, cw):
                    result["material_match"] += 1
                if match_size(w, cw) and match_material(w, cw):
                    result["both_match"] += 1

    return windows, type_counts, total_area, total_estimated_cost, match_results
