    // Get the modal and its content area
    const modal = document.getElementById("bookingModal");
    const modalContentDiv = document.getElementById("modal-form-content");
    
    // Function to open the modal and load the form into it
    function openModal(event) {
        event.preventDefault(); // Prevent the default form action (submitting)
    
        // Get data attributes from the clicked button
        const button = event.currentTarget;
        const vanImage = button.getAttribute('data-van-image');
        const vanModel = button.getAttribute('data-van-model');
        const vanDriver = button.getAttribute('data-van-driver');
        const vanSeats = button.getAttribute('data-van-seats');
    
        // Populate modal content
        document.getElementById("modal-van-img").src = vanImage;
        document.getElementById("modal-van-model").innerText = vanModel;
        document.getElementById("modal-driver-name").innerText = vanDriver;
        document.getElementById("modal-van-seater").innerText = vanSeats;
    
         // Set the hidden inputs with van details
        document.getElementById("hidden-van-image").value = vanImage;
        document.getElementById("hidden-van-model").value = vanModel;
        document.getElementById("hidden-van-driver").value = vanDriver;
        document.getElementById("hidden-van-seats").value = vanSeats;
    
        // Fetch the content from bookvanform.html (if needed)
        fetch("{% url 'bookvanform' %}")
            .then(response => response.text())
            .then(data => {
                modalContentDiv.innerHTML = data; // Insert the fetched HTML form into the modal
                modal.style.display = "block"; // Display the modal
            })
            .catch(error => console.error('Error loading the form:', error));
    }
    
    // Function to close the modal
    function closeModal() {
        modal.style.display = "none"; // Hide the modal
    }
    
    // Close modal when clicking outside of the modal content
    window.onclick = function(event) {
        if (event.target === modal) {
            closeModal();
        }
    };
    
    