"""
Retrieves data from wtforms in app.html to create new Household objects.
"""
from datetime import date
# wtforms for input validation
from flask_wtf import FlaskForm
from wtforms import (DateField, TextAreaField, IntegerField, BooleanField,
                     RadioField, SelectField, DecimalField)
from wtforms.validators import (DataRequired, InputRequired, Length, 
                                NumberRange, Optional, ValidationError)

class HouseholdForm(FlaskForm):
    """
    Uses wtforms and flask_wtf to validate wtform from jinja template.
    """

    # required fields

    income_type = SelectField("Income Type", choices=['Monthly', 'Annual'],
                              default="Monthly", validators=[InputRequired()])

    income_amount = DecimalField("Income Amount", validators=[InputRequired(),
                                 NumberRange(min=0, message="Income must be greater than 0.")])

    household_size = IntegerField("Household Size", validators=[InputRequired(),
                                  NumberRange(min=1, message="Household size must be at least 1.")])
    # optional fields
    has_children = BooleanField('Children in Household')

    monthly_rent = DecimalField("Monthly Rent", 
                                validators=[Optional(), 
                                NumberRange(min=0, message="Income must be greater than 0.")])
    client_dob = DateField("Client DOB", validators=[Optional()])


