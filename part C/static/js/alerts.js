// alerts.js - מטפל בהצגת התראות באופן מעוצב
function showAlert(message, type = 'info', title = '') {
    // קביעת כותרת ברירת מחדל לפי סוג ההתראה
    if (!title) {
        if (type === 'success') title = 'Success';
        else if (type === 'error') title = 'Error';
        else title = 'Notification';
    }

    // הסרת התראות קודמות
    const existingAlerts = document.querySelectorAll('.alert-popup');
    existingAlerts.forEach(alert => alert.remove());

    // יצירת התראה חדשה
    const alertEl = document.createElement('div');
    alertEl.className = `alert-popup ${type}`;

    alertEl.innerHTML = `
        <div class="alert-header">${title}</div>
        <div class="alert-content">${message}</div>
        <div class="alert-actions">
            <button class="alert-button">OK</button>
        </div>
    `;

    // הוספה למסמך
    document.body.appendChild(alertEl);

    // מאזין לסגירה
    alertEl.querySelector('.alert-button').addEventListener('click', () => {
        alertEl.style.animation = 'fadeOut 0.3s forwards';
        setTimeout(() => alertEl.remove(), 300);
    });

    // סגירה אוטומטית אחרי 5 שניות
    setTimeout(() => {
        if (alertEl.parentElement) {
            alertEl.style.animation = 'fadeOut 0.3s forwards';
            setTimeout(() => alertEl.remove(), 300);
        }
    }, 5000);
}

// זיהוי הודעות מהשרת והצגה בפורמט החדש
document.addEventListener('DOMContentLoaded', () => {
    // זיהוי הודעות מהשרת
    const flashMessages = document.querySelectorAll('.flash-message');

    flashMessages.forEach(msg => {
        const type = msg.classList.contains('error') ? 'error' :
                    msg.classList.contains('success') ? 'success' : 'info';

        let title = 'Notification';
        if (type === 'error') title = 'Error';
        if (type === 'success') title = 'Success';

        showAlert(msg.textContent, type, title);
        msg.style.display = 'none'; // הסתרת ההודעה המקורית
    });
});

// הגדרת פונקציה גלובלית להתראות מקומיות
window.showAlert = showAlert;