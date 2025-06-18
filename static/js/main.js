// Main JavaScript file for Sport Room Booking App

document.addEventListener("DOMContentLoaded", function () {
	// Initialize tooltips
	var tooltipTriggerList = [].slice.call(
		document.querySelectorAll('[data-bs-toggle="tooltip"]')
	);
	var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
		return new bootstrap.Tooltip(tooltipTriggerEl);
	});

	// Auto-hide alerts after 5 seconds
	const alerts = document.querySelectorAll(".alert:not(.alert-permanent)");
	alerts.forEach(function (alert) {
		setTimeout(function () {
			const bsAlert = new bootstrap.Alert(alert);
			bsAlert.close();
		}, 5000);
	});

	// Form validation helpers
	const forms = document.querySelectorAll(".needs-validation");
	forms.forEach(function (form) {
		form.addEventListener("submit", function (event) {
			if (!form.checkValidity()) {
				event.preventDefault();
				event.stopPropagation();
			}
			form.classList.add("was-validated");
		});
	});

	// Smooth scrolling for anchor links
	document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
		anchor.addEventListener("click", function (e) {
			e.preventDefault();
			const target = document.querySelector(this.getAttribute("href"));
			if (target) {
				target.scrollIntoView({
					behavior: "smooth",
					block: "start",
				});
			}
		});
	});

	// Loading states for buttons
	const loadingButtons = document.querySelectorAll("[data-loading]");
	loadingButtons.forEach((button) => {
		button.addEventListener("click", function () {
			const originalText = this.innerHTML;
			this.innerHTML =
				'<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
			this.disabled = true;

			// Re-enable after 3 seconds (adjust as needed)
			setTimeout(() => {
				this.innerHTML = originalText;
				this.disabled = false;
			}, 3000);
		});
	});
});

// Utility functions
function showToast(message, type = "info") {
	// Create toast element
	const toastContainer =
		document.getElementById("toast-container") || createToastContainer();

	const toastId = "toast-" + Date.now();
	const toastHtml = `
        <div id="${toastId}" class="toast align-items-center text-white bg-${type} border-0" role="alert">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>
    `;

	toastContainer.insertAdjacentHTML("beforeend", toastHtml);

	const toastElement = document.getElementById(toastId);
	const toast = new bootstrap.Toast(toastElement);
	toast.show();

	// Remove toast element after it's hidden
	toastElement.addEventListener("hidden.bs.toast", function () {
		this.remove();
	});
}

function createToastContainer() {
	const container = document.createElement("div");
	container.id = "toast-container";
	container.className = "toast-container position-fixed bottom-0 end-0 p-3";
	container.style.zIndex = "9999";
	document.body.appendChild(container);
	return container;
}

function formatDateTime(dateString) {
	const date = new Date(dateString);
	return date.toLocaleString("en-US", {
		year: "numeric",
		month: "short",
		day: "numeric",
		hour: "2-digit",
		minute: "2-digit",
	});
}

function validateTimeRange(startDate, startTime, endDate, endTime) {
	const start = new Date(`${startDate}T${startTime}`);
	const end = new Date(`${endDate}T${endTime}`);
	const now = new Date();

	if (start >= end) {
		return { valid: false, message: "End time must be after start time" };
	}

	if (start < now) {
		return { valid: false, message: "Booking time cannot be in the past" };
	}

	return { valid: true };
}

// Export functions for use in other scripts
window.SportBooking = {
	showToast,
	formatDateTime,
	validateTimeRange,
};
