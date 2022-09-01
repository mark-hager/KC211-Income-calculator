# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 13:31:56 2021

@author: mhager

Python implementation of Hannah Newton's Excel-based income calculator for
use by King County 2-1-1 specialists.

Used https://github.com/nanoproductions/flask_calculator_basic for help with flask
"""
# used for formatting user inputs by stripping dollar signs and commas
import re
# math package used for rounding
import math
# import Flask
from flask import Flask, flash, render_template, request
# create Flask object
app = Flask(__name__)
# set the secret key which is required for flash
app.secret_key = 'FD7syfsjh4Slj4w0'
# start an app route which is '/'
@app.route('/')
# declare the main function
def main():
    return render_template('app.html')


class new_household:
    def __init__(self, annual_income, household_size):
        self.annual_income = annual_income
        self.household_size = household_size
        self.fpl = None  # FPL, SMI and AMI are calculated by their respective methods
        self.smi = None
        self.ami = None

    def calculate_fpl(self):
        """
        Calculates the Federal Poverty Level based on HHS 2022 guidelines
        https://aspe.hhs.gov/topics/poverty-economic-mobility/poverty-guidelines
        """

        # FPL is calculated with a base rate times an additional rate per person
        fpl_base = 8870
        fpl_rate_per_person = 4720
        # calculate the FPL by dividing income by the base rate + household size
        # * the rate per person
        fpl = math.ceil(self.annual_income / ((self.household_size * fpl_rate_per_person)
                                        + fpl_base) * 100)
        # format as percentage
        fpl = "{}%".format(fpl)
        self.fpl = fpl  # assign the calculated Federal Poverty Level percentage to our object


    def calculate_smi(self):
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
        if self.household_size < 7:
            smi = self.annual_income / ((self.household_size * smi_rate_household_5_or_less)
                                + smi_base_household_5_or_less) * 100
        elif self.household_size > 6:
            smi = self.annual_income / (smi_base_household_6_or_more +
                                ((self.household_size - 6) * (smi_rate_household_6_or_more))) * 100
        # round the SMI up
        smi = math.ceil(smi)
        # format as percentage
        smi = "{}%".format(smi)
        self.smi = smi  # assign the calculated State Median Income percentage to our object


    def excel_ceil(num):  # emulating excel's ceiling function to directly copy Hannah's formula
        return 50 * math.ceil(float(num) / 50)

def calculate_ami(annual_income, household_size):
    """
    Calculates the Area Median Income based on HUD 2022 guidelines
    https://www.huduser.gov/portal/datasets/il/il2022/2022summary.odn

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
    if household_size < 5:
        initial_ami = annual_income / ((ami_base_0) + (household_size * (ami_base_household_of_4 * .10))) * 100
        ami_80_cap = ami_base_0_80_percent + ami_base_80_percent * (household_size * .10)       #80% CAP calculation in Hannah's excel calculator
    elif household_size > 4:
        initial_ami = annual_income / ((ami_base_household_of_4 * .08) * (household_size - 4) + ami_base_household_of_4) * 100
        ami_80_cap = ami_base_80_percent + (ami_base_80_percent * (household_size - 4) * .08)

    ami_80_cap = excel_ceil(ami_80_cap)
    # calculate Hannah's Base 100% (C8), a massaged 100% AMI number
    if household_size < 5:
        ami_massaged_100_percent = ami_base_0 + (ami_base_household_of_4 * 0.1 * household_size)
    elif household_size > 4:
        ami_massaged_100_percent = ami_base_household_of_4 + (ami_base_household_of_4 * 0.08 * (household_size - 4))


    # AMI adjustment for incomes that would normally fall between 70% and 80% of the AMI
    if initial_ami >= 71 and initial_ami <= 81:
        if household_size < 5:
            adjusted_ami = annual_income / (ami_base_between_70_and_80 + ((household_size - 4) * ami_base_between_70_and_80 * .10)) * 100
        else:
            adjusted_ami = annual_income / (ami_base_between_70_and_80 + ((household_size - 4) * ami_base_between_70_and_80 * .08)) * 100

    else:
        adjusted_ami = initial_ami

    # AMI adjustments for incomes that would fall under the 50% CAP
    cap_50 = ami_massaged_100_percent / 2
    cap_50 = 50 * round(cap_50 / 50)
    check_50_percent = False

    if annual_income > cap_50 and adjusted_ami < 51:
        check_50_percent = True

    # 80% CHECK:
    if annual_income > ami_80_cap and adjusted_ami < 81:
        check_80_percent = True

    ami = math.floor(adjusted_ami)
    if check_50_percent == True:
        ami = 51
    if check_80_percent == True:
        ami = 81
    # format as percentage
    ami = "{}%".format(ami)
    return ami




#def income_eligibility(annual_income, household_size, AMI, FPL, SMI):




# form submission route
@app.route('/send', methods = ['POST'])
def send(fpl = sum, smi = sum, ami = sum):
    if request.method == 'POST':
        errors = False
        # start pulling data from form input

        # check that household size is an integer greater than 0
        try:
            if int(request.form['Household Size']) > 0:
                household_size = int(request.form['Household Size'])
        # else give an error
        except ValueError:
            flash('Household size must be a number greater than 0.')
            errors = True

        income_type = request.form['Income Type']
        raw_income = request.form['Income Amount']
        # remove dollar signs and commas from income
        clean_income = re.compile(r'[^\d.]+')
        raw_income = clean_income.sub('', raw_income)
        # check that income is a nonnegative number
        try:
            if float(raw_income) >= 0 and income_type == 'Monthly':
                annual_income = float(raw_income) * 12
            elif float(raw_income) >= 0 and income_type == 'Annual':
                annual_income = float(raw_income)
        # else give an error
        except ValueError:
            flash('Household income must be 0 or greater.')
            errors = True
        # if there's an error refresh the page
        if errors:
            return render_template('app.html')


    FPL = calculate_fpl(annual_income, household_size)
    SMI = calculate_smi(annual_income, household_size)
    AMI = calculate_ami(annual_income, household_size)

    return render_template('app.html', fpl = FPL, smi = SMI, ami = AMI)

if __name__ == ' __main__':
    app.debug = True
    app.run()




person = new_household(30000, 1)
print(person.calculate_fpl())