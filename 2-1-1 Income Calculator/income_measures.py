"""
Contains methods for calculating the Area Median Income, the
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


def calculate_fpl(client):
    """
    Calculates the Federal Poverty Level based on HHS 2023 guidelines
    https://aspe.hhs.gov/topics/poverty-economic-mobility/poverty-guidelines
    """

    # FPL is calculated with a base rate times an additional rate per person
    fpl_base = 9440
    fpl_rate_per_person = 5140
    # calculate the FPL by dividing income by the base rate + household size
    # * the rate per person
    fpl = math.ceil(client.annual_income / ((client.household_size * fpl_rate_per_person)
                                    + fpl_base) * 100)

    # convert from percentage back to decimal for program eligibility and formatting
    fpl = fpl / 100
   
    return fpl  # return the calculated Federal Poverty Level percentage to our client object


def calculate_smi(client):
    """
    Calculates the State Median Income based on DSHS 2023 guidelines
    https://www.dshs.wa.gov/esa/eligibility-z-manual-ea-z/state-median-income-chart
    """

    # SMI is calculated with separate base rates depending on household size
    # for families of 5 or less, and families of 6 or more
    smi_base_household_5_or_less = 40824
    smi_base_household_6_or_more = 149736
    # the rate for each person in a household of 5 or less
    smi_rate_household_5_or_less = 18156
    # the rate for each person in a household of 6 or more
    smi_rate_household_6_or_more = 3408

    # calculate the SMI depending on household size, 
    # rounded to 4 decimal places to match the excel calculator; can't
    # find documentation on how other people calculate this
    if client.household_size < 7:
        smi = round(client.annual_income / ((client.household_size * smi_rate_household_5_or_less)
                            + smi_base_household_5_or_less), 4) * 100
    elif client.household_size > 6:
        smi = round(client.annual_income / (smi_base_household_6_or_more +
                            ((client.household_size - 6) * (smi_rate_household_6_or_more))), 4) * 100
    # round the SMI up
    smi = math.ceil(smi)
    # convert from percentage back to decimal for program eligibility and formatting
    smi = smi / 100

    return smi  # return the calculated State Median Income to our client object




def calculate_ami(client):
    """
    Calculates the Area Median Income based on HUD 2023 guidelines
    https://www.huduser.gov/portal/datasets/il/il2023/2023summary.odn?states=%24states%24&data=2023&inputname=METRO42660MM7600*Seattle-Bellevue%2C+WA+HUD+Metro+FMR+Area&stname=%24stname%24&statefp=99&year=2023&selection_type=hmfa
    Uses artificial "caps" rounded to the nearest 50 for each of the income limits: 30%, 50% and 80% of the AMI as defined by HUD.
    Should refactor code to make variable names and calculations clearer.

    """
    # AMI is calculated from the median annual income for a family of 4
    ami_base_household_of_4 = 137000
    # 80% low-income limit for a family of 4; for more detail read https://www.huduser.gov/portal/datasets/il/il2022/2022ILCalc3080.odn
    ami_base_80_percent = 100900
    # theoretical median income for a household of 0
    ami_base_0 = 82200
    # 80% of the median income for a household of 0
    ami_base_0_80_percent = 60540
    # for calculations when the initial AMI is between 70% and 80%
    ami_base_between_70_and_80 = (ami_base_80_percent * 1.25)
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
        
    # AMI adjustments for incomes that would fall under the 30% CAP
    cap_30 = ami_massaged_100_percent * 0.3
    cap_30 = 50 * round(cap_30 / 50)
    check_30_percent = False
    
    if client.annual_income > cap_30 and adjusted_ami < 31:
        check_30_percent = True
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
    
    # check that any value over defined income limit is rounded up 
    if check_30_percent is True:
        ami = 31
    elif check_50_percent is True:
        ami = 51
    elif check_80_percent is True:
        ami = 81
        
    # convert from percentage back to decimal for program eligibility and formatting
    ami = ami / 100

    return ami  # return the calculated Area Median Income percentage to our client object
