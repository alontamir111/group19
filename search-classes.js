// search-classes.js
class YogaClass {
    constructor(id, name, level, type, datetime, duration, instructorName, location, maxParticipants, participants = []) {
        this.id = id;
        this.name = name;
        this.level = level;
        this.type = type;
        this.datetime = datetime;
        this.duration = duration;
        this.instructorName = instructorName;
        this.location = location;
        this.maxParticipants = maxParticipants;
        this.participants = participants;
    }
 }
 
 class YogaClassSearch {
    constructor() {
        this.checkAuth();
        this.classes = this.getInitialClasses();
        this.setupEventListeners();
        this.displaySearchResults(this.classes);
        this.populateInstructors(); // הוספת קריאה לפונקציה
    }
 
    checkAuth() {
        const user = JSON.parse(localStorage.getItem('signedInUser'));
        if (!user) {
            window.location.href = 'Login.html';
            return;
        }
        this.user = user;
    }
 
    setupEventListeners() {
        document.querySelector('.search-button').addEventListener('click', () => this.handleSearch());
        document.getElementById('logoutBtn').addEventListener('click', () => this.handleLogout());
    }
 
    getInitialClasses() {
        if (localStorage.getItem('yogaClasses')) {
            return JSON.parse(localStorage.getItem('yogaClasses'));
        }
 
        const currentDate = new Date('2025-01-25');
        const classes = [];
        
        for (let i = 0; i < 30; i++) {
            const date = new Date(currentDate);
            date.setDate(date.getDate() + i);
            
            classes.push(
                new YogaClass(
                    classes.length + 1,
                    "Morning Flow",
                    "beginner",
                    "vinyasa",
                    this.formatDateForClass(date, 7),
                    90,
                    "Sarah Cohen", 
                    "tel-aviv",
                    20
                ),
                new YogaClass(
                    classes.length + 2,
                    "Power Yoga",
                    "advanced", 
                    "power",
                    this.formatDateForClass(date, 9),
                    90,
                    "Danny Levy",
                    "tel-aviv", 
                    15
                ),
                new YogaClass(
                    classes.length + 3,
                    "Gentle Hatha",
                    "beginner",
                    "hatha",
                    this.formatDateForClass(date, 12),
                    60,
                    "Michelle Golan",
                    "tel-aviv",
                    25
                ),
                new YogaClass(
                    classes.length + 4,
                    "Yin Yoga",
                    "all-levels",
                    "yin",
                    this.formatDateForClass(date, 14),
                    75,
                    "Emma Wilson",
                    "tel-aviv",
                    20
                ),
                new YogaClass(
                    classes.length + 5,
                    "Advanced Flow",
                    "intermediate",
                    "vinyasa",
                    this.formatDateForClass(date, 18),
                    75,
                    "Sarah Cohen",
                    "tel-aviv",
                    20
                ),
                new YogaClass(
                    classes.length + 6,
                    "Meditation",
                    "all-levels",
                    "meditation",
                    this.formatDateForClass(date, 20),
                    45,
                    "Michelle Golan",
                    "tel-aviv",
                    30
                )
            );
        }
 
        localStorage.setItem('yogaClasses', JSON.stringify(classes));
        return classes;
    }
 
    formatDateForClass(date, hours) {
        const newDate = new Date(date);
        newDate.setHours(hours, 0, 0, 0);
        return newDate.toISOString();
    }
 
    populateInstructors() {
        const instructors = [
            {id: 1, name: "Sarah Cohen"},
            {id: 2, name: "Danny Levy"},
            {id: 3, name: "Michelle Golan"},
            {id: 4, name: "Emma Wilson"}
        ];
 
        const select = document.getElementById('instructor');
        select.innerHTML = '<option value="">All Instructors</option>';
        instructors.forEach(instructor => {
            const option = document.createElement('option');
            option.value = instructor.name;
            option.textContent = instructor.name;
            select.appendChild(option);
        });
    }
 
    handleSearch() {
        const filters = {
            type: document.getElementById('class-type').value,
            level: document.getElementById('level').value,
            time: document.getElementById('time').value,
            location: document.getElementById('location').value,
            instructor: document.getElementById('instructor').value
        };
 
        const filteredClasses = this.filterClasses(filters);
        this.displaySearchResults(filteredClasses);
    }
 
    filterClasses(filters) {
        return this.classes.filter(yogaClass => {
            const classHour = new Date(yogaClass.datetime).getHours();
            let timeMatch = true;
 
            if (filters.time) {
                const times = {
                    'morning': [6, 12],
                    'afternoon': [12, 17],
                    'evening': [17, 23]
                };
                const [start, end] = times[filters.time];
                timeMatch = classHour >= start && classHour < end;
            }
 
            return (
                (!filters.type || yogaClass.type === filters.type) &&
                (!filters.level || yogaClass.level === filters.level) &&
                (!filters.location || yogaClass.location === filters.location) &&
                (!filters.instructor || yogaClass.instructorName === filters.instructor) &&
                timeMatch
            );
        });
    }
 
    displaySearchResults(classes) {
        const container = document.getElementById('searchResults');
        
        if (classes.length === 0) {
            container.innerHTML = '<div class="no-results">No classes found matching your criteria</div>';
            return;
        }
 
        const sortedClasses = classes.sort((a, b) => new Date(a.datetime) - new Date(b.datetime));
        container.innerHTML = sortedClasses.map(yogaClass => this.createClassCard(yogaClass)).join('');
    }
 
    createClassCard(yogaClass) {
        const isBooked = yogaClass.participants.includes(this.user.email);
        const isFull = yogaClass.participants.length >= yogaClass.maxParticipants;
 
        let buttonHtml;
        if (isBooked) {
            buttonHtml = `<button class="cancel-btn" onclick="yogaClassSearch.cancelClass(${yogaClass.id})">Cancel Booking</button>`;
        } else {
            buttonHtml = `<button class="book-btn" onclick="yogaClassSearch.bookClass(${yogaClass.id})" ${isFull ? 'disabled' : ''}>${isFull ? 'Class Full' : 'Book Now'}</button>`;
        }
 
        return `
            <div class="class-card">
                <div class="class-info">
                    <div class="class-header">
                        <h4>${yogaClass.name}</h4>
                        <span class="level-tag">${this.formatLevel(yogaClass.level)}</span>
                    </div>
                    <div class="class-details">
                        <p><span class="label">Instructor:</span> ${yogaClass.instructorName}</p>
                        <p><span class="label">Time:</span> ${this.formatDateTime(yogaClass.datetime)}</p>
                        <p><span class="label">Duration:</span> ${yogaClass.duration} minutes</p>
                        <p><span class="label">Location:</span> ${this.formatLocation(yogaClass.location)}</p>
                        <p><span class="label">Available Spots:</span> ${yogaClass.maxParticipants - yogaClass.participants.length}</p>
                    </div>
                    <div class="class-description">${this.getClassDescription(yogaClass.type)}</div>
                </div>
                ${buttonHtml}
            </div>
        `;
    }
 
    bookClass(classId) {
        const classToBook = this.classes.find(c => c.id === classId);
        if (!classToBook) return;
 
        if (!classToBook.participants.includes(this.user.email)) {
            classToBook.participants.push(this.user.email);
            localStorage.setItem('yogaClasses', JSON.stringify(this.classes));
            this.handleSearch();
            alert('Class booked successfully!');
        }
    }
 
    cancelClass(classId) {
        const classToCancel = this.classes.find(c => c.id === classId);
        if (!classToCancel) return;
 
        const index = classToCancel.participants.indexOf(this.user.email);
        if (index > -1) {
            classToCancel.participants.splice(index, 1);
            localStorage.setItem('yogaClasses', JSON.stringify(this.classes));
            this.handleSearch();
            alert('Booking cancelled successfully!');
        }
    }
 
    formatLevel(level) {
        const levels = {
            'beginner': 'Beginner',
            'intermediate': 'Intermediate',
            'advanced': 'Advanced',
            'all-levels': 'All Levels'
        };
        return levels[level] || level;
    }
 
    formatDateTime(datetime) {
        return new Date(datetime).toLocaleString('en-US', {
            weekday: 'long',
            month: 'long',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    }
 
    formatLocation(location) {
        return 'Tel Aviv Studio';
    }
 
    getClassDescription(type) {
        const descriptions = {
            'vinyasa': 'Dynamic flow linking breath with movement',
            'hatha': 'Traditional yoga focusing on alignment and breath',
            'power': 'Vigorous practice building strength and flexibility',
            'yin': 'Slow-paced style holding poses for longer periods',
            'meditation': 'Guided meditation and mindfulness practice',
            'prenatal': 'Gentle yoga designed for expectant mothers'
        };
        return descriptions[type] || 'Join us for this amazing yoga class!';
    }
 
    handleLogout() {
        localStorage.removeItem('signedInUser');
        window.location.href = 'Home.html';
    }
 }
 
 let yogaClassSearch;
 window.onload = () => {
    yogaClassSearch = new YogaClassSearch();
 };