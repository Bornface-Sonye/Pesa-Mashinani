let sidebar = document.querySelector(".sidebar");
let closeBtn = document.querySelector("#btn");
let searchBtn = document.querySelector(".bx-search");

closeBtn.addEventListener("click", () => {
    sidebar.classList.toggle("open");
    menuBtnChange();
})

searchBtn.addEventListener("click", () => {
    sidebar.classList.toggle("open");
    menuBtnChange();
})

function menuBtnChange() {
    if (sidebar.classList.contains("open")) {
        closeBtn.classList.replace("bx-menu", "bx-menu-alt-right");
    } else {
        closeBtn.classList.replace("bx-menu-alt-right", "bx-menu");
    }
}

/*menuBtnChange();


// script.js
function showSection(sectionId) {
    // Hide all sections
    var sections = document.querySelectorAll('.section');
    sections.forEach(function(section) {
      section.classList.remove('active');
    });
  
    // Show the selected section
    var selectedSection = document.getElementById(sectionId);
    selectedSection.classList.add('active');
  }
  */

  document.addEventListener("DOMContentLoaded", function () {
    // Logo animation on page load
    const logo = document.querySelector('.logo');
    if (logo) {
        logo.style.opacity = 0;
        logo.style.transform = 'translateY(-20px)';

        setTimeout(() => {
            logo.style.opacity = 1;
            logo.style.transform = 'translateY(0)';
        }, 500);
    }

    // Smooth scroll effect for anchor links
    const scrollLinks = document.querySelectorAll('a.scroll-link');
    scrollLinks.forEach(link => {
        link.addEventListener('click', e => {
            e.preventDefault();

            const targetId = link.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 20,
                    behavior: 'smooth'
                });
            }
        });
    });

    // Form validation and animations
    const form = document.querySelector('form');
    if (form) {
        form.addEventListener('submit', function (e) {
            // Example validation: Check if the national ID number is not empty
            const nationalIdInput = document.getElementById('id_national_id_number');
            if (!nationalIdInput.value.trim()) {
                e.preventDefault(); // Prevent form submission
                nationalIdInput.classList.add('invalid-input');
                
                // Shake animation for invalid input
                setTimeout(() => {
                    nationalIdInput.classList.remove('invalid-input');
                }, 500);
            }
            // You can add more validation for other fields here

            // Optional: Scroll to the top of the form on submission
            window.scrollTo({
                top: form.offsetTop - 20,
                behavior: 'smooth'
            });
        });

        // Optional: Add focus animation for input fields
        const inputFields = form.querySelectorAll('input[type="text"], select');
        inputFields.forEach(input => {
            input.addEventListener('focus', () => {
                input.classList.add('focus-outline');
            });

            input.addEventListener('blur', () => {
                input.classList.remove('focus-outline');
            });
        });
    }
});
