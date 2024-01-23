"""
Retrieves data from wtforms in app.html to create new Household objects.
"""
# wtforms for input validation
from flask_wtf import FlaskForm
from wtforms import (IntegerField, BooleanField, SelectField, StringField, DecimalField)
from wtforms.validators import (InputRequired, NumberRange, Optional)


class HouseholdForm(FlaskForm):
    """
    Uses wtforms and flask_wtf to create forms in jina template with datatypes and validators
    specific to each field.
    """

    # required fields
    income_type = SelectField("Income Type", choices=['Monthly', 'Annual'],
                              default="Monthly", validators=[InputRequired()])

    income_amount = StringField("Income Amount", validators=[InputRequired()])

    household_size = IntegerField("Household Size", validators=[InputRequired(),
                                  NumberRange(min=1, max=99, message="Household size must be at least 1 and less than 100.")])

    # optional fields
    has_children = BooleanField('Children in Household')

    monthly_rent = StringField("Monthly Rent", validators=[Optional()])
