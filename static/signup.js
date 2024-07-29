document.addEventListener('DOMContentLoaded', function() {
    const phoneInputField = document.getElementById('phone');
    const phoneInput = window.intlTelInput(phoneInputField, {
        initialCountry: 'auto',
        geoIpLookup: function(callback) {
            fetch('https://ipinfo.io', {
                headers: { 'Accept': 'application/json' }
            })
            .then((resp) => resp.json())
            .then((resp) => {
                const countryCode = (resp && resp.country) ? resp.country : 'us';
                callback(countryCode);
            });
        },
        utilsScript: 'https://cdnjs.cloudflare.com/ajax/libs/intl-tel-input/17.0.13/js/utils.js'
    });

    document.getElementById('signup-form').addEventListener('submit', function(event) {
        event.preventDefault(); // Prevent form from submitting

        // Clear previous errors
        clearErrors();

        // Validate each field
        let isValid = true;

        // Name validation (must not be empty)
        const name = document.getElementById('name').value.trim();
        if (!name.match(/^[a-zA-Z ]+$/)) {
            showError('nameError', 'Name must contain only letters and spaces.');
            isValid = false;
        }

        // Email validation (HTML5 email validation is sufficient)
        const email = document.getElementById('email').value.trim();
        if (!email.match(/^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/)) {
            showError('emailError', 'Invalid email format.');
            isValid = false;
        }

        // Phone validation
        if (!phoneInput.isValidNumber()) {
            showError('phoneError', 'Invalid phone number.');
            isValid = false;
        }

        // Date of birth validation (must be in the past)
        const dob = document.getElementById('date-of-birth').value;
        const dobDate = new Date(dob);
        const today = new Date();
        if (dobDate >= today) {
            showError('date-of-birthError', 'Date of birth must be in the past.');
            isValid = false;
        }

        // Username validation (example: must be alphanumeric and between 3-16 characters)
        const username = document.getElementById('username').value.trim();
        if (!username.match(/^[a-zA-Z0-9]{3,16}$/)) {
            showError('usernameError', 'Username must be 3-16 alphanumeric characters.');
            isValid = false;
        }

        // Password validation (example: at least 6 characters)
        const password = document.getElementById('password').value.trim();
        if (password.length < 6) {
            showError('passwordError', 'Password must be at least 6 characters long.');
            isValid = false;
        }

        // If all validations pass, submit the form
        if (isValid) {
            alert('Form submitted successfully!');
            // Optionally, you can submit the form programmatically here
            // event.target.submit();
        }
    });

    function showError(elementId, message) {
        document.getElementById(elementId).innerText = message;
    }

    function clearErrors() {
        const errors = document.querySelectorAll('.error');
        errors.forEach(error => error.innerText = '');
    }
});
