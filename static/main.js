// Select the required elements
const inputElement = document.getElementById('input');
const outputElement = document.getElementById('output');
const copyButton = document.getElementById('copy-button');
const navbar = document.getElementById('navbar');
const footer = document.getElementById('footer');

// Define the API endpoint URL
const apiUrl = 'http://127.0.0.1:8000/js2py';

// Set the initial mode to dark mode
let isDarkMode = true;

// Define a function to toggle the mode
function toggleMode() {
    // Toggle the mode flag
    isDarkMode = !isDarkMode;

    // Set the body class based on the mode
    document.body.className = isDarkMode ? 'dark-mode' : 'light-mode';

    // Set the navbar and footer colors based on the mode
    navbar.className = isDarkMode ? 'navbar navbar-dark bg-dark' : 'navbar navbar-light bg-light';
    footer.className = isDarkMode ? 'footer bg-dark text-light' : 'footer bg-light text-dark';
}


const convertBtn = document.getElementById("convert-btn");

convertBtn.addEventListener("click", async () => {
    const input = document.getElementById("input-text").value;
    const response = await fetch("/app", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({
            js_expression: input
        }),
    });
    const data = await response.json();
    document.getElementById("output-text").value = data.py_expression;
});


// Define a function to send the input to the API and update the output
async function updateOutput() {
    try {
        // Get the input value
        const inputValue = inputElement.value;

        // Send a POST request to the API with the input value
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                js_expression: inputValue
            })
        });

        // Parse the response as JSON
        const data = await response.json();

        // Set the output value
        outputElement.value = data.py_expression;
    } catch (error) {
        console.error(error);
    }
}

// Add event listeners to the input element and the copy button
inputElement.addEventListener('input', updateOutput);
copyButton.addEventListener('click', function () {
    // Select the output element and copy its value to the clipboard
    outputElement.select();
    document.execCommand('copy');
});

// Toggle the mode initially
toggleMode();

// Call the updateOutput function initially
updateOutput();
