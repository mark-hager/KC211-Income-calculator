"""
Class containing methods for determining household eligibility for various benefits programs.
"""

class ProgramEligibility: 
    """
    Determines eligiblity for various benefits programs from an instance
    of NewHousehold to check program requirements against the FPL, SMI, AMI
    and household composition.
    """
    eligibile_for_hsp = False
    def __init__(self, household):

        self.household = household
        
        # default eligibility to all programs as false
        self.hsp = False

        # check for eligibility only if rent_amount is not empty
        if hasattr(self.household, 'monthly_rent'):
            self.hsp_eligibile = self.eligible_for_hsp()

    def eligible_for_hsp(self):
        """
        Determines eligibility for Housing Stability Project:
        Area Median Income must be less than or equal to 50% and
        rent to income ratio must be less than or equal to 1:1.5
        """

        if self.household.ami > 0.5:
            print("Income too high: AMI was above 0.5")
            self.hsp = False
        if ((self.household.annual_income / 12) / self.household.monthly_rent) < 1.5:
            print("Income to rent ratio was too low; must be at least 1.5:1")
            self.hsp = False
        else:
            self.hsp = True
