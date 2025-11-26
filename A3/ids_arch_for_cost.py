from pathlib import Path
import ifcopenshell
from ifctester import ids, reporter


def ask_ifc_path() -> Path:
    while True:
        print("Enter path to IFC file:")
        raw = input("> ").strip().strip('"')

        if raw == "":
            print("You must enter a file path.\n")
            continue

        p = Path(raw)
        if p.exists() and p.is_file():
            return p
        print(f"File not found: {p}\nTry again.\n")


def add_area_property_spec(my_ids, ifc_entity, spec_name, pset_name, prop_name):
    spec = ids.Specification(name=spec_name)
    spec.applicability.append(ids.Entity(name=ifc_entity))

    req = ids.Property()
    req.propertySet = pset_name
    req.name = prop_name

    spec.requirements.append(req)
    my_ids.specifications.append(spec)


def print_basic_counts(model):
    print("\n--- Element counts in IFC ---")
    types = [
        ("IfcWindow", "Windows"),
        ("IfcDoor", "Doors"),
        ("IfcWall", "Walls"),
        ("IfcWallStandardCase", "Standard walls"),
        ("IfcSlab", "Slabs"),
        ("IfcCovering", "Coverings"),
        ("IfcRoof", "Roofs"),
        ("IfcCurtainWall", "Curtain walls"),
    ]
    for t, label in types:
        print(f"{label:20s}: {len(model.by_type(t))}")


def evaluate_tool_compatibility(results):
    """
    Determine if the model can be used with your cost tool.
    Logic:
    - If ANY areas exist -> tool can run fully (best quality)
    - If 0 area quantities exist but windows/doors have height/width -> tool can run with fallback
    - If neither -> low-quality estimation
    """

    total_passed = results["total_checks_pass"]
    total_checks = results["total_checks"]

    completeness = (total_passed / total_checks) * 100 if total_checks > 0 else 0

    if completeness > 50:
        level = "FULLY SUPPORTED – High quality input"
        detail = (
            "The model contains enough BaseQuantities to run the cost tool with full accuracy."
        )
    elif 1 <= completeness <= 50:
        level = "PARTIALLY SUPPORTED – Medium quality input"
        detail = (
            "The model is missing some quantity data. The tool will use geometry fallback "
            "(OverallHeight/OverallWidth or face area) where needed."
        )
    else:
        level = "SUPPORTED WITH FALLBACK – Low quality input"
        detail = (
            "The model contains no usable QTO quantity sets. The tool will rely on geometry "
            "projection and default rules for most elements."
        )

    return level, completeness, detail


def print_ids_summary(results):
    print("\n--- IDS per specification ---")
    for spec in results["specifications"]:
        name = spec["name"]
        status = "PASS" if spec["status"] else "FAIL"
        total_applicable = spec["total_applicable"]
        checks_pass = spec["total_checks_pass"]
        checks_fail = spec["total_checks_fail"]

        print(f"\n[{status}] {name}")
        print(f"  Applicable elements: {total_applicable}")
        print(f"  Checks: {checks_pass} pass / {checks_fail} fail")


def main():
    # ---- 1. Ask user for IFC path ----
    ifc_path = ask_ifc_path()

    # ---- 2. Load IFC ----
    print("\nLoading IFC...")
    model = ifcopenshell.open(ifc_path)

    # ---- 3. Build IDS programmatically (no XML) ----
    print("Building IDS for ARCH cost tool requirements...")
    my_ids = ids.Ids(title="ARCH cost tool – info requirements")

    add_area_property_spec(my_ids, "IFCWINDOW", "Windows – Area", "Qto_WindowBaseQuantities", "Area")
    add_area_property_spec(my_ids, "IFCDOOR", "Doors – Area", "Qto_DoorBaseQuantities", "Area")
    add_area_property_spec(my_ids, "IFCWALL", "Walls – NetSideArea", "Qto_WallBaseQuantities", "NetSideArea")
    add_area_property_spec(my_ids, "IFCWALLSTANDARDCASE", "WallsSC – NetSideArea", "Qto_WallBaseQuantities", "NetSideArea")
    add_area_property_spec(my_ids, "IFCSLAB", "Slabs – Area", "Qto_SlabBaseQuantities", "Area")
    add_area_property_spec(my_ids, "IFCCOVERING", "Coverings – Area", "Qto_CoveringBaseQuantities", "Area")
    add_area_property_spec(my_ids, "IFCROOF", "Roofs – Area", "Qto_RoofBaseQuantities", "Area")
    add_area_property_spec(my_ids, "IFCCURTAINWALL", "Curtain walls – Area", "BaseQuantities", "Area")

    # ---- 4. Validate ----
    print("\nRunning IDS validation...")
    my_ids.validate(model)

    # ---- 5. JSON report -> compact summary ----
    json_report = reporter.Json(my_ids)
    results = json_report.report()

    # ---- 6. TOOL COMPATIBILITY SUMMARY (NEW!) ----
    level, completeness, detail = evaluate_tool_compatibility(results)

    print("\n===================================")
    print("     COST TOOL COMPATIBILITY")
    print("===================================")
    print(f"Status: {level}")
    print(f"Data completeness score: {completeness:.1f}%")
    print(f"Explanation: {detail}")
    print("===================================\n")

    # ---- 7. IFC element counts ----
    print_basic_counts(model)

    # ---- 8. Detailed per-spec summary ----
    print("\n=== IDS VALIDATION SUMMARY ===")
    print_ids_summary(results)

    # ---- 9. Save output ----
    out_json = ifc_path.with_name("ids_arch_results.json")
    json_report.to_file(str(out_json))
    print(f"\nDetailed JSON saved to: {out_json}")

    out_ids = ifc_path.with_name("ids_arch_programmatic_exported.ids")
    my_ids.to_xml(str(out_ids))
    print(f"Exported IDS file saved to: {out_ids}")


if __name__ == "__main__":
    main()
