// /static/modals/consent-modal.js
// Handles consent modal popup before allowing signup form submission

document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('signup-form');
    const modal = document.getElementById('consent-modal');
    const overlay = document.getElementById('modal-overlay');
    const checkbox = document.getElementById('consent-checkbox');
    const confirmBtn = document.getElementById('consent-confirm');

    let consentGiven = false;

    if (form && modal && checkbox && confirmBtn && overlay) {
        form.addEventListener('submit', function (e) {
            // If user hasn't already confirmed, show the modal
            if (!consentGiven) {
                e.preventDefault(); // Prevent submission if modal is still open
                modal.classList.remove('hidden');
                overlay.classList.remove('hidden');
            }
        });

        confirmBtn.addEventListener('click', function () {
            if (checkbox.checked) {
                consentGiven = true;
                modal.classList.add('hidden');
                overlay.classList.add('hidden');
                form.submit(); // Proceed with form submission
            } else {
                alert("Please check the box to confirm.");
            }
        });
    }
});

