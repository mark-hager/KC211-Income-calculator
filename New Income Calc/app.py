# -*- coding: utf-8 -*-
"""
Created on Mon Aug 23 13:31:56 2021

@author: mhager

Python implementation of Hannah Newton's Excel-based income calculator for 
use by King County 2-1-1 specialists.

Used https://github.com/nanoproductions/flask_calculator_basic for help with flask
"""
# math package used for rounding
import math
# import Flask
from flask import Flask, render_template, request
# create Flask object
app = Flask(__name__)
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
    _fpl_base = 8340
    _fpl_rate_per_person = 4540
    # calculate the FPL by dividing income by the base rate + household size
    # * the rate per person
    _fpl = math.ceil(annual_income / ((household_size * _fpl_rate_per_person)
                                      + _fpl_base) * 100)
    # format as percentage
    _fpl = "{}%".format(_fpl)
    return _fpl


def calculate_smi(annual_income, household_size):
    """
    Calculates the State Median Income based on DSHS 2021 guidelines
    https://www.dshs.wa.gov/esa/eligibility-z-manual-ea-z/state-median-income-chart

    """
    
    # SMI is calculated with separate base rates depending on household size
    # for families of 5 or less, and families of 6 or more
    _smi_base_household_5_or_less = 36996
    _smi_base_household_6_or_more = 135684
    # the rate for each person in a household of 5 or less
    _smi_rate_household_5_or_less = 16452
    # the rate for each person in a household of 6 or more
    _smi_rate_household_6_or_more = 2940
    
    # calculate the SMI depending on household size
    if household_size < 7:
        _smi = annual_income / ((household_size * _smi_rate_household_5_or_less) 
                               + _smi_base_household_5_or_less) * 100
    elif household_size > 6:
        _smi = annual_income / (_smi_base_household_6_or_more + 
                               ((household_size - 6) * (_smi_base_household_6_or_more))) * 100 
    # round the SMI up
    _smi = math.ceil(_smi)
    # format as percentage
    _smi = "{}%".format(_smi)
    return _smi

def calculate_ami(annual_income, household_size):
    """
    Calculates the Area Median Income based on HUD 2021 guidelines
    https://www.huduser.gov/portal/datasets/il/il2021/2021MedCalc.odn

    """
    # AMI is calculated from the median annual income for a family of 4
    _ami_base_household_of_4 = 115700
    # 80% of area median annual income for a family of 4
    _ami_base_80_percent = 90500
    # theoretical median income for a household of 0
    _ami_base_0 = 69420
    # 80% of the median income for a household of 0
    _ami_base_0_80_percent = 54300
    # initialize to false
    _check_80_percent = False
    
    if household_size < 5:
        _initial_ami = annual_income / ((_ami_base_0) + (household_size * (_ami_base_household_of_4 * .10))) * 100
        ami_80_cap = ((_ami_base_0_80_percent * .08) + (_ami_base_80_percent * .08) * (household_size * .10))        #80% CAP calculation in Hannah's excel calculator
    elif household_size > 4:
        _initial_ami = annual_income/ ((_ami_base_household_of_4 * .08) * (household_size - 4) + _ami_base_household_of_4) * 100
        ami_80_cap = ((_ami_base_80_percent * .08) + ((_ami_base_80_percent * .08) * (household_size - 4) * .08))
    
    #AMI adjustment for incomes that would normally fall between 71% and 81% of the AMI
    if _initial_ami >= 71 and _initial_ami <= 81:
        _adusted_ami = annual_income / ((_ami_base_80_percent) + (household_size - 4) * _ami_base_80_percent * .08) * 100
    else:
        _adjusted_ami = _initial_ami
    
    # More AMI calculations based on Hannah's excel calculator	
    # Variable _ami_base100b4 is taken directly from Hannah's excel; will rename once I find out what it means
    if _initial_ami < .71 and household_size < 5:
        _ami_base100b4 = _ami_base_0 + (_ami_base_household_of_4 * .10 * household_size)
    elif _initial_ami < .71 and household_size > 4:
        _ami_base100b4 = _ami_base_household_of_4 + (_ami_base_household_of_4 * .08 * (household_size - 4))
    elif _initial_ami > .7 and household_size < 5:
        _ami_base100b4 = _ami_base_0_80_percent + (household_size * .10 * _ami_base_80_percent)
    elif _initial_ami > .7 and household_size > 4:
        _ami_base100b4 = _ami_base_80_percent + ((household_size - 4) * .08 * _ami_base_80_percent)
	
    # 80% CHECK:
    if annual_income > ami_80_cap and _adjusted_ami < .81:
        _check_80_percent = True
    
    _rounded_ami = math.ceil(_adjusted_ami)
    if _check_80_percent == True:
        _rounded_ami == 81

    # format as percentage
    _rounded_ami = "{}%".format(_rounded_ami)
    return _rounded_ami 






# form submission route
@app.route('/send', methods = ['POST'])
def send(fpl = sum, smi = sum, ami = sum):
    if request.method == 'POST':
        # start pulling data from form input
        household_size = int(request.form['Household Size'])
        annual_income = int(request.form['Annual Income'])

    FPL = calculate_fpl(annual_income, household_size)
    SMI = calculate_smi(annual_income, household_size)
    AMI = calculate_ami(annual_income, household_size)
    
    return render_template('app.html', fpl = FPL, smi = SMI, ami = AMI)

if __name__ == ' __main__':
    app.debug = True
    app.run()


        

