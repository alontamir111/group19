# The Yoga Spot - Yoga Studio Management Website
## WEB course 2024 - Part C

## Project Overview

"The Yoga Spot" is a website designed for a yoga studio that allows users to register, search for yoga classes based on various criteria, book places in classes, and manage their personal profiles. The website aims to improve the user experience for yoga practitioners and enable them to manage their yoga activities easily and conveniently.

The project includes a full implementation of the server side using Flask and MongoDB, addressing all requirements: proper directory structure, client request handling, database connection and queries, form implementation, and a complete user experience.

## Website Workflow

Here is the typical sequence of actions for a user on the website:

1. **Visit the Homepage** - The user arrives at the homepage and is exposed to information about the studio and navigation options.
2. **Register/Login** - A new user registers or an existing user logs in.
3. **Search for Classes** - The user searches for suitable yoga classes using various filters.
4. **Book a Class** - Selection of an appropriate class and booking a spot.
5. **Profile Management** - View and update personal details, view existing bookings and cancel future bookings if necessary.
6. **Send Inquiries** - Use the "Contact Us" form for inquiries and questions.
7. **View Additional Information** - Browse information pages such as class types, studio locations, and more.
8. **Logout** - Exit the system and return to the homepage.

## Website Pages and Functionality

### Homepage
The homepage displays general information about the studio, atmosphere images, and an introduction to the experience offered by the studio. The page includes quick links to different sections of the website.

![HomePage1.jpg](static/media/README_img/HomePage1.jpg)

### Registration Page
Allows new users to register with their personal details. The form includes validation and requires acceptance of the terms of use and privacy policy through a popup window, allowing the user to read the terms before approval.

![Register.jpg](static/media/README_img/Register.jpg)
![Terms.jpg](static/media/README_img/Terms.jpg)

### Login Page
Allows registered users to log in to their account using email and password.

![SignIn.jpg](static/media/README_img/SignIn.jpg)

### Class Search Page
A central page that allows users to search for classes based on a variety of criteria: class type, level, time, location, and instructor. Results are displayed in a convenient format and allow for easy booking.

![FindClass.jpg](static/media/README_img/FindClass.jpg)

### Profile Page
Displays the user's personal details, allows editing them, and includes a list of their class bookings. Users can view their history and cancel future bookings. Additionally, users can view all inquiries made through the "Contact Us" form and delete previous inquiries.

![Profile1.png](static/media/README_img/Profile1.png)
![Profile-Classes.png](static/media/README_img/Profile-Classes.png)
![Profile-Edit.png](static/media/README_img/Profile-Edit.png)

### Contact Us Page
Allows users to send messages and questions to the studio through a contact form. Inquiries are saved in the system and can be viewed through the profile page.

![ContactUs.jpg](static/media/README_img/ContactUs.jpg)

### Class Types Page
Displays detailed information about all types of classes offered at the studio, including description, difficulty levels, benefits, and images.

![OurClasses1.png](static/media/README_img/OurClasses1.png)
![OurClasses2.png](static/media/README_img/OurClasses2.png)

### Studio Page
Displays the various studio locations, including addresses, contact details, maps, and operating hours.

![Studios.jpg](static/media/README_img/Studios.jpg)
![Studios2.png](static/media/README_img/Studios2.png)

### About Page
Provides information about the studio, its history, instructors, and the philosophy that guides it.

![About.png](static/media/README_img/About.png)

### Logout
Allows users to safely log out of the system and return to the homepage.

![Signout.png](static/media/README_img/Signout.png)

## Technical Implementation

The website was developed in a Python/Flask environment with support for:
- Responsive design using HTML5, CSS3, and JavaScript
- MongoDB database for storing information about users, classes, and bookings
- Server-side authentication and validation for information security
- Support for profile image uploads
- Use of templates for displaying dynamic content