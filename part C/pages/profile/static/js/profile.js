// profile.js - JavaScript for profile page functionality
document.addEventListener('DOMContentLoaded', () => {
    // Handle profile editing
    const editBtn = document.getElementById('editBtn');
    const saveBtn = document.getElementById('saveBtn');
    
    // Input fields
    const nameInput = document.getElementById('nameInput');
    const emailInput = document.getElementById('emailInput');
    const phoneInput = document.getElementById('phoneInput');
    const cityInput = document.getElementById('cityInput');
    
    // Tab elements
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    // Flash messages handling (from server)
    const flashMessages = document.querySelectorAll('.flash-message');
    if (flashMessages.length > 0) {
        // Auto-hide flash messages after 5 seconds
        setTimeout(() => {
            flashMessages.forEach(msg => {
                msg.style.display = 'none';
            });
        }, 5000);
    }

    // Initialize tabs
    if (tabButtons.length > 0) {
        tabButtons.forEach(button => {
            button.addEventListener('click', () => {
                // הסרת הקלאס פעיל מכל הכפתורים
                tabButtons.forEach(btn => btn.classList.remove('active'));
                // הסרת הקלאס פעיל מכל התוכן
                tabContents.forEach(content => content.classList.remove('active'));

                // הוספת הקלאס פעיל לכפתור שנלחץ
                button.classList.add('active');

                // הוספת הקלאס פעיל לתוכן המתאים
                const tabId = button.getAttribute('data-tab');
                document.getElementById(tabId).classList.add('active');
            });
        });
    }

    // Toggle between view and edit modes
    if (editBtn) {
        editBtn.addEventListener('click', () => {
            toggleEditMode(true);
        });
    }

    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            saveChanges();
        });
    }

    // Handle cancel booking buttons
    const cancelButtons = document.querySelectorAll('.cancel-booking-btn');
    cancelButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const bookingId = e.target.getAttribute('data-id');
            cancelBooking(bookingId);
        });
    });

    // Handle delete contact request buttons
    const deleteRequestButtons = document.querySelectorAll('.delete-request-btn');
    deleteRequestButtons.forEach(button => {
        button.addEventListener('click', (e) => {
            const requestId = e.target.getAttribute('data-id');
            deleteContactRequest(requestId);
        });
    });

    // Toggle between view and edit modes
    function toggleEditMode(isEditing) {
        document.querySelectorAll('.info-item span').forEach(s =>
            s.classList.toggle('hidden', isEditing));
        document.querySelectorAll('.edit-input').forEach(i =>
            i.classList.toggle('hidden', !isEditing));

        editBtn.classList.toggle('hidden', isEditing);
        saveBtn.classList.toggle('hidden', !isEditing);
    }

    // Save profile changes via AJAX
    function saveChanges() {
        // Validate inputs before saving
        if (!validateInputs()) {
            if (window.showAlert) {
                showAlert('Please fill in all fields correctly. Phone number in Israeli format and valid email required.', 'error', 'Validation Error');
            } else {
                alert('Please fill in all fields correctly. Phone number in Israeli format and valid email required.');
            }
            return;
        }

        // Create form data to send to server
        const formData = new FormData();
        formData.append('nameInput', nameInput.value);
        formData.append('emailInput', emailInput.value);
        formData.append('phoneInput', phoneInput.value);
        formData.append('cityInput', cityInput.value);

        // Send data to server via AJAX
        fetch('/profile/update', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update displayed information
                document.getElementById('userName').textContent = nameInput.value;
                document.getElementById('userEmail').textContent = emailInput.value;
                document.getElementById('userPhone').textContent = phoneInput.value;
                document.getElementById('userCity').textContent = cityInput.value;

                // Switch back to view mode
                toggleEditMode(false);

                // Show success message
                if (window.showAlert) {
                    showAlert('Profile updated successfully!', 'success', 'Profile Updated');
                } else {
                    alert('Profile updated successfully!');
                }
            } else {
                // Show error message
                if (window.showAlert) {
                    showAlert(data.message || 'Failed to update profile', 'error', 'Update Error');
                } else {
                    alert(data.message || 'Failed to update profile');
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            if (window.showAlert) {
                showAlert('An error occurred while updating profile', 'error', 'Error');
            } else {
                alert('An error occurred while updating profile');
            }
        });
    }

    // Basic validation for profile inputs
    function validateInputs() {
        const name = nameInput.value.trim();
        const email = emailInput.value.trim();
        const phone = phoneInput.value.trim();
        const city = cityInput.value.trim();

        const nameRegex = /^.+ .+$/; // At least first and last name
        const phoneRegex = /^05\d(-?\d{7})$/;
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        return nameRegex.test(name) &&
               emailRegex.test(email) &&
               phoneRegex.test(phone.replace('-', '')) &&
               city.length > 0;
    }

    // Cancel a booking via AJAX
    function cancelBooking(bookingId) {
        // בדיקה אם זה שיעור שעבר
        const card = document.querySelector(`.class-card[data-id="${bookingId}"]`);
        if (!card) return;

        // בדיקה אם השיעור כבר עבר
        const isPast = card.getAttribute('data-is-past') === 'true';

        if (isPast) {
            if (window.showAlert) {
                showAlert('Cannot cancel past classes', 'error', 'Cancellation Error');
            } else {
                alert('Cannot cancel past classes');
            }
            return;
        }

        if (!confirm('Are you sure you want to cancel this booking?')) {
            return;
        }

        const formData = new FormData();
        formData.append('bookingId', bookingId);

        fetch('/profile/cancel-booking', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // הסרת הכרטיס מהתצוגה
                if (card) {
                    card.remove();
                }

                // אם אין יותר שיעורים שהוזמנו, הצגת הודעה
                const bookedClasses = document.getElementById('bookedClasses');
                if (bookedClasses && bookedClasses.querySelectorAll('.class-card').length === 0) {
                    bookedClasses.innerHTML = '<p class="no-classes">No booked classes yet</p>';
                }

                if (window.showAlert) {
                    showAlert('Booking cancelled successfully!', 'success', 'Booking Cancelled');
                } else {
                    alert('Booking cancelled successfully!');
                }
            } else {
                if (window.showAlert) {
                    showAlert(data.message || 'Failed to cancel booking', 'error', 'Cancellation Error');
                } else {
                    alert(data.message || 'Failed to cancel booking');
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            if (window.showAlert) {
                showAlert('An error occurred while cancelling the booking', 'error', 'Error');
            } else {
                alert('An error occurred while cancelling the booking');
            }
        });
    }

    // Delete a contact request via AJAX
    function deleteContactRequest(requestId) {
        if (!confirm('Are you sure you want to delete this contact request?')) {
            return;
        }

        const formData = new FormData();
        formData.append('requestId', requestId);

        fetch('/profile/delete-contact-request', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // הסרת הכרטיס מהתצוגה
                const card = document.querySelector(`.request-card[data-id="${requestId}"]`);
                if (card) {
                    card.remove();
                }

                // אם אין יותר פניות, הצגת הודעה
                const contactRequests = document.getElementById('contactRequests');
                if (contactRequests && contactRequests.querySelectorAll('.request-card').length === 0) {
                    contactRequests.innerHTML = '<p class="no-requests">No contact requests yet</p>';
                }

                if (window.showAlert) {
                    showAlert('Contact request deleted successfully!', 'success', 'Request Deleted');
                } else {
                    alert('Contact request deleted successfully!');
                }
            } else {
                if (window.showAlert) {
                    showAlert(data.message || 'Failed to delete contact request', 'error', 'Deletion Error');
                } else {
                    alert(data.message || 'Failed to delete contact request');
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            if (window.showAlert) {
                showAlert('An error occurred while deleting the contact request', 'error', 'Error');
            } else {
                alert('An error occurred while deleting the contact request');
            }
        });
    }

    // Format phone number as user types
    if (phoneInput) {
        phoneInput.addEventListener('input', function(e) {
            let value = e.target.value.replace(/\D/g, ''); // Remove non-digits

            if (value.length > 3) {
                value = value.substring(0, 3) + '-' + value.substring(3, 10);
            }

            e.target.value = value;
        });
    }
});