"""
Functions for determining household eligibility 
for various state and federal benefits programs.
"""


def hsp_eligibility(self):
    """
    Determines eligibility for Housing Stability Project:
    Area Median Income must be less than or equal to 50% and
    rent to income ratio must be less than or equal to 1:1.5
    """

    if self.ami > 0.5:
        print("Income too high for HSP: AMI was above 0.5")
        return False
    if ((self.annual_income / 12) / 
        self.monthly_rent) < 1.5:
        print("Income to rent ratio was too low; must be at least 1.5:1")
        return False
    else:
        return True


def apple_health_eligibility(self):
    """
    Determines eligibility for Apple Health insurance:
    Income must be at or below 138% of the Federal Poverty Level.
    Info for 2022:
    https://www.hca.wa.gov/assets/free-or-low-cost/22-315.pdf
    """

    if self.fpl > 1.38:
        print("Income too high for Apple Health: FPL was above 1.38")
        return False
    else:
        return True

def basic_food_eligibility(self):
    """
    Determines eligibility for Washington's Basic Food Program:
    Income must be at or below 200% of the Federal Poverty Level.
    Info for 2022:
    https://kingcounty.gov/depts/health/locations/health-insurance/access-and-outreach/basic-food-program.aspx
    """

    if self.fpl > 2:
        print("Income too high for WA Basic Food: FPL was above 2")
        return False
    else:
        return True

def liheap_eligibility(self):
    """
    Determines eligibility for the Low Income Home Energy Assistance
    Program (LIHEAP):
    Income must be at or below 150% of the Federal Poverty Level.
    Info for 2022:
    https://www.benefits.gov/benefit/623
    """
    
    if self.fpl > 1.5:
        print("Income too high for LIHEAP: FPL was above 1.5")
        return False
    else:
        return True

def pse_help_eligibility(self):
    """
    Determines eligibility for PSE HELP:
    Income must be at or below 80% of the Area Median Income
    """
    
    if self.ami > .8:
        print("Income too high for PSE HELP: AMI was above 0.8")
        return False
    else:
        return True