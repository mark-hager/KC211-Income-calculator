"""
Class containing methods for representing a household
in order to estimate eligibility for 
various state assistance programs based on
income measures and household size and composition.
"""
from datetime import datetime, date

from income_measures import *
# uses program eligibility requirements cefined in program_requirements.py
from program_eligibility import *

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
        
        self.program_eligibility()


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
    
    def program_eligibility(self):
        """
        Determines eligiblity for various benefits programs using the FPL, SMI, AMI
        and household composition, using the eligibility requirements
        defined in each of the program functions in program_eligibility.py
        """

        # programs that can be screened w/out rent
        apple_health = apple_health_eligibility(self)
        liheap = liheap_eligibility(self)
        wa_basic_food = basic_food_eligibility(self)

        # check for eligibility only if rent_amount is not empty
        if hasattr(self, 'monthly_rent'):
            hsp = hsp_eligibility(self)
        else:
            hsp = False

        # initialize list to hold program names that the client/household may
        # be eligible for; dynamically displayed by jinja template
        self.programs = []
        if wa_basic_food is True:
            self.programs.append("Washington Basic Food Program")
        if apple_health is True:
            self.programs.append("Apple Health")
        if hsp is True:
            self.programs.append("Housing Stability Project")
        if liheap is True:
            self.programs.append("Low Income Home Energy Assistance Program (LIHEAP)")
    
