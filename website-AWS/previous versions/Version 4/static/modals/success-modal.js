// /static/modals/success-modal.js
// Handles success modal popup after successful signup form submission

document.addEventListener('DOMContentLoaded', function () {
    const modal = document.getElementById('success-modal');
    const overlay = document.getElementById('success-overlay');
    const idDisplay = document.getElementById('success-id');
    const okBtn = document.getElementById('success-ok-btn'); // fixed ID match

    if (modal && overlay && idDisplay && okBtn) {
        const publicId = idDisplay.dataset.publicId || "???";
        const redirectUrl = okBtn.dataset.url || "/";

        idDisplay.textContent = publicId;
        modal.classList.remove('hidden');
        overlay.classList.remove('hidden');

        okBtn.addEventListener('click', function () {
            modal.classList.add('hidden');
            overlay.classList.add('hidden');
            window.location.href = redirectUrl;
        });
    }
});
