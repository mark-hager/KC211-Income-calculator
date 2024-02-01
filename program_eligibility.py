"""
Functions for determining household eligibility 
for various state and federal benefits programs.
"""

class CheckProgramEligibility:
    """
    Determines which programs a household may be eligible for based on
    household size, composition, and gross income.
    """
    # is passed client object containing demographics and info needed
    # to determine eligibility
    def __init__(self, client):
        self.client = client
        # init empty list to hold programs client may be eligible for
        self.referrals = []

        # only check HSP eligibility if monthly rent entered
        if hasattr(self.client, 'monthly_rent') and self.client.monthly_rent > 0:
            self.hsp_eligibility()
        # check eligibility for remaining programs        
        self.apple_health_eligibility()
        self.basic_food_eligibility()
        self.liheap_eligibility()
        self.pse_help_eligibility()
        self.elia_eligibility()

    def hsp_eligibility(self):
        """
        Determines eligibility for Housing Stability Project:
        Area Median Income must be less than or equal to 50% and
        rent to income ratio must be less than or equal to 1:1.5
        """

        if self.client.ami > 0.5:
            print("Income too high for HSP: AMI was above 0.5")
            return False
        if ((self.client.annual_income / 12) /
            self.client.monthly_rent) < 1.5:
            print("Income to rent ratio was too low; must be at least 1.5:1")
            return False

        # else household is possibly eligible
        self.referrals.append("Housing Stability Project")
        return True


    def apple_health_eligibility(self):
        """
        Determines eligibility for Apple Health insurance:
        Income must be at or below 138% of the Federal Poverty Level.
        Info for 2022:
        https://www.hca.wa.gov/assets/free-or-low-cost/22-315.pdf
        """

        if self.client.fpl > 1.38:
            print("Income too high for Apple Health: FPL was above 1.38")
            return False
        self.referrals.append("Housing Stability Project")
        return True

    def basic_food_eligibility(self):
        """
        Determines eligibility for Washington's Basic Food Program:
        Income must be at or below 200% of the Federal Poverty Level.
        Info for 2022:
        https://kingcounty.gov/depts/health/locations/health-insurance/access-and-outreach/basic-food-program.aspx
        """

        if self.client.fpl > 2:
            print("Income too high for WA Basic Food: FPL was above 2")
            return False

        self.referrals.append("Washington Basic Food Program")
        return True

    def liheap_eligibility(self):
        """
        Determines eligibility for the Low Income Home Energy Assistance
        Program (LIHEAP):
        Income must be at or below 150% of the Federal Poverty Level.
        Info for 2022:
        https://www.benefits.gov/benefit/623
        """

        if self.client.fpl > 1.5:
            print("Income too high for LIHEAP: FPL was above 1.5")
            return False

        self.referrals.append("Low Income Home Energy Assistance Program (LIHEAP)")
        return True

    def pse_help_eligibility(self):
        """
        Determines eligibility for PSE HELP:
        Income must be at or below 80% of the Area Median Income.
        Info for 2022:
        https://www.pse.com/account-and-billing/assistance-programs/Income-Guidelines
        """

        if self.client.ami > 0.8:
            print("Income too high for PSE HELP: AMI was above 0.8")
            return False

        self.referrals.append("PSE HELP - PSE Customers Only")
        return True

    def elia_eligibility(self):
        """
        Determines eligibility for SCL ELIA (Emergency Low-Income Assistance Program):
        Income must be at or below 70% of the State Median Income.
        Info for 2022:
        https://www.seattle.gov/city-light/residential-services/billing-information/bill-assistance-programs#longterm
        """

        if self.client.smi > 0.7:
            print("Income too high for ELIA: SMI was above 0.7")
            return False

        self.referrals.append("Emergency Low Income Assistance (ELIA) - SCL Customers Only")
        return True
