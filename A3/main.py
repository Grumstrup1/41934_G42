from utils import open_ifc, count_elements, calculate_areas, estimate_cost, show_cost_pie_chart

prices = {
    "WINDOW": 2500,
    "DOOR": 1800,
    "INTERNAL_WALL": 900,
    "EXTERNAL_WALL": 1600,
    "FLOOR": 1100,
    "CEILING": 650,
    "ROOF": 1400,
    "CURTAIN_WALL": 3200
}

default_areas = {
    "WINDOW": 2.0,
    "DOOR": 2.0,
    "INTERNAL_WALL": 10.0,
    "EXTERNAL_WALL": 10.0,
    "FLOOR": 20.0,
    "CEILING": 20.0,
    "ROOF": 30.0,
    "CURTAIN_WALL": 10.0
}


def main():
    print("=== IFC ARCH Cost Estimator ===")
    path = input("Enter IFC file path: ").replace('"', '')
    model = open_ifc(path)
    if not model:
        return

    while True:
        print("\n--- Menu ---")
        print("1) Show element count")
        print("2) Show element areas")
        print("3) Estimate cost")
        print("4) Change element price")
        print("5) Change element default area")
        print("6) Show cost pie chart")
        print("7) Quit")

        choice = input("Select option: ")

        if choice == "1":
            counts = count_elements(model)
            print("\nElement counts:")
            for k,v in counts.items():
                print(f"{k}: {v}")

        elif choice == "2":
            areas = calculate_areas(model, default_areas)
            print("\nElement areas (m²):")
            for k,v in areas.items():
                print(f"{k}: {v:.2f}")

        elif choice == "3":
            areas = calculate_areas(model, default_areas)
            total_cost = estimate_cost(areas, prices)
            print(f"\nEstimated total cost: {total_cost:,.2f} DKK")

        elif choice == "4":
            print("\nCurrent prices (DKK/m²):")
            for k,v in prices.items():
                print(f"{k}: {v}")
            key = input("Enter element type to change: ").upper()
            if key in prices:
                prices[key] = float(input("New price: "))
            else:
                print("Invalid type")

        elif choice == "5":
            print("\nCurrent default fallback areas:")
            for k,v in default_areas.items():
                print(f"{k}: {v}")
            key = input("Enter element type to change: ").upper()
            if key in default_areas:
                default_areas[key] = float(input("New area: "))
            else:
                print("Invalid type")

        elif choice == "6":
            areas = calculate_areas(model, default_areas)
            show_cost_pie_chart(areas, prices)

        elif choice == "7":
            print("Quitting...")
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()
