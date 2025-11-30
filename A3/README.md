# Assignment A3 – Cost Estimation Validation Tool

## Summary
**Title:** IFC architectural cost estimator tool
**Category:** Build / Cost / Buildability / Permits  
**Description (20–40 words):** 


---

## 01 Your tool - A Python script


---

## 03 A markdown file:
### State the problem / claim that your tool is solving.
Cost estimation and budgeting for building projects are a central part of the process; ensuring fast and adaptable tools for estimating cost could have a huge impact. Making sure to have the correct quantities of both models (Arkitekt) and cost estimation from advisers aligns is a huge advantage. By creating a tool where ICF elements can be detected and given value depending on the chosen product.  
By creating a tool that can not only validate the claimed cost estimation but also create its own cost estimation based on quantities from the IFC models, more accurate cost estimations can be made, resulting in better decision-making and budgeting.

### State where you found that problem.
The issue appears when working with IFC files/models for cost estimation. It is often difficult to load the file correctly, extract the right quantities, or rely on correct and thorough use of classification systems. As a result, quantities must often be checked manually, and this is a very time-consuming task.

### Description of the tool
The tool consists of two Python scripts:
- main.py – handles the menu, terminal interaction, and catalog for price and default area
- utils.py – contains all functions for reading the IFC, classifying elements, calculating areas, and estimating costs  

The tool requires access to the IFC file on the computer running it (copy the file path).

### Instructions to run the tool
To run the tool, you need to have IFCOpenShell and Python installed. Make sure both main.py and utils.py are downloaded and placed in the same folder. 

In main.py, you can adjust two things before you start:
- prices: price DKK per m² for each element type  
- default_areas: fallback areas for each element type  in m²
Both can also be changed later in the terminal using the menu options.

When starting to run the script, the first thing it will ask is to enter the file path for the chosen IFC model.
If it loads, it will state IFC model loaded successfully, and an options menu will pop up. If not, you get an error.

The menu has the following options:

<img width="1244" height="342" alt="image" src="https://github.com/user-attachments/assets/f6b6770d-9f8f-45a5-802a-fc0951a918c6" /> 

1) **Show element count** -  Counts each architectural element type. Internal/external walls are automatically separated based on IFC properties and naming. Walls marked as load-bearing in the IFC are ignored for this tool.

2) **Show element areas** - extract, calculate, or approximate area. This takes longer because the tool tries several methods to determine the area:

The script processes the model and calculates areas in the following order:

1. IfcQuantityArea
2. Height × width (for windows/doors)  
3. Geometric projection using IfcOpenShell  
4. Default fallback area (user-defined)  

If an element had to be approximated or defaulted, the script lists both the element type and the amount:
<img width="1229" height="355" alt="image" src="https://github.com/user-attachments/assets/8d1588b6-4790-4ca0-b34c-e0bb3d074d93" />
If many elements use default areas, it is a good idea to update the values in default_areas in main.py to ensure correct data.


3) **Estimate cost** - The tool multiplies every element’s area by its price from the price catalog. The script then prints the total estimated cost in DKK.
Therefore also important to make sure to update the price catalog to the prices used in the specific project. This is done in main.py under prices, see the picture below.
<img width="1077" height="289" alt="image" src="https://github.com/user-attachments/assets/b52a49c5-14ed-4a43-bfa0-9236908821c2" />

5) **Change element price** - for changing the price while running the script, instead os using the price catalog at the beginning of the script, the prices can be updated directly in the terminal. Also Useful if you want to compare different material choices or suppliers.

6) **Change element default area** - For cases where geometry is missing, each element type has a fallback area. If you know your project uses larger roofs or curtain walls, adjust them here. 

7) **Show cost pie chart** - Opens a pie chart showing each element type’s share of total cost.
This gives a quick overview of which elements in the ARCH require more budget.

9) **Quit** - Ends the script.

## Advanced Building Design
### What Advanced Building Design Stage (A,B,C, or D) would your tool be useful?
The tool works better the more information there is in the IFC model, meaning it can be used for estimations right from when the IFC model has been made, but the results are only useful after more data is given.
The showing of element areas and checking the information in the IFC file can be useful in earlier stages, maybe early C, while the cost estimation needs the dimensions and materials to get a relevant result.

Therefore, we would recommend trying out the tool in phase C for an overview and early estimate, checking the area information on the elements.
For the cost estimation, it becomes more reliable in the D phase, during the process of finalizing the BIM, as well as the final IFC, for the most accurate data.

### Which subjects might use it?
This would mainly be the project manager, while the tool is for cost estimation. It could also be useful for checking the ICT classifications, and if more area information is necessary, to get a more efficient calculation.
It could also be relevant to materials for the LCI extraction of amounts and volumes from the Arch IFC. 

### What information is required in the model for your tool to work?
For the tool to work, the IFC model needs to contain architectural elements. The script looks for windows, doors, walls, slabs, ceilings, roofs, and curtain walls. 
Use option 2 to check elements, and see if it matches your expected amount. 
The tool works best when the model includes quantity data like IfcQuantityArea or simpler parameters like height and width for windows and doors. If these are missing, the geometry must be detailed enough for IfcOpenShell to calculate projected areas. IF none of this is available, the tool falls back on default areas, so it can still run, but the areas have to be calculated or found manually.


---

## 04 — IDS: Model Readiness Check
The IDS file tests whether the IFC model contains area quantities for the architectural elements needed by the our tool. It checks IfcQuantityArea on windows, doors, walls, slabs, ceilings, roofs and curtain walls. If the model includes these, the cost output is more accurate; if not, the tool switches to geometry or default areas.

