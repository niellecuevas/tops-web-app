    // Get the modal and its content area
    const customModal = document.getElementById("bookingCustomModal");
    const customModalContentDiv = document.getElementById("custom-modal-form-content");
    // Function to open the modal and load the form into it
    function openCustomModal(event) {
        event.preventDefault(); // Prevent the default form action (submitting)
    
        // Fetch the content from bookvanform.html (if needed)
        fetch(bookVanFormUrl)
            .then(response => response.text())
            .then(data => {
                customModalContentDiv.innerHTML = data; // Insert the fetched HTML form into the modal
                customModal.style.display = "block"; // Display the modal
            })
            .catch(error => console.error('Error loading the form:', error));
    }
    
    // Attach event listeners to all buttons with class 'book-button'
    document.querySelectorAll(".custom-booking").forEach(button => {
            button.addEventListener("click", openCustomModal);
        });
    
        // Function to close the modal
    function closeCustomModal() {
        customModal.style.display = "none"; // Hide the modal
    }
    
    // Close modal when clicking outside of the modal content
    window.onclick = function(event) {
        if (event.target === customModal) {
            closeCustomModal();
        }
    };
    