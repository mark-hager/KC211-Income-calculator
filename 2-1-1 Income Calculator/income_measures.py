"""
Class containing methods for calculating the Area Median Income, the
Federal Poverty Level,and the State Median Income. These functions are based
on the direct calculations Hannah used in the Excel income calculator,
and thus aren't necessarily the best or most accurate ways of calculating them
in Python.
*TO DO* check AMI again't HUD's method.
"""
# math package used for rounding to follow Hannah's excel income calculations for AMI
import math

def excel_ceil(num):
    """
    Emulates excel's ceiling function to directly copy Hannah's formula
    """
    return 50 * math.ceil(float(num) / 50)

class IncomeMeasures:
    """
    Represents a household for the purposes of determining eligibility for various
    benefit programs. Includes fields for annual income and household size as well as
    a boolean reflecting whether or not the household includes minor children.
    Also has fields for client age and client dob for the purposes of estimating birth year
    and calculating the client's age, respectively.
    """
    def __init__(self, client):

        # initialized as None until we calculate the FPL, SMI and AMI via their
        # respective methods
        self.fpl = None
        self.smi = None
        self.ami = None

        self.calculate_fpl(client)
        self.calculate_smi(client)
        self.calculate_ami(client)


    def calculate_fpl(self, client):
        """
        Calculates the Federal Poverty Level based on HHS 2022 guidelines
        https://aspe.hhs.gov/topics/poverty-economic-mobility/poverty-guidelines
        """

        # FPL is calculated with a base rate times an additional rate per person
        fpl_base = 8870
        fpl_rate_per_person = 4720
        # calculate the FPL by dividing income by the base rate + household size
        # * the rate per person
        fpl = math.ceil(client.annual_income / ((client.household_size * fpl_rate_per_person)
                                        + fpl_base) * 100)
        # format as percentage
        fpl = "{}%".format(fpl)
        self.fpl = fpl  # assign the calculated Federal Poverty Level percentage to our object


    def calculate_smi(self, client):
        """
        Calculates the State Median Income based on DSHS 2022 guidelines
        https://www.dshs.wa.gov/esa/eligibility-z-manual-ea-z/state-median-income-chart
        """

        # SMI is calculated with separate base rates depending on household size
        # for families of 5 or less, and families of 6 or more
        smi_base_household_5_or_less = 38940
        smi_base_household_6_or_more = 142776
        # the rate for each person in a household of 5 or less
        smi_rate_household_5_or_less = 17304
        # the rate for each person in a household of 6 or more
        smi_rate_household_6_or_more = 3240

        # calculate the SMI depending on household size
        if client.household_size < 7:
            smi = client.annual_income / ((client.household_size * smi_rate_household_5_or_less)
                                + smi_base_household_5_or_less) * 100
        elif client.household_size > 6:
            smi = client.annual_income / (smi_base_household_6_or_more +
                                ((client.household_size - 6) * (smi_rate_household_6_or_more))) * 100
        # round the SMI up
        smi = math.ceil(smi)
        # format as percentage
        smi = "{}%".format(smi)
        self.smi = smi  # assign the calculated State Median Income percentage to our object




    def calculate_ami(self, client):
        """
        Calculates the Area Median Income based on HUD 2022 guidelines
        https://www.huduser.gov/portal/datasets/il/il2022/2022summary.odn
        Currently rounding final AMI percentage as Hannah appears to be doing; need to confirm that this is correct.
        Previously I was using floor to always round down which created discrepancy

        """
        # AMI is calculated from the median annual income for a family of 4
        ami_base_household_of_4 = 129400
        # 80% low-income limit for a family of 4; for more detail read https://www.huduser.gov/portal/datasets/il/il2022/2022ILCalc3080.odn
        ami_base_80_percent = 95300
        # theoretical median income for a household of 0
        ami_base_0 = 77640
        # 80% of the median income for a household of 0
        ami_base_0_80_percent = 57180
        # for calculations when the initial AMI is between 70% and 80%
        ami_base_between_70_and_80 = 113125
        # initialize to false
        check_80_percent = False

        # calculate initial percentage to determine if it falls above or below 70%
        if client.household_size < 5:
            initial_ami = client.annual_income / ((ami_base_0) + (client.household_size * (ami_base_household_of_4 * .10))) * 100
            ami_80_cap = ami_base_0_80_percent + ami_base_80_percent * (client.household_size * .10)       #80% CAP calculation in Hannah's excel calculator
        elif client.household_size > 4:
            initial_ami = client.annual_income / ((ami_base_household_of_4 * .08) * (client.household_size - 4) + ami_base_household_of_4) * 100
            ami_80_cap = ami_base_80_percent + (ami_base_80_percent * (client.household_size - 4) * .08)

        ami_80_cap = excel_ceil(ami_80_cap)
        # calculate Hannah's Base 100% (C8), a massaged 100% AMI number
        if client.household_size < 5:
            ami_massaged_100_percent = ami_base_0 + (ami_base_household_of_4 * 0.1 * client.household_size)
        elif client.household_size > 4:
            ami_massaged_100_percent = ami_base_household_of_4 + (ami_base_household_of_4 * 0.08 * (client.household_size - 4))


        # AMI adjustment for incomes that would normally fall between 70% and 80% of the AMI
        if initial_ami >= 71 and initial_ami <= 81:
            if client.household_size < 5:
                adjusted_ami = client.annual_income / (ami_base_between_70_and_80 + ((client.household_size - 4) * ami_base_between_70_and_80 * .10)) * 100
            else:
                adjusted_ami = client.annual_income / (ami_base_between_70_and_80 + ((client.household_size - 4) * ami_base_between_70_and_80 * .08)) * 100

        else:
            adjusted_ami = initial_ami

        # AMI adjustments for incomes that would fall under the 50% CAP
        cap_50 = ami_massaged_100_percent / 2
        cap_50 = 50 * round(cap_50 / 50)
        check_50_percent = False

        if client.annual_income > cap_50 and adjusted_ami < 51:
            check_50_percent = True

        # 80% CHECK:
        if client.annual_income > ami_80_cap and adjusted_ami < 81:
            check_80_percent = True

        ami = round(adjusted_ami)
        if check_50_percent is True:
            ami = 51
        if check_80_percent is True:
            ami = 81
        # format as percentage
        ami = "{}%".format(round(ami))
        self.ami = ami  # assign the calculated Area Median Income percentage to our object
