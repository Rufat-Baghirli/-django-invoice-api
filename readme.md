Django Invoice Generator API
A robust backend API for asynchronously generating and emailing PDF invoices. This project showcases advanced Django concepts including background task processing with Celery, secure file handling, and professional API development with Django REST Framework.

Key Features
Asynchronous PDF Generation: PDF invoices are created in the background using Celery and Redis, ensuring a fast API response time for the user.

Automated Email Delivery: Generated invoices are automatically sent to the client's email address as an attachment, also handled by a Celery background task.

Secure, Token-Based Downloads: Each invoice has a unique, secure download link that uses a token for one-time or controlled access.

JWT Authentication: The API is secured using JSON Web Tokens, ensuring that only authenticated users can manage their invoices.

Per-User Data Isolation: Users can only view and manage the invoices they have created.

Technology Stack
Backend: Python, Django, Django REST Framework

Asynchronous Tasks: Celery, Redis

PDF Generation: ReportLab

Authentication: DRF Simple JWT (JSON Web Token)
- Database: SQLite3 (for development), PostgreSQL (recommended for production)

API Endpoints

Method

Endpoint

Description

Auth Required?

GET

/api/invoices/

Returns a list of the authenticated user's invoices.

Yes

POST

/api/invoices/

Creates a new invoice and triggers background tasks.

Yes

GET

/api/invoices/{invoice_id}/

Retrieves a specific invoice.

Yes (Owner only)

GET

/api/invoices/{invoice_id}/download/?token={token}

Downloads the generated PDF file using a secure token.

No (Token auth)

POST

/api/token/

Obtains a new token pair (access and refresh).

No

POST

/api/token/refresh/

Refreshes an access token.

No



Local Setup and Installation
Prerequisites
Python 3.8+

Redis Server

Running the Application
Clone the repository:

Bash

git clone https://github.com/your-username/django-invoice-api.git
cd django-invoice-api
Create and activate a virtual environment:

Bash

# For Windows:
python -m venv venv
.\venv\Scripts\Activate.ps1

# For macOS/Linux:
python3 -m venv venv
source venv/bin/activate
Install the required packages:

Bash

pip install -r requirements.txt
Set up the .env file:
Create a .env file in the root directory and fill it with your configuration (SECRET_KEY, DEBUG, email settings, etc.).

Apply the database migrations:

Bash

python manage.py migrate
Run all services (You will need 3 separate terminals):

Terminal 1: Start Redis Server (if not already running as a service)

Bash

redis-server
Terminal 2: Start the Celery Worker

Bash

# Make sure your venv is activated
celery -A autoinvoice_generator worker -l info -P eventlet
Terminal 3: Start the Django Development Server

Bash

# Make sure your venv is activated
python manage.py runserver
The project is now running at http://127.0.0.1:8000/.

License
This project is licensed under the MIT License.