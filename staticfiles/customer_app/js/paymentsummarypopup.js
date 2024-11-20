function loadTermsAndConditions() {
    fetch("/static/customer_app/xml/terms.xml") // Adjust to your path if needed
        .then(response => response.text())
        .then(data => {
            const parser = new DOMParser();
            const xmlDoc = parser.parseFromString(data, "text/xml");
            const termsSections = xmlDoc.getElementsByTagName("section");
            let termsHTML = '';

            Array.from(termsSections).forEach(section => {
                const title = section.getAttribute("title");
                const content = section.getElementsByTagName("content")[0];
                
                // Add section title
                termsHTML += `<h3>${title}</h3>`;
                
                // If content exists, add it
                if (content) {
                    termsHTML += `<p>${content.textContent.trim()}</p>`;
                }

                // Create a bulleted list for <item> elements
                const items = section.getElementsByTagName("item");
                if (items.length > 0) {
                    termsHTML += `<ul>`;
                    Array.from(items).forEach(item => {
                        termsHTML += `<li>${item.textContent.trim()}</li>`;
                    });
                    termsHTML += `</ul>`;
                }

                // Add any notes or contact information
                const notes = section.getElementsByTagName("note");
                Array.from(notes).forEach(note => {
                    termsHTML += `<p><em>${note.textContent.trim()}</em></p>`;
                });

                const contacts = section.getElementsByTagName("contact");
                Array.from(contacts).forEach(contact => {
                    termsHTML += `<p><strong>Contact:</strong><br>${contact.textContent.trim()}</p>`;
                });
            });

            // Insert terms HTML into the modal content div
            document.getElementById('terms-content').innerHTML = termsHTML;
        })
        .catch(error => console.error('Error fetching terms:', error));
}

// Event listener for opening and closing the modal
document.addEventListener("DOMContentLoaded", function() {
    document.getElementById('terms-link').onclick = function(event) {
        event.preventDefault();
        loadTermsAndConditions(); // Load the terms
        document.getElementById('terms-modal').style.display = 'block';
    };

    document.getElementById('close-modal').onclick = function() {
        document.getElementById('terms-modal').style.display = 'none';
    };

    window.onclick = function(event) {
        const modal = document.getElementById('terms-modal');
        if (event.target === modal) {
            modal.style.display = "none";
        }
    };
});
