"""
Python implementation of Hannah Newton's Excel-based income calculator for
use by King County 2-1-1 specialists. @author:mhager
Flask app takes inputs from the html form to determine eligibility for various
benefits programs based upon the annual income, size of the household, and
whether the household includes any minor children.
Also estimates birthyear and client age based upon the client's age or birthdate,
respectively.
"""
# for calculating client age
from datetime import datetime, date
import os

# import Flask
from flask import Flask, flash, render_template, request

# Gets the form data from html using flask_wtf and wtform
from form import HouseholdForm
# Use the data to get income measures and program eligibility
from income_measures import *
from program_eligibility import *

# create Flask object
app = Flask(__name__)
# default secret_key for development
app.secret_key = 'dev'
app.secret_key = os.environ.get('SECRET_KEY', 'dev')


# only one route since the calculator is only one page
@app.route("/", methods = ['GET', 'POST'])
def main():

    # get the data from the wtform
    form = HouseholdForm()
    # if POST request is valid and the data in the form passes validation
    if request.method == 'POST' and form.validate_on_submit():
        # dob field is not a wtform in order to use JavaScript on it
        raw_dob = request.form['dob_field']
        # then create a new household object
        client = NewHousehold(form, raw_dob)

        # determine program eligibility using household object
        eligibility = ProgramEligibility(client)

        return render_template('app.html', form = form, client = client, eligibility = eligibility)
    return render_template('app.html', form = form, client = None, eligibility = None)


class NewHousehold:
    """
    Uses validated data from the flask wtform to create
    a representation of a household for the purposes
    of determining income measures and program eligibility.
    """
    # default args for has_children, rent_amount and client_dob since these are optional fields
    def __init__(self, form, raw_dob):

        # required fields for calculating income measures
        self.annual_income = self.get_annual_income(form.income_amount.data, 
                                                    form.income_type.data)

        self.household_size = form.household_size.data

        # Calculate income measures using methods from income_measures.py
        self.ami = calculate_ami(self)
        self.fpl = calculate_fpl(self)
        self.smi = calculate_smi(self)

        # optional fields
        if hasattr(form, 'has_children'):
            self.has_children = form.has_children.data
        if hasattr(form, 'monthly_rent') and form.monthly_rent.data is not None: 
            self.monthly_rent = float(form.monthly_rent.data)
        if raw_dob is not None:
            self.age = self.calculate_age(raw_dob)

    def get_annual_income(self, income_amount, income_type):
        """
        Gets the income amount and type from the wtform and uniformly saves it as the annual
        income for the NewHousehold object by multiplying income amount by 12 when the income 
        type is monthly.
        """

        # convert flask_wtf decimal field to float for calculations
        if income_type == "Monthly":
            annual_income = float(income_amount * 12)
        else:
            annual_income = float(income_amount)
        return annual_income
    
    def calculate_age(self, raw_dob):
        """
        Calculates the client's age from their DOB.
        *TODO* validate dob by using custom wtform validator
        to give an error if DOB is invalid e.g a future date.
        """
        # try calculating age from the raw DOB string
        try:
            dob = datetime.strptime(
                        raw_dob,
                        '%Y-%m-%d')
            # roughly account for leapyears in calendar year
            age = int((datetime.today() - dob).days / 365.2425)
        except:
            return

        # check that the age is somewhat realistic
        if age > 0 and age < 120:
            return age
