// searchClasses.js - JavaScript file for the class search page

document.addEventListener('DOMContentLoaded', () => {
    // Get DOM elements
    const searchButton = document.querySelector('.search-button');
    const searchResults = document.getElementById('searchResults');

    // Setup event listeners
    if (searchButton) {
        searchButton.addEventListener('click', handleSearch);
    }

    // Load instructors on page load
    loadInstructors();

    // Function to load instructors from the server
    function loadInstructors() {
        fetch('/searchClasses/api/instructors')
            .then(response => response.json())
            .then(instructors => {
                const select = document.getElementById('instructor');
                select.innerHTML = '<option value="">All Instructors</option>';

                instructors.forEach(instructor => {
                    const option = document.createElement('option');
                    option.value = instructor.name;
                    option.textContent = instructor.name;
                    select.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Error loading instructors:', error);
                // If there's an error, use a static list as backup
                const instructors = [
                    {name: "Sarah Cohen"},
                    {name: "Danny Levy"},
                    {name: "Michelle Golan"},
                    {name: "Emma Wilson"}
                ];

                const select = document.getElementById('instructor');
                select.innerHTML = '<option value="">All Instructors</option>';

                instructors.forEach(instructor => {
                    const option = document.createElement('option');
                    option.value = instructor.name;
                    option.textContent = instructor.name;
                    select.appendChild(option);
                });
            });
    }

    // Function to handle the search
    function handleSearch() {
        // Display loading indicator
        searchResults.innerHTML = '<div class="loading">Loading classes...</div>';

        // Get filter values
        const filters = {
            class_type: document.getElementById('class-type').value,
            level: document.getElementById('level').value,
            time: document.getElementById('time').value,
            location: document.getElementById('location').value,
            instructor: document.getElementById('instructor').value
        };

        // Build query string
        const queryParams = new URLSearchParams();
        for (const key in filters) {
            if (filters[key]) {
                queryParams.append(key, filters[key]);
            }
        }

        // Make API request
        fetch(`/searchClasses/api/classes?${queryParams.toString()}`)
            .then(response => {
                console.log("API Response status:", response.status);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                console.log("API Data:", data);
                displaySearchResults(data);
            })
            .catch(error => {
                console.error('Error fetching classes:', error);
                searchResults.innerHTML = '<div class="error-message">Sorry, there was an error loading classes. Please try again later.</div>';
            });
    }

    // Function to display search results
    function displaySearchResults(classes) {
        if (!classes || classes.length === 0) {
            searchResults.innerHTML = '<div class="no-results">No classes found matching your criteria</div>';
            return;
        }

        const html = classes.map(yogaClass => createClassCard(yogaClass)).join('');
        searchResults.innerHTML = html;

        // Add event listeners to book/cancel buttons
        document.querySelectorAll('.book-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                bookClass(this.dataset.classId);
            });
        });

        document.querySelectorAll('.cancel-btn').forEach(btn => {
            btn.addEventListener('click', function() {
                cancelClass(this.dataset.classId);
            });
        });
    }

    // Function to create class card HTML
    function createClassCard(yogaClass) {
        const isBooked = yogaClass.is_booked || false;
        const isFull = yogaClass.is_full || false;
        const name = yogaClass.name || 'Unknown Class';
        const classType = yogaClass.classType || 'Unknown Type';
        const level = yogaClass.level || 'All Levels';
        const instructorName = yogaClass.instructorName || 'Unknown Instructor';
        const datetime = yogaClass.datetime || 'TBD';
        const duration = yogaClass.duration || 60;
        const location = yogaClass.location || 'Unknown Location';
        const availableSpots = yogaClass.availableSpots || 0;
        const maxParticipants = yogaClass.maxParticipants || 0;
        const price = yogaClass.price || 0;
        const description = yogaClass.description || 'No description available';

        let buttonHtml;
        if (isBooked) {
            buttonHtml = `<button class="cancel-btn" data-class-id="${yogaClass.id}">Cancel Booking</button>`;
        } else {
            buttonHtml = `<button class="book-btn" data-class-id="${yogaClass.id}" ${isFull ? 'disabled' : ''}>${isFull ? 'Class Full' : 'Book Now'}</button>`;
        }

        return `
            <div class="class-card">
                <div class="class-info">
                    <div class="class-header">
                        <h4>${name}</h4>
                        <span class="class-type-tag">${classType}</span>
                        <span class="level-tag">${level}</span>
                    </div>
                    <div class="class-details">
                        <p><span class="label">Instructor:</span> ${instructorName}</p>
                        <p><span class="label">Time:</span> ${datetime}</p>
                        <p><span class="label">Duration:</span> ${duration} minutes</p>
                        <p><span class="label">Location:</span> ${location}</p>
                        <p><span class="label">Available Spots:</span> ${availableSpots} / ${maxParticipants}</p>
                        <p><span class="label">Price:</span> ₪${price}</p>
                    </div>
                    <div class="class-description">${description}</div>
                </div>
                ${buttonHtml}
            </div>
        `;
    }

    // Function to book a class
    function bookClass(classId) {
        const formData = new FormData();
        formData.append('classId', classId);

        fetch('/searchClasses/book', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (window.showAlert) {
                    showAlert('Class booked successfully!', 'success', 'Booking Confirmed');
                } else {
                    alert('Class booked successfully!');
                }
                handleSearch(); // Refresh results
            } else {
                if (window.showAlert) {
                    showAlert(`Booking failed: ${data.message}`, 'error', 'Booking Error');
                } else {
                    alert(`Booking failed: ${data.message}`);
                }
            }
        })
        .catch(error => {
            console.error('Error booking class:', error);
            if (window.showAlert) {
                showAlert('An error occurred while booking the class. Please try again.', 'error', 'Error');
            } else {
                alert('An error occurred while booking the class. Please try again.');
            }
        });
    }

    // Function to cancel a booking
    function cancelClass(classId) {
        const formData = new FormData();
        formData.append('classId', classId);

        fetch('/searchClasses/cancel', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (window.showAlert) {
                    showAlert('Booking cancelled successfully!', 'success', 'Booking Cancelled');
                } else {
                    alert('Booking cancelled successfully!');
                }
                handleSearch(); // Refresh results
            } else {
                if (window.showAlert) {
                    showAlert(`Cancellation failed: ${data.message}`, 'error', 'Cancellation Error');
                } else {
                    alert(`Cancellation failed: ${data.message}`);
                }
            }
        })
        .catch(error => {
            console.error('Error cancelling booking:', error);
            if (window.showAlert) {
                showAlert('An error occurred while cancelling the booking. Please try again.', 'error', 'Error');
            } else {
                alert('An error occurred while cancelling the booking. Please try again.');
            }
        });
    }

    // Trigger search on page load to show initial results
    setTimeout(() => {
        handleSearch();
    }, 500);
});