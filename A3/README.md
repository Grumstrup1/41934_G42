# Assignment A3 – Cost Estimation Validation Tool

## Summary
**Title:** Cost Estimation Validation Tool for ARCH IFC  
**Category:** Build / Cost / Buildability / Permits  
**Description (20–40 words):**  

---

## 01 Your tool - A Python script


---

## 03 A markdown file:
State the problem / claim that your tool is solving.

State where you found that problem.

Description of the tool

Instructions to run the tool.

---

## 04 — IDS: Model Readiness Check

We implemented a simple IDS to determine whether an IFC model contains the quantity properties our cost tool requires. The IDS validates whether elements such as windows, doors, walls, slabs, ceilings, roofs, and curtain walls include their expected BaseQuantities (e.g., `Area`, `NetSideArea`).

The IDS is implemented in **`A3/ids_arch_for_cost.py`** using the `ifctester` API.  
It generates the IDS programmatically, validates any IFC file, and reports:

- A **compatibility status** for our tool  
  (“Fully supported”, “Partially supported”, or “Supported with fallback”)
- A **data completeness score** (%)  
- PASS/FAIL checks for required quantity properties

This shows whether the IFC model contains the information needed for reliable cost estimation or whether our tool must fall back to geometry-based calculations.
