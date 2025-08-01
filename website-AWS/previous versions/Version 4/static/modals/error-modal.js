// static/modals/error-modal.js
// Handles error modal popup after failed signup form submission

document.addEventListener('DOMContentLoaded', function () {
    const errorModal = document.getElementById('error-modal');
    const errorMsg = document.getElementById('error-msg');
    const errorOverlay = document.getElementById('error-overlay');
    const closeBtn = document.getElementById('close-error-btn');

    const errorDataEl = document.getElementById('error-message-data');
    const errorText = errorDataEl?.dataset?.error?.trim();

    if (errorText && errorModal && errorMsg && errorOverlay && closeBtn) {
        errorMsg.textContent = errorText;
        errorModal.classList.remove('hidden');
        errorOverlay.classList.remove('hidden');

        closeBtn.addEventListener('click', function () {
            errorModal.classList.add('hidden');
            errorOverlay.classList.add('hidden');
        });
    }
});
