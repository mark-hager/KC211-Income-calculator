"""
Class containing methods for determining household eligibility for various benefits programs.
"""

class ProgramEligibility: 
    """
    Determines eligiblity for various benefits programs from an instance
    of NewHousehold to check program requirements against the FPL, SMI, AMI
    and household composition of the household.
    """
    eligibile_for_hsp = False
    def __init__(self, household):
        self.household = household

    def hsp_eligibility(self):
        """
        Determines eligibility for Housing Stability Project:
        Area Median Income must be less than or equal to 50% and
        rent to income ratio must be less than or equal to 1:1.5
        """
        if self.household.rent_amount is None:
            print("Please enter a rental amount to determine HSP eligibility")
            return
        if self.household.household.ami > 0.5:
            print("Income too high: AMI was above 0.5")
            self.eligibile_for_hsp = False
        if ((self.household.income / 12) / self.household.rent) < 1.5:
            print("Income to rent ratio was too low; must be at least 1.5:1")
            self.eligibile_for_hsp = False
        return
