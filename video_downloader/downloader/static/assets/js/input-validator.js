document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementsByTagName('form');

    form.addEventListener('input', function(event) {
        validateField(event.target);
    });

    form.addEventListener('submit', function(event) {
        let valid = true;
        const fields = form.querySelectorAll('input, select');
        fields.forEach(field => {
            if (!validateField(field)) {
                valid = false;
            }
        });

        if (!valid) {
            event.preventDefault();
        }
    });

    function validateField(field) {
        const errorSpan = document.getElementById('error-' + field.name);
        let valid = true;

        if (field.required && !field.value.trim()) {
            showError(errorSpan, 'This field is required.');
            valid = false;
        } else {
            clearError(errorSpan);
        }

        if (field.name === 'email' && !validateEmail(field.value)) {
            showError(errorSpan, 'Please enter a valid email address.');
            valid = false;
        }

        if (field.name === 'password1' && (field.value.length < 8 || field.value.length > 60)) {
            showError(errorSpan, 'Password must be at least 8 characters long.');
            valid = false;
        }

        if (field.name === 'password2') {
            const password1 = form.querySelector('input[name="password1"]').value;
            if (field.value !== password1) {
                showError(errorSpan, 'Passwords do not match.');
                valid = false;
            }
        }

        return valid;
    }

    function showError(element, message) {
        element.textContent = message;
        element.style.display = 'block';
    }

    function clearError(element) {
        element.textContent = '';
        element.style.display = 'none';
    }

    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    }
});


/* document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementsByTagName('form');
    form.addEventListener('input', function (event) {
        const field = event.target.name;
        const value = event.target.value;
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
        const url = "{% url 'validate_form_field' %}";

        if (field) {
            fetch(`${url}?field=${field}&value=${value}`, {
                method: 'GET',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json'
                }
            })
            .then(response => response.json())
            .then(data => {
                const errorDiv = document.getElementById(`${field}-error`);
                if (data[field]) {
                    errorDiv.textContent = data[field];
                    event.target.classList.add('is-invalid');
                    event.target.classList.remove('is-valid');
                } else {
                    errorDiv.textContent = '';
                    event.target.classList.remove('is-invalid');
                    event.target.classList.add('is-valid');
                }
            });
        }
    });
});
 */
