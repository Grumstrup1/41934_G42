# Assignment A3 – Rapid IFC-Based Architectural Cost Estimator

---

## State the problem/claim that your tool is solving.
Cost estimation is a time-consuming task, especially when IFC models have to be loaded into programs like Sigma, where setup, formatting issues, and error diagnosis take up a lot of time. This makes it difficult to get a fast overview of the cost of the project.
Our Rapid IFC-Based Architectural Cost Estimator removes most of that setup and error handling. It reads the IFC directly and gives a quick overview of the architectural quantities and cost. Also, good data to compare results with the traditional cost estimation.

## **State where you found that problem**
The problem comes from working as a project manager in earlier projects, where we handled cost estimation. Loading IFC files into Sigma was difficult, and getting the right quantities depended on correct classification and clean data. Because of this, quantities often had to be checked manually, which is a very time-consuming task.

## Description of the tool
The tool consists of two Python scripts:

- **[main.py](A3/main.py)** - handles the menu, terminal interaction, and the catalog for prices and default areas  
- **[utils.py](A3/utils.py)** - contains all functions for reading the IFC, classifying elements, calculating areas, and estimating costs  

The tool requires access to the IFC file on the computer running it (paste the full file path when the script asks for it).

## Instructions to run the tool
To run the tool, you need IFCOpenShell and Python installed. Download [main.py](A3/main.py) and [utils.py](A3/utils.py) and place them in the same folder. 
For a video tutorial, follow the link [her](https://youtu.be/iAVOLkmRwe0)

In [main.py](A3/main.py), you can adjust two things before you start:

- **prices**: price in DKK per m² for each element type  
- **default_areas**: fallback areas in m² for each element type  

Both can also be changed later in the terminal through the menu.

When starting the script, the first thing it asks for is the file path to the IFC model. If the file loads, it prints “IFC model loaded successfully” and shows the menu. If not, it prints an error.

**The menu has the following options:**

<img width="1244" height="342" alt="image" src="https://github.com/user-attachments/assets/f6b6770d-9f8f-45a5-802a-fc0951a918c6" /> 

1) **Show element count** -  Counts each architectural element type. Internal/external walls are separated automatically based on IFC properties and naming. Load-bearing walls are ignored.

2) **Show element areas** - Extracts, calculates, or approximates the area of each element type.  
This takes longer because the tool tries several methods in this order:

1. IfcQuantityArea
2. Height × width (for windows/doors)  
3. Geometric projection using IfcOpenShell  
4. Default fallback area (user-defined)  

If an element had to be approximated or defaulted, the script lists how many of each type (example of output below):
<img width="1229" height="355" alt="image" src="https://github.com/user-attachments/assets/8d1588b6-4790-4ca0-b34c-e0bb3d074d93" />
If many elements use default areas, it is recommended to update the values in default_areas in main.py.

3) **Estimate cost** - Multiplies every element’s area by its price from the price catalog and prints the total estimated cost in DKK. It is important to update the prices to match the specific project. Prices are defined in main.py under prices (see picture below).
<img width="1077" height="289" alt="image" src="https://github.com/user-attachments/assets/b52a49c5-14ed-4a43-bfa0-9236908821c2" />

5) **Change element price** - Updates the price for an element type while the script is running. Useful for comparing different materials or supplier prices without editing the script.

6) **Change element default area** - Updates the fallback areas used when the IFC does not provide geometry or quantity data. It can also be updated in the script main.py under default_areas (see picture below).
<img width="1188" height="256" alt="image" src="https://github.com/user-attachments/assets/bfe482d6-b8af-4bbc-a7fd-841204c77d61" />


7) **Show cost pie chart** - Opens a pie chart showing each element type’s share of the total cost. Gives a quick overview of which architectural elements drive the budget.

8) **Quit** - Ends the script.

## Advanced Building Design
### What Advanced Building Design Stage (A,B,C, or D) would your tool be useful?
The tool works better the more information there is in the IFC model. It can be used early for rough estimations, but the results become meaningful once dimensions and materials are known. Showing element areas and checking the IFC data can already be useful in the early phase C. For cost estimation, the tool is most reliable in phase D, when the IFC is more complete, and the data is stable.

### Which subjects might use it?
This would mainly be the project manager, since they are responsible for the cost estimation. The tool can also be useful for checking ICT classifications and seeing if more area information is needed for a more efficient calculation.  
It can also support material, for example, extracting LCI quantities and volumes from the architectural IFC.

### What information is required in the model for your tool to work?
The tool requires the IFC model to contain basic architectural elements such as windows, doors, walls, slabs, ceilings, roofs, and curtain walls. Use menu option 2 to check whether the element counts match your expectations.  
The tool works best when the model includes IfcQuantityArea or simple dimensions such as height and width. If these are missing, the IFC must have enough geometry for IfcOpenShell to calculate projected areas. If none of this is available, the tool falls back on default areas, so the script will still run, but the areas must then be verified manually.

---

## 04 — IDS: Model Readiness Check
The IDS file tests whether the IFC model contains area quantities for the architectural elements needed by our tool. It checks IfcQuantityArea on windows, doors, walls, slabs, ceilings, roofs, and curtain walls. If the model includes these, the cost output is more accurate; if not, the tool switches to geometry or default areas.






