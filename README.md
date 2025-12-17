# Hospital Management System

This is a demo-friendly Hospital Management web application built with Django. It showcases a complete appointment booking workflow, including doctor and patient registration, availability management, and email notifications.

## Project Status

This project is a demonstration application. It is not intended for production use in its current state but serves as a strong example of a Django-based web application with external service integrations.

## Features

### For Patients
- **Sign Up & Login:** Patients can create their own accounts and log in.
- **View Doctors:** Browse a list of available doctors.
- **Book Appointments:** Select a doctor and book an available time slot.
- **Receive Email Confirmations:** Get an email notification upon successful booking.

### For Doctors
- **Sign Up & Login:** Doctors can create their own accounts and log in.
- **Manage Availability:** Doctors can add, view, and delete their available time slots for appointments.
- **Receive Email Confirmations:** Get an email notification when a patient books an appointment.

### Technical Features
- **Race-Condition-Safe Booking:** The booking process uses database-level locking (`select_for_update`) to prevent double-booking of the same time slot.
- **Google Calendar Integration:** Stubs are in place to create Google Calendar events for both the doctor and the patient when a booking is made.
- **Serverless Email Notifications:** A separate, serverless function (designed for AWS Lambda) handles sending email notifications.

## Application Architecture

The application follows a standard Django architecture:

- **`hospital_mgmt`:** The main Django project directory.
- **`accounts`:** Manages user registration (for both doctors and patients) and authentication.
- **`doctors`:** Handles doctor-specific functionality, such as managing availability.
- **`bookings`:** Manages the appointment booking process.
- **`integrations`:** Contains modules for interacting with external services like Google Calendar.
- **`email_service`:** A separate serverless application for sending emails.

## Tech Stack

- **Backend:** Django
- **Database:** PostgreSQL
- **Email Service:** Python with AWS Lambda (using the Serverless Framework)
- **Frontend:** Django Templates with basic CSS

## Local Setup

### 1. Prerequisites
- Python 3.x
- PostgreSQL
- Node.js and npm (for the serverless email service)

### 2. Django Application Setup

1.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```

2.  **Install Python dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Configure environment variables:**
    Create a `.env` file in the project root. You can use the following as a template:
    ```env
    DEBUG=True
    SECRET_KEY=a-secure-secret-key-for-your-project

    # Database Settings
    DB_NAME=hospital_db
    DB_USER=postgres
    DB_PASSWORD=your_db_password
    DB_HOST=127.0.0.1
    DB_PORT=5432

    # Google OAuth Settings (Optional)
    GOOGLE_CLIENT_ID=your-google-oauth-client-id
    GOOGLE_CLIENT_SECRET=your-google-oauth-client-secret
    GOOGLE_REDIRECT_URI=http://localhost:8000/integrations/google/oauth2/callback/

    # Email Service URL
    EMAIL_LAMBDA_URL=http://localhost:3000/dev/email
    ```

4.  **Set up the database:**
    Ensure your PostgreSQL server is running. Then, run the migrations to create the database schema:
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

5.  **Create a superuser (optional):**
    This allows you to access the Django admin interface.
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The application will be available at `http://127.0.0.1:8000`.


### 3. Serverless Email Service Setup

1.  **Navigate to the `email_service` directory:**
    ```bash
    cd email_service
    ```

2.  **Install Node.js dependencies:**
    ```bash
    npm install -g serverless
    ```
    
3. **Install Python dependencies for the service**
   ```bash
   pip install -r requirements.txt
   ```
4.  **Configure SMTP environment variables:**
    Create a `.env` file inside the `email_service` directory with your SMTP credentials. For example, for Gmail, you would need an "App Password".
    ```env
    SMTP_HOST=smtp.gmail.com
    SMTP_PORT=587
    SMTP_USER=your-email@example.com
    SMTP_PASSWORD=your-app-password
    FROM_EMAIL=your-email@example.com
    ```

5.  **Run the service locally:**
    ```bash
    serverless plugin install -n serverless-offline
    serverless offline
    ```
    This will start a local server, typically at `http://localhost:3000`, that simulates the AWS Lambda environment.

## Workflows

### Doctor Workflow
1.  Sign up for a new doctor account.
2.  Log in to the doctor dashboard.
3.  Navigate to "My Availability".
4.  Add new time slots for when you are available to take appointments.

### Patient Workflow
1.  Sign up for a new patient account.
2.  Log in to the patient dashboard.
3.  Click on "Book Appointment".
4.  Choose a doctor from the list.
5.  Select an available time slot and confirm the booking.
6.  You will receive an email confirmation for your appointment.