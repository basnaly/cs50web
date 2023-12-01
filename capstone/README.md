# PET CLINIC

Video Demo:

# Description

My Pet Clinic application is intended to register a pet/s, to sign up for an appointment to the vet, make the insurance for the pet, see last vaccinations and get the notifcations about appointments to the vet.

# Introduction

My Pet Clinic app is about pet care management. The app for pet owners and pet clinic staff. It simplifies pet care management like scheduling vet visits, registering for vaccinations, managing insurance, user and pet registration and etc.

# Authentication

Every user can register in the app, login and logout. It allows user to save his profile and after registration also to change it in 'My profile' page.

During user registration he must choose his identical number, first name, last name, phone number and email. Also user must type password confirmation. After registration finishes the app will add the new user to the sqlite3 database.

After user registered or logged into the app he can see greeting in the right upper corner. To do this, I get the name of the user from the database by user id.

# Application Data

All data is stored in the db.sqlite3.

There are 5 tables in the database: user, pet, insurance, visit, vaccination. Every user is a row in the user table and pet is a row in the pet table.

Each table is defined in model.py file.

# Application Features

The Pet Clinic app has 5 main features that are represented by options in the nav bar: "Visit Us", "Vaccination", "Insurance", "Register Pet", "Notification". Also the app has 2 features in the user dropown - user and profile of each of his registered pets.

## Main features

### 1\. Visit Us

Here user can select:

- his pet that needs vet care
- the reason of visit from 3 options: illness, vaccination, consulting
- the date of visit

After clicking on the button "Show me the times", it will send a request for the possible times on this date. The times are appear and the busy times will be show as disabled. The user cannot select the dates in the past and weekends. Inpython code i also check that the selected pet already has an appointment and display the corresponding message.

User can click on the button "Submit my visit". After that the user will get the message that appointment was created. Also user have another option - reset selected date by clickin on the "Reset" button.

### 2\. Vaccination

When user comes with his pet to the vet according to the appointment, vet examines the pet and applies the vaccination to the pet. After that the vet logs in into the django administration panel using pet clinic account and document the details of the vaccination.

So user can see the data of vaccination of all his pets in his account by clicking on "Vaccination" tab. The data is displyed in the table and includes pet name, date of vaccination and next vaccination. However the vet fills in addition the fields like details and his name  that can be seen in the administration panel.

If user have pet/s that still didn't have the vaccinations, his/their nicknames will be also displayed on this page.

### 3.Insurance

In page "Insurance" user selects one of his pets.

If user already has an insurence for the selected pet, user gets the corresponding message with details when the insurance starts and it's monthly price.

If not the form appears and user can select start date of the insurance. Depends on the user's pet, monthly price is displayed. When user submits the form, he gets the message: "We've got your request. We'll call back you during 1 work day."

### 4\. Register Pet

The user can register his pet on the add pet page.In order to do this he must select the icon for his pet from 16 different animal icons, fill the nickname of his pet, pet type (cat, dog and etc.), select pet's birthdate. User can type some information about his pet in the details field but it is not required.

If user didn't fill one of the mandatory fields and clicks on "Submit" button, he gets the message "Please fill all the fields!"

If all the mandatory fields were filled, user gets the message that the pet was added.

### 5\. Notification

If user has appointments to visit vet with his pet, he can see it in the notification page as a message with appointment details. User gets notifications for all his pets.

If user doesn't have any appointments yet, he will get the corresponding message.

## User dropdown features

### 1\. User profile

When the user logged in he can see in the right upper corner user dropdown. When user clicks on it he can see greeting with his first name and link to "My profile".

By clicking on this link user can change his profile data saved during register excluding the identical number.

### 2\. Pet profile

Bellow "My profile" link in the dropdown there are links of all pets of the user (if there are some). User can click on the pet's nickname to change the information filled during the registration of the pet. User can change icon, birth date and details field.

User can also delete his pet by clickin on "Delete pet" button.

# Distinctiveness and Complexity

My Pet Clinic app differs from all other applications that we built during the course:

1.  I developed an additional registration for user's pets.
2.  I have date validation. In some places user is not allowed to provide past date and in some future dates.
3.  I have weekend check to avoid user scheduling an appointment to the weekend days.
4.  Schedule visit is done in 2 steps. First, user selects date and I calculate the available time slots for that day. Second, user selects the desired time slot and applies for the visit.
5.  Security: On every request for pet I validate that the requested user is indeed the owner of this pet.
6.  I developed the user dropdown menu where user can access his profile and profile of all his pets. I send request in JavaScript to get the list of pets in this dropdown.
7.  The vet manager is intended to fill the data using admin panel of Django.
8.  All the deletion in my app use modal dialog to avoid accidental click on the delete button.
9.  I developed custom 404 page.
10. My tests tests all the pages when user is logged in.

