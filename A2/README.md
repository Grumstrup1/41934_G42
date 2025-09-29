# Assignment A2 – Cost Estimation Validation Tool

## A2a: Coding Confidence

**I am confident coding in Python:**
**Score: 3 – Agree**

Our group feels comfortable coding in Python, especially when using libraries such as `ifcopenshell` to parse IFC files and apply logic to check building-related claims. There is still room to improve efficiency, optimization, and extending functionality to other building elements, but we are confident in building functional tools.

---

## A2b: Identify the Claim

**Selected building:** #2516

**Claim / issue to check:**
The claimed *cost estimation* of constructing the building.

**Description of the claim:**
The report for Building #2516 provides a cost estimate for various building elements (e.g., windows). We want to verify whether the claimed numbers of elements and their stated costs match what can be extracted from the actual BIM model (IFC). This allows us to validate whether the reported costs are legitimate and consistent with the model geometry.

**Justification for selection:**
Cost estimation is a central part of building design and construction. Incorrect or inflated cost claims can significantly impact budgets and decision-making. By focusing on windows first (and later extending to doors, walls, and other elements), we can create a tool that checks the validity of reported numbers against the model. This directly supports transparency and reliability in construction projects.

---

## A2c: Use Case

**How would you check this claim?**

* By reading the IFC model with `ifcopenshell` and automatically counting relevant elements (e.g., windows).
* By calculating areas and volumes where needed.
* By comparing extracted values against the reported claims.
* By estimating costs using a price database (e.g., cost per m²) and highlighting mismatches.

**When would this claim need to be checked?**

* During the **design phase**, when cost reports are prepared.
* It can also be valuable in the **planning phase**, before tendering, to ensure claimed numbers are realistic.

**What information does this claim rely on?**

* Quantities of building elements (e.g., number of windows, dimensions).
* Material properties (wood, aluminum, etc.).
* Claimed prices and assembly units (from the cost report).
* Market-based or database-based price per m².

**What phase?**

* **Design and planning phase.**

**What BIM purpose is required?**

* **Analyse**: To check validity of claims.
* **Communicate**: To report mismatches between model and cost report.

**Closest BIM use case:**

* "Cost Estimation" (5D BIM).
* If no exact match exists, this is a new use case: **Automated Validation of Cost Reports from IFC models.**

---

## A2d: Scope the Use Case

*(Diagram will be created separately.)*

---

## A2e: Tool Idea

**Description:**
We are developing a Python-based tool using `ifcopenshell` that automatically validates cost estimation claims from BIM models. The tool reviews the IFC model, extracts relevant elements (starting with windows), calculates their areas and counts, assigns estimated prices, and compares these against claimed costs in reports. It then highlights mismatches in quantities, dimensions, or total costs.

**Business and societal value:**

* **Transparency:** Ensures that reported costs match actual model data, preventing overestimation.
* **Efficiency:** Automates a process that is otherwise manual and error-prone.
* **Trustworthiness:** Helps stakeholders (clients, contractors, auditors) verify that project costs are grounded in real data.
* **Educational value:** Demonstrates the potential of OpenBIM tools in cost validation for students and professionals.

---

## A2f: Information Requirements

**Information needed from IFC:**

* **IfcWindow** (and later IfcDoor, IfcWall, etc.)

  * `OverallHeight` (for dimensions)
  * `OverallWidth` (for dimensions)
  * `HasAssociations → RelatingMaterial` (for material type)
* Element counts
* Element geometry (to calculate areas, m²)

**Where is this in IFC?**

* `IfcWindow.OverallHeight` and `IfcWindow.OverallWidth` give element dimensions.
* `IfcRelAssociatesMaterial → IfcMaterial.Name` gives the material.

**Is it in the model?**

* Yes, these attributes are standard in IFC windows and are present in our Building #2516 model.

**Do you know how to get it in ifcOpenShell?**

* Yes. Using `model.by_type("IfcWindow")` we can iterate through wi

