/* API call to generate and populate password field */
/* Made with help from Google AI */
async function fetchGeneratedPassword(inputX) {
    const api_uri = window.location.origin + "/painlesspass/api/pass_gen/";

    try {
        // Try the API endpoint
        const response = await fetch(api_uri);
        const data = await response.json();

        // Set value for inputField...
        inputX.value = data.gen_password;

    } catch (error) {
        console.error("Error fetching data from password generator API:", error);
    }
}

$(document).ready(function() {
    /* Toggles password field visibility based on pressing an icon above the field */
    /* Made with help from Google AI */
    const inputField = document.getElementById("id_password");
    const toggleIcon = document.getElementById("pass-toggle");
    const passGenButton = document.getElementById("pass-gen");

    if (toggleIcon) {
        toggleIcon.addEventListener("click", function () {
            if (inputField.type === "password") {
                inputField.type = "text";
                toggleIcon.className = "bi bi-eye-fill float-end ps-1"; // Change to a different eye icon
            } else {
                inputField.type = "password";
                toggleIcon.className = "bi bi-eye-slash-fill float-end ps-1";
            }
        });
    }

    /* TODO: Generate password and replace value field from API */

    /* Rotates the password generator icon, replaces field with generated password, makes it visible if it's not */
    if (passGenButton) {
        passGenButton.addEventListener("click", function () {
            fetchGeneratedPassword(inputField);
            passGenButton.classList.toggle("rotated");
            if (inputField.type === "password") {
                inputField.type = "text";
                toggleIcon.className = "bi bi-eye-fill float-end ps-1"; // Change to a different eye icon
            }
        });
    }
});