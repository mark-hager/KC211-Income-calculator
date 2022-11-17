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

        # programs that can be screened w/out rent
        self.eligible_for_applehealth()
        # check for eligibility only if rent_amount is not empty
        if hasattr(self.household, 'monthly_rent'):
            self.hsp_eligibile = self.eligible_for_hsp()

        # initialize empty list to hold programs client may be eligible for
        self.programs = []
        if self.hsp is True:
            self.programs.append("Housing Stability Project")
        if self.apple_h is True:
            self.programs.append("Apple Health")


    def eligible_for_hsp(self):
        """
        Determines eligibility for Housing Stability Project:
        Area Median Income must be less than or equal to 50% and
        rent to income ratio must be less than or equal to 1:1.5
        """

        if self.household.ami > 0.5:
            print("Income too high: AMI was above 0.5")
            self.hsp = False
        if ((self.household.annual_income / 12) / 
            self.household.monthly_rent) < 1.5:
            print("Income to rent ratio was too low; must be at least 1.5:1")
            self.hsp = False
        else:
            self.hsp = True


    def eligible_for_applehealth(self):
        """
        Determines eligibility for Apple Health insurance:
        FPL must be at or below 138% of the Federal Poverty Level.
        Info for 2022:
        https://www.hca.wa.gov/assets/free-or-low-cost/22-315.pdf
        """

        if self.household.fpl > 1.38:
            print("Income too high: FPL was above 1.38")
            self.apple_h = False
        else:
            self.apple_h = True
