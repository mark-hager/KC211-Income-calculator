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


class DollarField(DecimalField):
    """
    Custom subclass of wtform's decimal field that allows for commmas to be submitted along with 
    the decimal itself. Thanks to stackoverflow!
    https://stackoverflow.com/questions/20876217/wtforms-custom-field-for-dollar-values
    """
    def process_formdata(self, valuelist):
        for val in valuelist:
            self.data = [valuelist[0].replace(',', '')]
        # Calls "process_formdata" on the parent types of "DollarField",
        # which includes "DecimalField"
        super(DollarField).process_formdata(self.data)

class HouseholdForm(FlaskForm):
    """
    Uses wtforms and flask_wtf to create forms in jina template with datatypes and validators
    specific to each field.
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