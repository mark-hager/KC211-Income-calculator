# 211-Income-calculator

Flask app used by King County 211 to estimate household eligibility for commonly referred state and local assistance programs.

## Description

Estimates household eligibility for assistance programs like Apple Health (Washington State medicaid), Basic Food/SNAP, LIHEAP and more by
comparing common measures of median income against the gross monthly or annual income and household size to generate a percentage.

These income measurements include the Federal Poverty Level ([FPL](https://www.healthcare.gov/glossary/federal-poverty-level-fpl/)), the State Median Income ([SMI](https://www.dshs.wa.gov/esa/eligibility-z-manual-ea-z/state-median-income-chart)), and the Area Median Income ([AMI](https://www.huduser.gov/Portal/datasets/il.html)).

The State Median Income and Area Median Income limits used by this calculator reflect the current (as of December, 2023) values for King County, WA and can be found in income_measures.py.

State, local and federal assistance programs often require that applicants fall below a certain percentage of the median income. Federal programs use limits based on the federal poverty level. This includes expanded Medicaid, [where household income must be below 138% of the federal poverty level](https://www.healthcare.gov/medicaid-chip/medicaid-expansion-and-you/), and the Low Income Home Energy Assistance Program [(LIHEAP) which has a cap of 150% of the FPL](https://liheapch.acf.hhs.gov/tables/POP.htm).

Similarly, programs administered at the state level may have requirements based on that state's median income, and median income at the area/county level may also be used for determining program eligibility in metro areas with higher average incomes (and cost of living). 

All estimates are preliminary and require that the KC211 specialist screen each household for additional criteria before completing referral 


## Additional features

Calculates a client's age from their DOB to assess for program eligibility where age is a requirement. Also contains optional fields for indicating whether a household
has minor children as well as inputting the monthly rent. Some programs may require a particular income-to-rent ratio e.g. rental or deposit assistance.

### Dependencies
* Python 3
* Flask 3
* Flask-WTF [integrates WTForms with Flask. Used here for field validation.](https://flask-wtf.readthedocs.io/)

### Credits

Thank you, Hannah Newton at CrCon/KC211 for building the Excel income calculator this project is based off of and for teaching me how the heck to calculate AMI percentages. You truly are a wizard and I am so glad to have had you as my mentor :mage_woman:.