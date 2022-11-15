
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
        age = "Error: DOB may not be a future date";
    } else if (age > 120) {
        age = "Error: DOB must be after 01/01/1900";

    } else if (isNaN(age)) {
        return "Error: Invalid DOB"
    }
    
    document.getElementById("age_result").innerHTML = age;

}

