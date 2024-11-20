document.addEventListener("DOMContentLoaded", function () {
  const sections = document.querySelectorAll(".hidden-section");

  // Create a new intersection observer
  const observer = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
          // Section is entering the viewport (scrolling down)
          if (entry.isIntersecting) {
              entry.target.classList.add("visible-section");
              entry.target.classList.remove("exiting-section");
          } 
          // Section is leaving the viewport (scrolling up)
          else {
              entry.target.classList.add("exiting-section");
              entry.target.classList.remove("visible-section");
          }
      });
  }, {
      threshold: 0.2, // Adjust this to determine when the section becomes visible (20% visibility)
  });

  sections.forEach((section) => {
      observer.observe(section); // Start observing each section
  });
});
     
        // Function to set the active class based on the current scroll position
        function setActiveLinkOnScroll() {
          const sections = document.querySelectorAll('div[id]'); // Select all sections
          const navLinks = document.querySelectorAll('.nav-link');
      
          let currentSection = '';
      
          sections.forEach(section => {
              const sectionTop = section.offsetTop;
              const sectionHeight = section.clientHeight;
      
              // Check if the section is in the viewport
              if (pageYOffset >= sectionTop - sectionHeight / 3) {
                  currentSection = section.getAttribute('id');
              }
          });
      
          navLinks.forEach(link => {
              link.classList.remove('active'); // Remove active class from all links
              if (link.getAttribute('href') === `#${currentSection}`) {
                  link.classList.add('active'); // Add active class to the current link
              }
          });
      }
            
// Call the function on scroll
window.addEventListener('scroll', setActiveLinkOnScroll);

// Call the function on page load to set the active link initially
document.addEventListener('DOMContentLoaded', setActiveLinkOnScroll);

document.addEventListener("DOMContentLoaded", function () {
  const counters = document.querySelectorAll(".stat-item h3");

  counters.forEach(counter => {
    counter.innerText = '0';

    const updateCounter = () => {
      const target = +counter.getAttribute('data-target');
      const current = +counter.innerText.replace(/,/g, ''); // Remove commas for calculation

      const increment = target / 200; // Adjust this value to control the speed

      if (current < target) {
        counter.innerText = Math.ceil(current + increment).toLocaleString(); // Format with commas
        setTimeout(updateCounter, 10); // Adjust timing if needed
      } else {
        if (target >= 10000) {
          // Add a + sign for numbers that need it, e.g., 10,000+
          counter.innerText = target.toLocaleString() + '+'; 
        } else {
          counter.innerText = target.toLocaleString(); // Regular formatting for other numbers
        }
      }
    };

    updateCounter();
  });
});