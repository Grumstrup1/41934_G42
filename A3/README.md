# Assignment A3 – Cost Estimation Validation Tool

## Summary
**Title:** IFC architectural cost estimator tool
**Category:** Build / Cost / Buildability / Permits  
**Description (20–40 words):**  

---

## 01 Your tool - A Python script


---

## 03 A markdown file:
**State the problem / claim that your tool is solving.**

Cost estimation and budgeting for building projects are a central part of the process; ensuring fast and adaptable tools for estimating cost could have a huge impact. Making sure to have the correct quantities of both models (Arkitekt) and cost estimation from advisers aligns is a huge advantage. By creating a tool where ICF elements can be detected and given value depending on the chosen product.  
By creating a tool that can not only validate the claimed cost estimation but also create its own cost estimation based on quantities from the IFC models, more accurate cost estimations can be made, resulting in better decision-making and budgeting.

**State where you found that problem.**
The problem is found while working with cost estimation, where it is hard to either load in the file correctly and having to check everything through, making sure to use the right quantities or having to count, because things aren't named specifically enough to do it automatically. 

**Description of the tool**
The tool is a standalone Python tool, which consists of two Python scripts, a utility, and a main. The code runs through an IFC-file to check and extract the relevant data. The tool requires that the applicable IFC file be available on the computer running the tool, knowing the file path.

The main script gives the outputs 
Price catalog change the prices 

**Instructions to run the tool.**
To run the tool, you need to download IFCOpenShell and Python. Make sure you have both Python files, and now you can run the main script. 

Everything will be in the terminal, the first thing it will ask is to enter the file path for the chosen IFC model
If it loads, it will state IFC model loaded successfully, and an options menu will pop up. If not, you get an error.

The menu has the following options

<img width="1244" height="342" alt="image" src="https://github.com/user-attachments/assets/f6b6770d-9f8f-45a5-802a-fc0951a918c6" /> 

1) Show element count -  Counts each architectural element type. Internal/external walls are automatically separated based on IFC properties and naming.

2) Show element areas - extract, calculate, or approximate area. This takes longer because the tool tries several methods to determine the area:
   IfcQuantityArea
   Height × width (for windows/doors)
   Geometric projection (IfcOpenShell geom)
   Fallback defaults from the script
If an element had to be approximated or defaulted, the script lists both the element type and the amount:
<img width="1215" height="510" alt="image" src="https://github.com/user-attachments/assets/acc1965f-5acb-4156-8b13-9a8e6007eeb6" />
Here, it is smart to update all defaulted areas in the default area in the main script to ensure correct information. 

3) Estimate cost - The tool multiplies every element’s area by its price from the price catalog.
   Therefore also important to make sure to update the price catalog to the prices used in the specific project. This is done in the main.py under prices, or see       the picture below.
<img width="1077" height="289" alt="image" src="https://github.com/user-attachments/assets/b52a49c5-14ed-4a43-bfa0-9236908821c2" />

4) Change element price - for changing the price while running the script, instead os using the price catalog at the beginning of the script, the prices can be updated directly in the terminal. Also Useful if you want to compare different material choices or suppliers.

5) Change element default area - For cases where geometry is missing, each element type has a fallback area. If you know your project uses larger roofs or curtain walls, adjust them here. 

6) Show cost pie chart - Opens a pie chart showing each element type’s share of total cost.
This gives a quick overview of which elements in the ARCH require more budget.

9) Quit - Ends the script.

---

## 04 — IDS: Model Readiness Check

We implemented a simple IDS to determine whether an IFC model contains the quantity properties our cost tool requires. The IDS validates whether elements such as windows, doors, walls, slabs, ceilings, roofs, and curtain walls include their expected BaseQuantities (e.g., `Area`, `NetSideArea`).

The IDS is implemented in **[`ids_arch_for_cost.py`](ids_arch_for_cost.py)**  using the `ifctester` API.  
It generates the IDS programmatically, validates any IFC file, and reports:

- A **compatibility status** for our tool  
  (“Fully supported”, “Partially supported”, or “Supported with fallback”)
- A **data completeness score** (%)  
- PASS/FAIL checks for required quantity properties

This shows whether the IFC model contains the information needed for reliable cost estimation or whether our tool must fall back to geometry-based calculations.
