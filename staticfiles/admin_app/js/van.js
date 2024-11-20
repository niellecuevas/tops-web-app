const fileInput = document.getElementById('file_upload');
const fileInfo = document.getElementById('file-info');
const fileNameDisplay = document.getElementById('file-name');

// Trigger file input when "Choose File" is clicked
document.querySelector('.browse-files-text').addEventListener('click', function() {
    fileInput.click();
});

fileInput.addEventListener('change', function() {
    const file = fileInput.files[0];
    if (file) {
        fileInfo.style.display = 'block'; // Show the file info div
        fileNameDisplay.textContent = file.name; // Display the file name
    } else {
        fileInfo.style.display = 'none'; // Hide the file info if no file is selected
    }
});

function confirmDelete(vanId) {
    Swal.fire({
        title: 'Are you sure?',
        text: "You won't be able to revert this!",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Yes, delete it!',
        cancelButtonText: 'No, cancel!',
    }).then((result) => {
        if (result.isConfirmed) {
            document.getElementById('delete-form-' + vanId).submit();
        }
    });
}