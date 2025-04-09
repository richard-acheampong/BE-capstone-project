Residency Management API
A backend system built using Django and Django REST Framework (DRF) to manage church planting residency cohorts. This project handles user roles, cohort management, resident management, and generates reports for administrators and coaches.

Features
User Authentication: Custom user model with different roles (admin, coordinator, coach, resident).

Cohort Management: Create and manage cohorts, assign coordinators, and associate residents with cohorts.

Resident Management: Register residents, assign coaches, and track details like sending church and plant location.

Reporting: Generate cohort summary and coach-resident reports.

Technologies Used
Django: Web framework for Python.
Django REST Framework: For creating RESTful APIs.
MySQL: Database for storing all application data.
Gunicorn: WSGI HTTP server for running the app in production.

Requirements
Python 3.8+
MySQL
Virtual environment (recommended)# BE-capstone-project

Installation
Step 1: Clone the repository
git clone <repository_url>
cd <repository_name>

Step 2: Create a virtual environment
python -m venv venv

Step 3: Activate the virtual environment
venv\Scripts\activate

Step 4: Install dependencies
pip install -r requirements.txt

Step 5: Configure the database
Ensure MySQL is installed and running. Then create a database for the project.
mysql -u root -p
CREATE DATABASE residency_management;
Update the DATABASES settings in residency_project/settings.py with your MySQL credentials

Step 6: Run migrations
python manage.py migrate

Step 7: Create a superuser
python manage.py createsuperuser

Step 8: Run the development server
python manage.py runserver
Visit http://127.0.0.1:8000 in your browser.

API Endpoints
User Authentication
POST /residency/register/: Register a new user.

POST /residency/login/: Log in and get a token for authentication.

Cohort Management
GET /residency/cohorts/: Retrieve all cohorts.

POST /residency/cohorts/: Create a new cohort.

GET /residency/cohorts/<id>/: Retrieve a specific cohort.

Resident Management
GET /residency/residents/: Retrieve all residents.

POST /residency/residents/: Register a new resident.

GET /residency/residents/<id>/: Retrieve a specific resident.

Reporting
GET /reports/cohorts/: Get a summary of cohort sizes.

GET /reports/coaches/: List residents assigned to each coach.

Running Tests
python manage.py test

Contributing
Feel free to fork the repository and submit pull requests for any bug fixes or features. Make sure to follow the code style and run tests before submitting changes.

License
This project is licensed under the MIT License – see the LICENSE file for details.