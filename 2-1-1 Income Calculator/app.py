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
@app.route("/", methods = ['POST', 'GET'])
def main():
    # get the data from the form submission
    form = HouseholdForm()
    # if POST request is valid and the data in the form passes validation
    if form.validate_on_submit():
        # then create a new household object
  
    return render_template('app.html', form = form)
        

    


def NewHousehold(form_data):
    """
    Uses validated data from the flask wtform to create
    a representation of a household for the purposes
    of determining income measures and program eligibility.
    """