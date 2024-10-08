
# Absence_Mananger - Leave Application and Approval System Backend

## Project Description

The Leave Application and Approval System Backend is built with Django and Django REST Framework (DRF) to support the Leave Application and Approval System. This backend service provides secure user authentication, manages leave requests, and enables communication between employees and managers within an organization.

## Table of Contents

- [Key Features](#key-features)
- [Technologies Used](#technologies-used)
- [Installation Instructions](#installation-instructions)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Contributing](#contributing)


## Key Features

- **User Authentication**: Secure login system using JWT for both employees and managers.
- **Leave Application Management**: API endpoints for submitting, reviewing, and managing leave requests.
- **Role-Based Access Control**: Different access levels for employees and managers.
- **Database Management**: PostgreSQL for storing user data and leave applications.

## Technologies Used

- **Backend Framework**: [Django](https://www.djangoproject.com/)
- **REST Framework**: [Django REST Framework (DRF)](https://www.django-rest-framework.org/)
- **Authentication**: [JSON Web Tokens (JWT)](https://jwt.io/)
- **Database**: [PostgreSQL](https://www.postgresql.org/)
- **Environment Management**: [pipenv](https://pipenv.pypa.io/en/latest/)

## Installation Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/KiranBaburaj/Absence_Mananger_Backend.git
   ```

2. Navigate to the project directory:
   ```bash
   cd Absence_Mananger_Backend
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up the PostgreSQL database:
   - Create a new PostgreSQL database and user.
   - Update the database settings in the `settings.py` file.

5. Run database migrations:
   ```bash
   python manage.py migrate
   ```

6. Create a superuser to manage the application:
   ```bash
   python manage.py createsuperuser
   ```

7. Run the development server:
   ```bash
   python manage.py runserver
   ```

8. Access the API at `http://localhost:8000/api/`.

## Configuration

Make sure to configure your `.env` file with the necessary environment variables, such as database credentials and secret keys.

Example `.env` file:
```
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=postgres://user:password@localhost:5432/your_database
```

## Usage

- **For Employees**: Use the API to submit leave requests and view the status of your applications.
- **For Managers**: Use the API to review and approve/reject leave requests submitted by your team.

## API Endpoints

Here are some key API endpoints:

- **Authentication**
  - `POST /api/token/` - Obtain JWT token
  - `POST /api/token/refresh/` - Refresh JWT token

- **Leave Requests**
  - `GET /api/leaves/` - List all leave requests
  - `POST /api/leaves/` - Submit a new leave request
  - `PATCH /api/leaves/{id}/` - Approve or reject a leave request

- **User Management**
  - `GET /api/users/` - List all users (for managers)
  - `POST /api/users/` - Create a new user (for managers)

## Testing

- Ensure all functionalities are tested as per the test cases documented in the `/tests` directory.
- Use the following command to run tests:
  ```bash
  python manage.py test
  ```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/YourFeature`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

