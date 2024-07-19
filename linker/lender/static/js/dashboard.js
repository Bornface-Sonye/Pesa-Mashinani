       var hamburger = document.querySelector(".hamburger");
	hamburger.addEventListener("click", function(){
		document.querySelector("body").classList.toggle("active");
	})


	function hideAllForms() {
		document.querySelectorAll('.form-section').forEach(function(formSection) {
			formSection.classList.add('hidden');
		});
	}

	function showForm(formId) {
		hideAllForms();
		document.getElementById(formId).classList.remove('hidden');
	}
	// Function to start the progress animation
	function startProgress() {
		var progressBar = document.getElementById('progress-bar');
		progressBar.style.visibility = 'visible'; // Show the progress bar
	}

	// Function to stop the progress animation (called when the report is generated or downloaded)
	function stopProgress() {
		var progressBar = document.getElementById('progress-bar');
		progressBar.style.visibility = 'hidden'; // Hide the progress bar
	}

	// Listen for the X-Stop-Progress response header and stop the progress animation
	window.addEventListener('load', function() {
		var xhr = new XMLHttpRequest();
		xhr.onreadystatechange = function() {
			if (xhr.readyState === XMLHttpRequest.DONE) {
				if (xhr.getResponseHeader('X-Stop-Progress') === 'true') {
					stopProgress(); // Call stopProgress function
				}
			}
		};
		xhr.open('GET', document.location, true);
		xhr.send(null);
	});


	// JavaScript to toggle dropdown menu visibility
document.addEventListener("DOMContentLoaded", function () {
    const dropdownToggles = document.querySelectorAll(".dropdown-toggle");

    dropdownToggles.forEach(function (toggle) {
        toggle.addEventListener("click", function (e) {
            e.preventDefault();
            const parentLi = this.parentElement;
            const dropdownMenu = parentLi.querySelector(".dropdown-menu");

            // Toggle active class to show/hide dropdown
            dropdownMenu.classList.toggle("active");
        });
    });
});
