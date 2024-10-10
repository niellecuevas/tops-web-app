
    document.addEventListener("DOMContentLoaded", function() {
        const passengerCountInput = document.getElementById('passenger-count');
        const grandTotalDisplay = document.getElementById('grand-total-display');
        const grandTotalInput = document.getElementById('grand-total');  // Hidden input field for storing plain value

        // Function to update grand total
        function updateGrandTotal() {
            let passengerCount = parseInt(passengerCountInput.value) || 0;
            let grandTotal = passengerCount * 1000;

            // Update both the display and hidden input fields
            grandTotalDisplay.value = grandTotal.toLocaleString('en-PH');  // Display formatted number
            grandTotalInput.value = grandTotal;  // Store plain number
        }

        // Update total whenever passenger count changes
        passengerCountInput.addEventListener('input', updateGrandTotal);

        // Run once on page load to set initial value
        updateGrandTotal();
    });