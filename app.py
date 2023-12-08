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
import os

# import Flask
from flask import Flask, flash, render_template, request

# Gets the form data from html using flask_wtf and wtform
from form import HouseholdForm
# Use the form data to create a new household object
from new_household import *


# create Flask object
app = Flask(__name__)
# default secret_key for development
app.secret_key = 'dev'
# overridden if there's a config file containing a secret_key
app.config.from_pyfile('config.py', silent=True)

# only one route since the calculator is only one page
@app.route("/", methods = ['POST'])
def main():
    """
    Creates the form and collects its data on post.
    Then creates a household object with information
    needed to determine program eligibility.
    """

    # get the data from the wtform
    form = HouseholdForm(meta={'csrf': False})
    # if POST request is valid and the data in the form passes validation
    if request.method == 'POST' and form.validate_on_submit():
        # dob field is not a wtform in order to use JavaScript on it
        raw_dob = request.form['dob_field']
        # then create a new household object
        client = NewHousehold(form, raw_dob)

        return render_template('app.html', form = form, client = client)
    return render_template('app.html', form = form, client = None)

if __name__ == '__main__':
    app.run(debug=True)
