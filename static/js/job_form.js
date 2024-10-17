const tripTypeField = document.querySelector('#div_id_trip_option');
const citiesField = document.querySelector('#id_cities');
const tripTargetSelect = document.getElementById("div_id_trip_target");
const priceDisplay = document.getElementById("price_display");
const number_off_offers = document.getElementById("id_number_of_offers");
const form = document.querySelector('form'); // Get the form element
let base = 1000;
let offers = 0
let price = null


window.onload = function () {
    // Your JavaScript code to run when the HTML content is loaded or reloaded
    continent()
    offers_check()
};

function update_price() {
    price = base + offers * 1000
    priceDisplay.textContent = (price / 100).toFixed(2); // Display updated base
}

function cities() {
    const selectedOption = tripTypeField.querySelector('input:checked');
    if (selectedOption.value === 'Wiele miast') {
        citiesField.classList.remove('hidden');
    } else {
        citiesField.classList.add('hidden');
    }
    if (selectedOption.value === 'W jedną stronę') {
        $("#id_back_date").prop("required", false);
    } else {
        $("#id_back_date").prop("required", true);
    }
}

function continent() {
    let selectedValue = tripTargetSelect.querySelector('input:checked');

    if (selectedValue.value === 'Interkontynentalny') {
        base = 2000;
    } else {
        base = 1000;
    }
    offers_check()
    update_price()
}

function offers_check() {
    let value = number_off_offers.value
    value -= 2
    offers = value * base / 1000
    update_price()
}

document.addEventListener('DOMContentLoaded', function () {

    tripTypeField.addEventListener('change', function () {
        cities()
    });

    tripTargetSelect.addEventListener("change", function () {
        continent()
    });

    // Display updated base
    number_off_offers.addEventListener('change', function () {
        offers_check()
    })

    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        // Get the variable value from the base display element
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // Set the value of the hidden input field with the JavaScript variable value
        document.getElementById('js_price_value').value = price;

        // Submit the form
        form.submit();
    });


});
