// js function used to calculate client age from DOB field
// on the fly. since it's client side it doesn't require
// the data to be submitted.
function calculate_age(dob_input) {

    let dob = new Date(dob_input.target.value);

    let curr_day = new Date(Date.now())
    
    // simple js age calculation formula from
    // https://stackoverflow.com/questions/4076321/javascript-age-calculation
    let age = (curr_day.getFullYear() - dob.getFullYear());

    if (curr_day.getMonth() < dob.getMonth() || 
    // added dob.getDate()) + 1 because it was ahead one day for some reason
    curr_day.getMonth() == dob.getMonth() && curr_day.getDate() < (dob.getDate()) + 1) {
    age--;
 
    }

    if (age < 0 ) {
        document.getElementById("age_result").style.fontSize = "medium";
        document.getElementById("age_result").style.paddingLeft = "1px";

        document.getElementById("age_result").style.textDecoration = "none";

        age = "Invalid DOB!";
    // users can understand this
    /*
    } else if (age > 120) {
        document.getElementById("age_result").style.fontSize = "medium";
        document.getElementById("age_result").style.paddingLeft = "1px";

        document.getElementById("age_result").style.textDecoration = "none";

        age = "Error: DOB must be after 01/01/1900";
    */
    }
    else if (isNaN(age)) {
        document.getElementById("age_result").style.fontSize = "medium";
        document.getElementById("age_result").style.paddingLeft = "1px";
        document.getElementById("age_result").style.textDecoration = "none";
        age = "Invalid DOB!"

    } else {
        document.getElementById("age_result").style.fontSize = "x-large";
        document.getElementById("age_result").style.paddingLeft = "10px";
        document.getElementById("age_result").style.textDecoration = "underline";
        document.getElementById("age_result").style.textDecorationStyle = "double";
        
    }
    
    document.getElementById("age_result").innerHTML = age;
}
// formats income and monthly rent fields as currency with commas
function formatCurrency(input) {
    // remove non-numeric characters
    let value = input.value.replace(/[^0-9.]/g, '');
    // parse as float
    const parsedValue = parseFloat(value);
    // checking if the parsed value is a valid number
    if (!isNaN(parsedValue)) {
        // Ensure the value is less than 1 billion
        const maxValue = 999999999;
        value = Math.min(parsedValue, maxValue).toFixed(2);
        // format the number with commas
        value = Number(value).toLocaleString('en-US', { style: 'decimal', maximumFractionDigits: 2 });
    } else {
        // and handle the case where the input is not a valid number (NaN)
        value = '';
    }
    // update the input value
    input.value = value;
}
