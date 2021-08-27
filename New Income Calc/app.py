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

def calculate_fpl(annual_income, household_size):
    """
    Calculates the Federal Poverty Level based on HHS 2021 guidelines
    https://aspe.hhs.gov/topics/poverty-economic-mobility/poverty-guidelines
    """
    
    # FPL is calculated with a base rate times an additional rate per person
    fpl_base = 8340
    fpl_rate_per_person = 4540
    # calculate the FPL by dividing income by the base rate + household size
    # * the rate per person
    fpl = math.ceil(annual_income / ((household_size * fpl_rate_per_person)
                                      + fpl_base) * 100)
    # format as percentage
    fpl = "{}%".format(fpl)
    return fpl


def calculate_smi(annual_income, household_size):
    """
    Calculates the State Median Income based on DSHS 2021 guidelines
    https://www.dshs.wa.gov/esa/eligibility-z-manual-ea-z/state-median-income-chart

    """
    
    # SMI is calculated with separate base rates depending on household size
    # for families of 5 or less, and families of 6 or more
    smi_base_household_5_or_less = 36996
    smi_base_household_6_or_more = 135684
    # the rate for each person in a household of 5 or less
    smi_rate_household_5_or_less = 16452
    # the rate for each person in a household of 6 or more
    smi_rate_household_6_or_more = 2940
    
    # calculate the SMI depending on household size
    if household_size < 7:
        smi = annual_income / ((household_size * smi_rate_household_5_or_less) 
                               + smi_base_household_5_or_less) * 100
    elif household_size > 6:
        smi = annual_income / (smi_base_household_6_or_more + 
                               ((household_size - 6) * (smi_rate_household_6_or_more))) * 100 
    # round the SMI up
    smi = math.ceil(smi)
    # format as percentage
    smi = "{}%".format(smi)
    return smi

def calculate_ami(annual_income, household_size):
    """
    Calculates the Area Median Income based on HUD 2021 guidelines
    https://www.huduser.gov/portal/datasets/il/il2021/2021MedCalc.odn

    """
     # AMI is calculated from the median annual income for a family of 4
    ami_base_household_of_4 = 115700
    # 80% of area median annual income for a family of 4
    ami_base_80_percent = 90500
    # theoretical median income for a household of 0
    ami_base_0 = 69420
    # 80% of the median income for a household of 0
    ami_base_0_80_percent = 54300
    # for calculations when the initial AMI is between 70% and 80%
    ami_base_between_70_and_80 = 113125
    # initialize to false
    check_80_percent = False
    
    # calculate initial percentage to determine if it falls above or below 70%
    if household_size < 5:
        initial_ami = annual_income / ((ami_base_0) + (household_size * (ami_base_household_of_4 * .10))) * 100
        ami_80_cap = ((ami_base_0_80_percent * .08) + (ami_base_80_percent * .08) * (household_size * .10))        #80% CAP calculation in Hannah's excel calculator
    elif household_size > 4:
        initial_ami = annual_income / ((ami_base_household_of_4 * .08) * (household_size - 4) + ami_base_household_of_4) * 100
        ami_80_cap = ((ami_base_80_percent * .08) + ((ami_base_80_percent * .08) * (household_size - 4) * .08))
        
    
   
    # AMI adjustment for incomes that would normally fall between 70% and 80% of the AMI
    if initial_ami >= 71 and initial_ami <= 81:
        if household_size < 5:
            adjusted_ami = annual_income / (ami_base_between_70_and_80 + ((household_size - 4) * ami_base_between_70_and_80 * .10)) * 100
        else:
            adjusted_ami = annual_income / (ami_base_between_70_and_80 + ((household_size - 4) * ami_base_between_70_and_80 * .08)) * 100

    else:
        adjusted_ami = initial_ami

    print(ami_80_cap)
    # 80% CHECK:
    if annual_income > ami_80_cap and adjusted_ami < .81:
        check_80_percent = True
    
    ami = math.ceil(adjusted_ami)
    if check_80_percent == True:
        ami == 81
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


        raw_annual_income = request.form['Annual Income']
        # remove dollar signs and commas from income
        clean_income = re.compile(r'[^\d.]+')
        annual_income = clean_income.sub('', raw_annual_income)
        # check that annual income is a nonnegative number
        try:
            if float(annual_income) >= 0:
                annual_income = float(clean_income.sub('', raw_annual_income))
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


        

