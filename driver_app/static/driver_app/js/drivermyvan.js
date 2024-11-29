function toggleAvailability(vanId, isAvailable) {
    fetch(`/toggle-availability/${vanId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ availability: isAvailable })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert(`Van availability updated to: ${data.availability ? 'Available' : 'Not Available'}`);
            // You can update the UI here if needed (e.g., change text or colors)
        } else {
            alert('Error updating availability.');
        }
    })
    .catch(error => console.error('Error:', error));
}