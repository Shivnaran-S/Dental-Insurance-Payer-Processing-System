document.getElementById('uploadButton').addEventListener('click', function () {
    const fileInput = document.getElementById('fileInput');
    const message = document.getElementById('message');
    const loadingMessage = document.getElementById('loadingMessage');
    const viewMappingsLink = document.getElementById('viewMappingsLink');

    if (!fileInput.files.length) {
        message.textContent = "Please select a file.";
        return;
    }

    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('file', file);

    // Show loading message
    loadingMessage.style.display = 'block';
    message.textContent = '';

    // Add CSRF token to the request headers
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch('/upload/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': csrfToken,  // Include the CSRF token
        },
    })
    .then(response => response.json())
    .then(data => {
        message.textContent = data.message || data.error;
        if (data.message === "File processed successfully.") {
            viewMappingsLink.style.display = 'block';  // Show the "View Mappings" link
        }
    })
    .catch(error => {
        console.error("Error:", error);  // Log the error to the console
        message.textContent = "An error occurred while uploading the file.";
    })
    .finally(() => {
        // Hide loading message
        loadingMessage.style.display = 'none';
    });
});