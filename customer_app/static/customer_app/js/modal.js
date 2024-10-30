        //carousel Jscript
        let currentSlide = 0;

        function showSlide(index) {
            const slides = document.querySelectorAll('.carousel-slide');
            if (index >= slides.length) {
                currentSlide = 0;
            } else if (index < 0) {
                currentSlide = slides.length - 1;
            } else {
                currentSlide = index;
            }

            slides.forEach((slide, i) => {
                slide.style.display = (i === currentSlide) ? 'flex' : 'none';
            });
        }

        function moveSlide(direction) {
            showSlide(currentSlide + direction);
        }

        document.addEventListener('DOMContentLoaded', () => {
            showSlide(currentSlide); // Initialize the first slide
        });

        document.addEventListener('DOMContentLoaded', () => {
    showSlide(currentSlide); // Initialize the first slide

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

    // Store data in localStorage
    localStorage.setItem('vanImage', vanImage);
    localStorage.setItem('vanModel', vanModel);
    localStorage.setItem('vanDriver', vanDriver);
    localStorage.setItem('vanSeats', vanSeats);

    // Fetch the content from bookvanform.html (if needed)
    fetch(bookVanFormUrl)
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

    
    document.addEventListener("DOMContentLoaded", function() {
    // Check if the user came from the payment form
    var cameFromPayment = "{{ came_from_payment|default:'false' }}";
    if (cameFromPayment === "true") {
        // Open the modal
        var modal = document.getElementById("bookingModal");
        modal.style.display = "block"; // or use a function to open your modal

        // Populate the modal with data
        document.getElementById("modal-form-content").innerHTML = `
            <h2>Booking Details</h2>
            <p>Full Name: {{ full_name }}</p>
            <p>Passenger Count: {{ passenger_count }}</p>
            <p>Contact Number: {{ contact_number }}</p>
            <p>Pickup DateTime: {{ pickup_datetime }}</p>
            <p>Pickup Address: {{ pickup_address }}</p>
            <p>Dropoff Address: {{ dropoff_address }}</p>
            <p>Additional Notes: {{ additional_notes }}</p>
            <p>Round Trip: {{ round_trip }}</p>
        `;
    }
});
    // Attach event listeners to all buttons with class 'book-button'
    document.querySelectorAll(".book-button").forEach(button => {
        button.addEventListener("click", openModal);
    });

    // Close the modal when the close button (x) is clicked
    closeButton.onclick = function() {
        modal.style.display = "none";
        modalContentDiv.innerHTML = ""; // Clear the modal content when it's closed
    }

    // Close the modal if the user clicks outside the modal
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
            modalContentDiv.innerHTML = ""; // Clear the modal content when closed
        }
    }
});



const cameFromPayment = JSON.parse('{{ came_from_payment|default:"false"|escapejs }}');

    window.onload = function() {
        // Check if the user came from the payment success page
        if (cameFromPayment) {
            document.getElementById('bookingModal').style.display = 'block'; // Show the modal
        }
    };

    document.addEventListener("DOMContentLoaded", function () {
        // Get the modal and close button elements
        const modal = document.getElementById("bookingModal");
        const closeButton = document.querySelector(".close-button");

        // Function to update the URL and reload the page
        function updateUrlAndReload() {
            const currentUrl = window.location.href;

            if (currentUrl.includes('?came_from_payment=true')) {
                // Replace the current URL to remove the query parameter
                const newUrl = currentUrl.split('?')[0];
                history.replaceState(null, null, newUrl);

                // Reload the page after the URL has been updated
                window.location.reload();
            } else {
                // Hide the modal if no query parameter
                modal.style.display = "none";
            }
        }

        // Event listener for closing the modal with the close button
        closeButton.addEventListener("click", function () {
            updateUrlAndReload();
        });

        // Event listener for clicking outside the modal to close it
        window.addEventListener("click", function (event) {
            if (event.target === modal) {
                updateUrlAndReload();
            }
        });
    });

    // Optional: Close modal when clicking outside of it
    window.onclick = function(event) {
        const modal = document.getElementById('bookingModal');
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };