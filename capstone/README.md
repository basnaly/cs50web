# PET CLINIC

Video Demo:

# Description

My Pet Clinic application is intended to register a pet/s, to sign up for an appointment to the vet, make the insurance for the pet, see last vaccinations and get the notifcations about appointments to the vet.

# Introduction

My Pet Clinic app allows to manage pet health needs is about the most important things to vet care of pets. It helps to organaze, remind and get access to data about users' pets.

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
8.  I developed custom 404 page.
9.  My tests tests all the pages when user is logged in.

# Project files

# How to run
