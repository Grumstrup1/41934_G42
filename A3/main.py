from utils import open_ifc, count_elements, calculate_areas, estimate_cost, show_cost_pie_chart

# Default prices and areas per element
prices = {
    "WINDOW": 200,
    "DOOR": 150,
    "INTERNAL_WALL": 50,
    "EXTERNAL_WALL": 80,
    "FLOOR": 60,
    "CEILING": 40,
    "ROOF": 100,
    "CURTAIN_WALL": 120
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
    print("=== Simple IFC Cost Estimator ===")
    path = input("Enter IFC file path: ")
    model = open_ifc(path)
    if not model:
        return

    while True:
        print("\n--- Menu ---")
        print("1) Count architectural elements")
        print("2) Show element areas")
        print("3) Estimate cost")
        print("4) Change prices")
        print("5) Change default areas")
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
            if areas is None:
                continue
            print("\nElement areas:")
            for k,v in areas.items():
                print(f"{k}: {v:.2f} m²")

        elif choice == "3":
            areas = calculate_areas(model, default_areas)
            if areas is None:
                continue
            total_cost = estimate_cost(areas, prices)
            print(f"\nEstimated total cost: ${total_cost:,.2f}")

        elif choice == "4":
            print("\nCurrent prices:")
            for k,v in prices.items():
                print(f"{k}: {v} DKK/m²")
            key = input("Enter element type to change price: ").upper()
            if key in prices:
                try:
                    new_price = float(input(f"Enter new price for {key}: "))
                    prices[key] = new_price
                    print(f"{key} price updated to {new_price}")
                except:
                    print("Invalid value")
            else:
                print("Unknown element type")

        elif choice == "5":
            print("\nCurrent default areas:")
            for k,v in default_areas.items():
                print(f"{k}: {v} m²")
            key = input("Enter element type to change default area: ").upper()
            if key in default_areas:
                try:
                    new_area = float(input(f"Enter new default area for {key}: "))
                    default_areas[key] = new_area
                    print(f"{key} default area updated to {new_area}")
                except:
                    print("Invalid value")
            else:
                print("Unknown element type")

        elif choice == "6":
            areas = calculate_areas(model, default_areas)
            if areas is None:
                continue
            show_cost_pie_chart(areas, prices)

        elif choice == "7":
            print("Quitting...")
            break

        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()
