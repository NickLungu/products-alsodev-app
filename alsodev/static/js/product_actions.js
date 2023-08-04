$(document).ready(function() {
    $('#add-product-form').submit(function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Create a new FormData object
        var formData = new FormData(this);

        // Send an AJAX request to the server
        $.ajax({
            url: '/add_product/',
            type: 'POST',
            data: formData,
            processData: false, // Prevent jQuery from processing the data
            contentType: false, // Prevent jQuery from setting the content type
            success: function(response) {
                if (response.success) {
                    // Product added successfully
                    console.log('Product added successfully!');
                    // Display a success message on your website
                    $('#add-product-form').replaceWith('<h3>Product added successfully!</h3>');
                } else {
                    // Error occurred while adding the product
                    console.log('Error occurred while adding product.');
                    // Check if there are any errors in the response
                    if (response.errors) {
                        // Display the form errors on your website or perform any other action
                        console.log(response.errors);
                    }
                    // Handle any other actions or display an error message
                }
            },
            error: function() {
                // Handle any errors
                // You can display an error message or perform any other action
                console.error('Error occurred while adding product.');
            }
        });
    });
    $('#update-product-form').submit(function(event) {
        event.preventDefault(); // Prevent the default form submission

        // Create a new FormData object
        var formData = new FormData(this);
        var product_id = $(this).data('product-id');

        // Send an AJAX request to the server
        $.ajax({
            url: '/update_product/' + product_id + '/',
            type: 'POST',
            action: this.action,
            data: formData,
            processData: false, // Prevent jQuery from processing the data
            contentType: false, // Prevent jQuery from setting the content type
            success: function(response) {
                if (response.success) {
                    // Product added successfully
                    console.log('Product updated successfully!');
                    // Display a success message on your website
                    $('#update-product-form').replaceWith('<h3>Product updated successfully!</h3>');
                } else {
                    // Error occurred while adding the product
                    console.log('Error occurred while updating product.');
                    // Check if there are any errors in the response
                    if (response.errors) {
                        // Display the form errors on your website or perform any other action
                        console.log(response.errors);
                    }
                    // Handle any other actions or display an error message
                }
            },
            error: function() {
                // Handle any errors
                // You can display an error message or perform any other action
                console.error('Error occurred while adding product.');
            }
        });
    });
    $('.delete-image-btn').click(function(event) {
        event.preventDefault();

        // Get the image ID from the data attribute
        var imageId = $(this).data('image-id');

        // Retrieve the CSRF token from the form's data attribute
        console.log('1')
        var csrfToken = $('#update-product-form').data('csrf-token');
        console.log(csrfToken)
        console.log('2')

        // Send an AJAX request to delete the image
        $.ajax({
            url: '/delete_image/' + imageId + '/',
            type: 'POST',
            data: {
                csrfmiddlewaretoken: csrfToken
            },
            success: function(response) {
                if (response.success) {
                    // Image deleted successfully
                    // Remove the image element from the UI
                    $('#image-' + imageId).remove();
                } else {
                    // Error occurred while deleting the image
                    console.log('Error occurred while deleting image 1.');
                    // Handle the error or display an error message
                }
            },
            error: function() {
                // Handle any errors
                console.error('Error occurred while deleting image 2.');
            }
        });
    });
    // Update the image preview when a file is selected
    $('#id_images').change(function() {
      var fileInput = $(this)[0];

      if (fileInput.files && fileInput.files[0]) {
        var reader = new FileReader();

        reader.onload = function(e) {
          $('#image-preview').html('<img style="max-height:60px;" src="' + e.target.result + '" alt="Preview">');
        };

        reader.readAsDataURL(fileInput.files[0]);
      }
    });

});
function showNextFeatureField(button) {
    var featureContainer = button.parentElement;
    var nextFeatureContainer = featureContainer.nextElementSibling;

    var inputFields = featureContainer.querySelectorAll('input[type="text"]');

    for (var i = 0; i < inputFields.length; i++) {
        if (inputFields[i].value.trim() === '') {
            console.log('Input field ' + (i + 1) + ' is empty');
            // Perform any desired actions for empty input fields
            return; // Exit the function if any input field is empty
        }
    }

    console.log('All input fields are not empty');

    if (nextFeatureContainer) {
        nextFeatureContainer.style.display = 'block';
    }
}
