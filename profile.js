document.addEventListener("DOMContentLoaded", () => {
    const user = JSON.parse(localStorage.getItem('signedInUser'));
    if (!user) {
        window.location.href = 'Login.html';
        return;
    }

    displayUserInfo(user);
    setupButtons();
    displayBookedClasses();
    setupLogout();
});

function displayUserInfo(user) {
    document.getElementById('userName').textContent = `${user.firstName} ${user.lastName}`;
    document.getElementById('userEmail').textContent = user.email;
    document.getElementById('userPhone').textContent = user.phoneNumber;
    document.getElementById('userCity').textContent = user.city;
    
    document.getElementById('nameInput').value = `${user.firstName} ${user.lastName}`;
    document.getElementById('emailInput').value = user.email;
    document.getElementById('phoneInput').value = user.phoneNumber;
    document.getElementById('cityInput').value = user.city;
}

function setupButtons() {
    document.getElementById('editBtn').onclick = () => toggleEditMode(true);
    document.getElementById('saveBtn').onclick = saveChanges;
}

function saveChanges() {
    const [firstName, lastName] = document.getElementById('nameInput').value.split(' ');
    const email = document.getElementById('emailInput').value;
    const phoneNumber = document.getElementById('phoneInput').value;
    const city = document.getElementById('cityInput').value;

    if (!validateInputs(firstName, lastName, email, phoneNumber, city)) {
        alert('Please fill in all fields correctly. Phone number in Israeli format and valid email required.');
        return;
    }

    const user = JSON.parse(localStorage.getItem('signedInUser'));
    const users = JSON.parse(localStorage.getItem('registeredUsers'));
    
    // Check if email already exists for a different user
    const emailExists = users.some(u => u.email === email && u.email !== user.email);
    if (emailExists) {
        alert('This email is already registered');
        return;
    }

    const updatedUser = {...user, firstName, lastName, email, phoneNumber, city};
    const userIndex = users.findIndex(u => u.email === user.email);
    users[userIndex] = updatedUser;

    localStorage.setItem('registeredUsers', JSON.stringify(users));
    localStorage.setItem('signedInUser', JSON.stringify(updatedUser));

    displayUserInfo(updatedUser);
    toggleEditMode(false);
}

function validateInputs(firstName, lastName, email, phone, city) {
    const phoneRegex = /^05\d-?\d{7}$/;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return firstName?.trim() && 
           lastName?.trim() && 
           emailRegex.test(email) &&
           phoneRegex.test(phone.replace('-', '')) &&
           city?.trim();
}

function toggleEditMode(isEditing) {
    document.querySelectorAll('.info-item span').forEach(s => 
        s.classList.toggle('hidden', isEditing));
    document.querySelectorAll('.edit-input').forEach(i => 
        i.classList.toggle('hidden', !isEditing));
    document.getElementById('editBtn').classList.toggle('hidden', isEditing);
    document.getElementById('saveBtn').classList.toggle('hidden', !isEditing);
}

function displayBookedClasses() {
    const container = document.getElementById('bookedClasses');
    if (!container) return;

    const classes = JSON.parse(localStorage.getItem('yogaClasses')) || [];
    const userEmail = JSON.parse(localStorage.getItem('signedInUser')).email;
    
    const userClasses = classes.filter(c => 
        c.participants && c.participants.includes(userEmail)
    );
    
    if (userClasses.length === 0) {
        container.innerHTML = '<p class="no-classes">No booked classes yet</p>';
        return;
    }

    container.innerHTML = userClasses.map(c => `
        <div class="class-card">
            <h3>${c.name}</h3>
            <div class="class-details">
                <p><span class="label">Date:</span> ${new Date(c.datetime).toLocaleDateString()}</p>
                <p><span class="label">Time:</span> ${new Date(c.datetime).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</p>
                <p><span class="label">Location:</span> ${formatLocation(c.location)}</p>
                <p><span class="label">Instructor:</span> ${c.instructorName}</p>
                <p><span class="label">Duration:</span> ${c.duration} minutes</p>
            </div>
        </div>
    `).join('');
}

function formatLocation(location) {
    return location === 'tel-aviv' ? 'Tel Aviv Studio' : location;
}

function setupLogout() {
    document.getElementById('logoutBtn')?.addEventListener('click', (e) => {
        e.preventDefault();
        localStorage.removeItem('signedInUser');
        window.location.href = 'Home.html';
    });
}