const originalFileInput = document.getElementById('file_upload_original');
const fileInfoOriginal = document.getElementById('file-info-original');
const fileNameDisplayOriginal = document.getElementById('file-name-original');

// Trigger file input when "Upload an Image" label is clicked
document.querySelector('.file-upload-label').addEventListener('click', function() {
    originalFileInput.click();
});

// Display the selected file name
originalFileInput.addEventListener('change', function() {
    const file = originalFileInput.files[0];
    if (file) {
        fileInfoOriginal.style.display = 'block'; // Show the file info div
        fileNameDisplayOriginal.textContent = file.name; // Display the file name
    } else {
        fileInfoOriginal.style.display = 'none'; // Hide the file info if no file is selected
    }
});


function openModal(driverId, name, license, vanModel, plateNumber) {
    document.getElementById('myModal').style.display = 'block';
    
    // Populate the modal form with the respective row data
    document.getElementById('driver_id').value = driverId;
    document.getElementById('modal_name').value = name;
    document.getElementById('modal_license').value = license;
    document.getElementById('modal_van_model').value = vanModel;
    document.getElementById('modal_plate_number').value = plateNumber;

    // Clear any existing file from the file input field
    document.getElementById('modal_file_upload').value = "";
    document.getElementById('file-name-display').textContent = "No file selected";
}

function closeModal() {
    document.getElementById('myModal').style.display = 'none';
}

document.getElementById('updateDriverForm').onsubmit = function(event) {
    event.preventDefault();
    
    let formData = new FormData(this);

    fetch(updateDriverUrl, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(data.message);
            location.reload();  // Reload the page to reflect the changes in the table
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("An error occurred while updating the driver.");
    });
};

function displayFileName() {
    const fileInput = document.getElementById('modal_file_upload');
    const fileNameDisplay = document.getElementById('file-name-display');

    if (fileInput.files.length > 0) {
        fileNameDisplay.textContent = fileInput.files[0].name;
    } else {
        fileNameDisplay.textContent = "No file selected";
    }
}


// SORT
function sortTable() {
    const table = document.querySelector("table tbody");
    const rows = Array.from(table.querySelectorAll("tr"));

    // Determine the sort order
    const sortOrder = document.getElementById("sortDrivers").value;

    // Sort rows based on the Driver ID (assuming Driver ID is in the first cell)
    rows.sort((a, b) => {
        const idA = a.cells[0].innerText;  // Driver ID in the first column
        const idB = b.cells[0].innerText;
        
        // Remove 'DRV' prefix for numeric comparison
        const numA = parseInt(idA.replace('DRV', ''));
        const numB = parseInt(idB.replace('DRV', ''));

        return sortOrder === "asc" ? numA - numB : numB - numA;
    });

    // Remove existing rows from the table
    rows.forEach(row => table.appendChild(row)); // Re-append sorted rows to the table
}


// SEARCH BY DRIVER NAME
function searchTable() {
    const searchInput = document.getElementById("searchDriver").value.toLowerCase();
    const table = document.querySelector("table tbody");
    const rows = Array.from(table.querySelectorAll("tr"));

    rows.forEach(row => {
        const driverName = row.cells[1].innerText.toLowerCase(); // Assuming the name is in the second cell
        if (driverName.includes(searchInput)) {
            row.style.display = ""; // Show row if it matches
        } else {
            row.style.display = "none"; // Hide row if it doesn't match
        }
    });
}