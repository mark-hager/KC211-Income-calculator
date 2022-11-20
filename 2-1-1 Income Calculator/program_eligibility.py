"""
Class containing methods for determining household eligibility 
for various state and federal benefits programs.
"""

class ProgramEligibility: 
    """
    Determines eligiblity for various benefits programs from an instance
    of NewHousehold to check program requirements against the FPL, SMI, AMI
    and household composition.
    """


    def __init__(self, household):

        self.household = household
        # default eligibility to all programs as false
        self.hsp = False
        self.apple_h = False
        self.wa_food = False
        self.liheap = False

        # programs that can be screened w/out rent
        self.apple_health_eligibility()
        self.basic_food_eligibility()
        self.liheap_eligibility()
        # check for eligibility only if rent_amount is not empty
        if hasattr(self.household, 'monthly_rent'):
            self.hsp_eligibility()

        # initialize empty list to hold programs client may be eligible for
        self.programs = []
        if self.wa_food is True:
            self.programs.append("Washington Basic Food Program")
        if self.apple_h is True:
            self.programs.append("Apple Health")
        if self.hsp is True:
            self.programs.append("Housing Stability Project")
        if self.liheap is True:
            self.programs.append("Low Income Home Energy Assistance Program (LIHEAP)")


    def hsp_eligibility(self):
        """
        Determines eligibility for Housing Stability Project:
        Area Median Income must be less than or equal to 50% and
        rent to income ratio must be less than or equal to 1:1.5
        """

        if self.household.ami > 0.5:
            print("Income too high for HSP: AMI was above 0.5")
            self.hsp = False
        if ((self.household.annual_income / 12) / 
            self.household.monthly_rent) < 1.5:
            print("Income to rent ratio was too low; must be at least 1.5:1")
            self.hsp = False
        else:
            self.hsp = True


    def apple_health_eligibility(self):
        """
        Determines eligibility for Apple Health insurance:
        FPL must be at or below 138% of the Federal Poverty Level.
        Info for 2022:
        https://www.hca.wa.gov/assets/free-or-low-cost/22-315.pdf
        """

        if self.household.fpl > 1.38:
            print("Income too high for Apple Health: FPL was above 1.38")
            self.apple_h = False
        else:
            self.apple_h = True

    def basic_food_eligibility(self):
        """
        Determines eligibility for Washington's Basic Food Program:
        FPL must be at or below 200% of the Federal Poverty Level.
        Info for 2022:
        https://kingcounty.gov/depts/health/locations/health-insurance/access-and-outreach/basic-food-program.aspx
        """

        if self.household.fpl > 2:
            print("Income too high for WA Basic Food: FPL was above 2")
            self.wa_food = False
        else:
            self.wa_food = True
    
    def liheap_eligibility(self):
        """
        Determines eligibility for the Low Income Home Energy Assistance
        Program (LIHEAP):
        FPL must be at or below 150% of the Federal Poverty Level.
        Info for 2022:
        https://www.benefits.gov/benefit/623
        """
        
        if self.household.fpl > 1.5:
            print("Income too high for LIHEAP: FPL was above 1.5")
            self.liheap = False
        else:
            self.liheap = True
    
