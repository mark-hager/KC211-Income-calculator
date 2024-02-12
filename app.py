"""
Python implementation of Hannah Newton's Excel-based income calculator for
use by King County 2-1-1 specialists. @author:mhager
Flask app takes inputs from the html form to determine eligibility for various
benefits programs based upon the annual income, size of the household, and
whether the household includes any minor children.
Also estimates birthyear and client age based upon the client's age or birthdate,
respectively.
"""

# import Flask
from flask import Flask, render_template, request
# Gets the form data from html using flask_wtf and wtform
from form import HouseholdForm
# Use the form data to create a new household object
from new_household import NewHousehold
# Used to calculate median income from guidelines as well as publication year
from income_measures import calculate_percentages, year_published
# uses program eligibility requirements cefined in program_requirements.py
from program_eligibility import check_eligibility


# create Flask object
app = Flask(__name__)
# default secret_key for development
app.secret_key = 'dev'
# overridden if there's a config file containing a secret_key
app.config.from_pyfile('config.py', silent=True)

# only one route since the calculator is only one page
@app.route("/", methods = ['GET', 'POST'])
def main():
    """
    Creates the form and collects its data on post.
    Then creates a household object with information
    needed to determine program eligibility.
    """
    # get the data from the wtform
    form = HouseholdForm(meta={'csrf': False})

    # load current income measurement data for tooltip
    form.income_measurements = {'AMI': year_published['ami'],
                                 'FPL': year_published['fpl'], 'SMI': year_published['smi']}

    # if POST request is valid and the data in the form passes validation
    if request.method == 'POST' and form.validate_on_submit():
        # dob field is not a wtform in order to use JavaScript on it
        raw_dob = request.form['dob_field']
        # then create a new household object
        client = NewHousehold(form, raw_dob)

        # get the AMI, FPL and SMI percentages for the household
        calculate_percentages(client)

        # gets list of programs client household may be eligible for
        client.programs = check_eligibility(client)

        return render_template('app.html', form = form, client = client)
    return render_template('app.html', form = form, client = None)

if __name__ == '__main__':
    app.run(debug=True)
