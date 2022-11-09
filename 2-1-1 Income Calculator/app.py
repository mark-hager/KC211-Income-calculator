"""
Python implementation of Hannah Newton's Excel-based income calculator for
use by King County 2-1-1 specialists. @author:mhager
Flask app takes inputs from the html form to determine eligibility for various
benefits programs based upon the annual income, size of the household, and
whether the household includes any minor children.
Also estimates birthyear and client age based upon the client's age or birthdate,
respectively.
"""

# used for formatting user inputs by stripping dollar signs and commas
import re
import os

# import Flask
from flask import Flask, flash, render_template, request

# Gets the form data from html using flask_wtf and wtform
from form import HouseholdForm
# Use the data to get income measures and program eligibility
from income_measures import *
#from program_eligibility import *

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
        # then create a new household object
        client = NewHousehold(form)

        # calculate the income measures using the household data
        client_income = IncomeMeasures(client)

        return render_template('app.html', form = form, client = client, income = client_income)
    return render_template('app.html', form=form, client=None, income=None)


class NewHousehold:
    """
    Uses validated data from the flask wtform to create
    a representation of a household for the purposes
    of determining income measures and program eligibility.
    """
    # default args for has_children, rent_amount and client_dob since these are optional fields
    def __init__(self, form):
        # convert flask_wtf decimal field to float for calculations
        self.annual_income = float(form.income_amount.data)
        self.household_size = form.household_size.data

        # optional fields
        if hasattr(form, 'has_children'):
            self.has_children = form.has_children.data
        if hasattr(form, 'rent_amount'):
            self.rent_amount = form.rent_amount.data

        # client_dob and client_age are used for calculating age from birthdate
        # and estimating year of birth from age, respectively
        # self.client_age = client_age
        # self.client_dob = client_dob

        # used for determininig eligibility to HSP which requires a rent to income ratio of 1:1.5
        