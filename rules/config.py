from collections import Counter

# -----------------------------
# CLAIMED WINDOWS DATABASE
# -----------------------------
CLAIMED_WINDOWS_DB = [
    {
        "name": "Window set: 2 x Udskifte fast vindue af træ, 1.188 x 1.188 mm, 3 lags; "
                "1 x Udskifte vendevindue af træ, 1.188 x 1.188, 3 lags",
        "width_mm": 1188,
        "height_mm": 1188,
        "material": "Wood",
        "count": 330,
        "units_per_window": 3,
        "price_per_window": 18005.60
    },
    # Add more claimed windows here if needed
]

# -----------------------------
# WINDOW PRICE DATABASE BY AREA
# -----------------------------
WINDOW_PRICE_DB = {
    "small": {"min_area": 0, "max_area": 1.5, "price_per_m2": 4000},
    "medium": {"min_area": 1.5, "max_area": 3.0, "price_per_m2": 6100},
    "large": {"min_area": 3.0, "max_area": float("inf"), "price_per_m2": 9000},
}

# -----------------------------
# HELPER FUNCTION
# -----------------------------
def build_claimed_type_counts(claimed_windows, categorize_window):
    """
    Precompute claimed window counts by category.
    
    Parameters:
        claimed_windows (list): List of claimed window dicts
        categorize_window (function): Function to categorize window area
    
    Returns:
        Counter: Number of claimed windows per category
    """
    counts = Counter()
    for cw in claimed_windows:
        area = (cw["width_mm"] / 1000) * (cw["height_mm"] / 1000) * cw.get("units_per_window", 1)
        category = categorize_window(area)
        counts[category] += cw["count"]
    return counts