# Project files

## Static folder

In static folder I put image files and index.js file. In index.js file I have 3 functions: Two first functions are intended to create an appoinment to a vet.

- First. When user select the pet, the type visit and the date visit, the function sends the request to python to check what time slot is available and after getting the response it displays the all time slot. Some of them might not be available because  someone has ordered it before and some are avilable to select.
- Second. After user selected the time slot and clicked on the "Submit" button, the function sends request to python to create the visit and save it to the db.
- Third. Last function allows to reset selected fields.

## Templates/petclinic folder

In this folder I created a bunch of HTML templates to display corresponding data and information:

- 404.html. This ipage is displayed when there is some error and the message is passed from python.
- add_pet.html, displayed on "/add_pet url". In this page there is a form and submit button to register a new pet. Also I added some JavaScript function to hide the message after 3 sec and after that to show user the clean page to register another pet.
- index.html, displayed on "/" url. If the user logged in on this page there is a form to make an appoinment to the vet and also 2 buttons: submit and reset. If the user isn't logged in, it displays some general information and gives links to log in and register.
- insuranse.html, displayed on "/insuranse" url.  There is a selection button here to select the pet of the user. After the user selects his pet he gets information about insurance for this pet. If this pet already has the insurance, it will be displayed on the page "/pet_insurance/pet_id".
- layout.html. This page is intended to the whole app. There are header, footer, nav bar and body. If the user is authenticated it displays all navbar links except log in and regester links. Also this template has a JavaScript function that sends a request to python to get the list of pets of the user (if he has some) and displays them in the user profile dropdown as links. If user is not logged in, there are only 5 links in the nav bar: "Visit Us", "Vaccination", "Insurance", "Log In", "Register" and the same general information on the 3 first links.
- login.html, displayed on "/login" url. There is a form and "Login" button that allows user log into the app.
- notification.html, displayed on "/notification" url. There are notification messages that user has an appointments with his pet/s to the vet. Also user can cancel his visit by clicking on the "Cancel visit" button. There is a JavaScript function that sends to python request to delete the visit from db and when it gets the response it displays the appropriate message for 3 sec and then reloads this page.
- pet_insurance.html, displayed on "/pet_insurance/pet_id" url. Allows user to order the insurance fof his pet by filling the form. If user already has the insurance for this pet, it displays the details of insurance on the page. After submitting the pet insurance request the message is displayed for 3 sec and then removed by JavaScript function.
- pet_profile.html, displayed on "/pet_profile/pet_id" url. There is a form of the pet data that user filled during registration of his pet. The user can change all the fields except the nickname and type of his pet. Also in the form there are 2 buttons: save the changed data and delete the pet. The deletion is performed using modal dialog to avoid accidental removal of the pet. There is a JavaScript function that sends to python request to delete the pet from db and when it gets the response it sends the appropriate message. This message is removed after 3 sec and the user is redirected to the index page.
- profile.html, displayed on "/profile" url. There is a form of the user data that user filled during the registration. The user can change all the fields except identical number, there is "Save" button that saves the changes. There is a JavaScript function that removes a message after 3 sec.
- register.html, displayed on "/register" url. There is a form that consists of an identical number, first name, last name, phone number, email, password, confirmation and "Register" button that allows user to register into the app.
- show_vaccination.html, displayed on "/show_vaccination" url. All the pets with the vacccinations will be shown in the table with some details. The others will be shown below.  Also each pet's nickname has a link that leads to his pet profile page.

## Tests

I developed 2 classes of tests:

1.  PetclinicTestCase. In this class I test my models
2.  PetclinicUITestCase. In this case I test html pages, their context for logged in user.

# How to run

### To run Pet Clinic app:

1.  Install python3 and django.
2.  In cmd run `python3 manage.py makemigrations`
3.  In cmd run `python3 manage.py migrate`
4.  In cmd run `python3 manage.py runserver`
5.  In browser navigate to: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

### To create pet clinic administration account:

1.  In cmd run `python3 manage.py createsuperuser`
2.  Follow instructions on the screen
3.  In browser navigate to: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)
