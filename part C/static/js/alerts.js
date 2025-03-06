// alerts.js - Handles displaying styled alerts
function showAlert(message, type = 'info', title = '') {
    // Set default title based on alert type
    if (!title) {
        if (type === 'success') title = 'Success';
        else if (type === 'error') title = 'Error';
        else title = 'Notification';
    }

    // Remove previous alerts
    const existingAlerts = document.querySelectorAll('.alert-popup');
    existingAlerts.forEach(alert => alert.remove());

    // Create new alert
    const alertEl = document.createElement('div');
    alertEl.className = `alert-popup ${type}`;

    alertEl.innerHTML = `
        <div class="alert-header">${title}</div>
        <div class="alert-content">${message}</div>
        <div class="alert-actions">
            <button class="alert-button">OK</button>
        </div>
    `;

    // Add to document
    document.body.appendChild(alertEl);

    // Close button listener
    alertEl.querySelector('.alert-button').addEventListener('click', () => {
        alertEl.style.animation = 'fadeOut 0.3s forwards';
        setTimeout(() => alertEl.remove(), 300);
    });

    // Auto-close after 5 seconds
    setTimeout(() => {
        if (alertEl.parentElement) {
            alertEl.style.animation = 'fadeOut 0.3s forwards';
            setTimeout(() => alertEl.remove(), 300);
        }
    }, 5000);
}

// Detect server messages and display in the new format
document.addEventListener('DOMContentLoaded', () => {
    // Identify server messages
    const flashMessages = document.querySelectorAll('.flash-message');

    flashMessages.forEach(msg => {
        const type = msg.classList.contains('error') ? 'error' :
                    msg.classList.contains('success') ? 'success' : 'info';

        let title = 'Notification';
        if (type === 'error') title = 'Error';
        if (type === 'success') title = 'Success';

        showAlert(msg.textContent, type, title);
        msg.style.display = 'none'; // Hide the original message
    });
});

// Define global function for local alerts
window.showAlert = showAlert;