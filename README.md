

Project : Freelance Marketplace Web Application
------------------------------------------------------------

A production-style Django freelance marketplace platform where customers can book various services and it will be  allocated randomly to one of the service providers such as plumbers, electricians, gardeners, AC technicians, and painters.


The application supports:

* Session Based User Authentication
* Role-based access
* Booking workflow
* Provider assignment
* Real-time chat using Django Channels
* Notifications
* Responsive Bootstrap 5 frontend

------------------------------------------------

# Tech Stack

* Python 3.14
* Django
* Django Channels
* Bootstrap 5
* WebSockets

----------------------------------------------

# Project Setup Steps

## 1. Clone Repository
----------------------------

--bash
git clone https://github.com/KrishnapriyaRishi/mainProject_Freelance_Hub.git


--bash
cd Freelance_Hub_Project


---

## 2. Create Virtual Environment
---------------------------------

### Windows

--bash
python -m venv firstenv


--bash
.\firstenv\scripts\activate


### Linux / macOS

--bash
python3 -m venv firstenv


--bash
source venv/bin/activate


-------------------------------------

## 3. Install Dependencies

--bash
pip install -r requirements.txt


-------------------------------------


## 4. Apply Migrations

--bash
python manage.py makemigrations


--bash
python manage.py migrate


-------------------------------------

## 5. Create Superuser

--bash
python manage.py createsuperuser


--------------------------------------

## 6. Run Development Server

--bash
python manage.py runserver

---------------------------------------

# Admin Login Credentials

Username: Krishna
Password: njimko09


# Application Features
------------------------------------------

* Customer & Provider Authentication
* Session Based Authentication
* Multiple Service Categories
* Random Provider Assignment
* Secure role validation
* Real-time Chat System using Django Channels
* Booking based chat room
* Message persistence
* Notifications
* Ratings & Reviews
* Provider Approval
* Admin Dashboard



# Real-Time Chat Setup
-----------------------------------------

The project uses:

* Django Channels
* Daphne
* WebSockets

Each booking dynamically create a private WebSocket room where only the assigned provider and customer can communicate securely.




