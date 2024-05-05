jQuery(document).ready(function($) {
  $('#predictionForm').submit(function(event) {
    event.preventDefault(); // Prevent default form submission (full page reload)

    // Get text input value
    var textInput = $('#text_input').val();

    // Send POST request to Flask server
    $.ajax({
      type: 'POST',
      url: '/predict',
      data: { text_input: textInput },
      success: function(response) {
        // Check if 'sentiment' key exists in the response
        if (response.sentiment !== undefined) {
          // Update predictionResult div with predicted sentiment
          var sentiment = response.sentiment;
          $('#predictionResult').html('Predicted Sentiment: ' + sentiment);
        } else if (response.error !== undefined) {
          // If 'error' key exists, display the error message
          var errorMessage = response.error;
          $('#predictionResult').html(errorMessage);
        } else {
          // Handle other cases if needed
          $('#predictionResult').html('Undefined response');
        }
      },
      error: function(xhr, status, error) {
        console.error('Error:', error);
        $('#predictionResult').html('Error occurred while predicting sentiment. Please try again.');
      }
    });
  });
});

// Function to handle form submission
function handleSubmit(event) {
    event.preventDefault();

    // Get form elements
    const form = document.getElementById('uploadForm');
    const fileInput = document.getElementById('fileInput');
    const filenameInput = document.getElementById('filenameInput');
    const formatSelect = document.getElementById('formatSelect');

    // Create FormData object
    const formData = new FormData(form);

    // Add filename and format to FormData
    formData.append('filename', filenameInput.value);
    formData.append('format', formatSelect.value);

    // Send POST request to server
    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (response.ok) {
            // Download the labeled dataset file
            response.blob().then(blob => {
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = filenameInput.value + '.' + formatSelect.value;
                document.body.appendChild(a);
                a.click();
                window.URL.revokeObjectURL(url);
            });
        } else {
            console.error('Error:', response.statusText);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Add event listener to form submission
const form = document.getElementById('uploadForm');
form.addEventListener('submit', handleSubmit);



