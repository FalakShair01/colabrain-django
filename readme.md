# Colabrain API - Readme

Welcome to the Colabrain API! This repository contains the code for an API that provides various functionalities related to user management in the organization app. Below, you'll find a setup guide and API endpoint guide to get you started.

## Setup Guide

### Step 1: Clone the Repository

If you have Git installed, open a terminal or command prompt and run:

```
git clone <repository_url.git>
cd <repository_name>
```

Replace `<repository_url.git>` and `<repository_name>` with the actual URL and name of your GitHub repository.

### Step 2: Create a Virtual Environment

Create a virtual environment to isolate the project's dependencies:

```
python -m venv env
```

### Step 3: Activate the Virtual Environment

Activate the virtual environment:

On Windows:

```
env\Scripts\activate
```

On macOS and Linux:

```
source env/bin/activate
```

### Step 4: Install Dependencies

Install the required dependencies using `pip`:

```
pip install -r requirements.txt
```

### Step 5: Database Migration

Apply the initial database migrations:

```
python manage.py migrate
```

### Step 6: Run the Development Server

Start the Django development server:

```
python manage.py runserver
```

The development server should now be running locally at `http://127.0.0.1:8000/`.
The deployment server is running at `http://falak.pythonanywhere.com/
`

## API Endpoint Guide

### Authentication

#### Login User

- Endpoint: `/api/token/`
- Method: POST
- Body:
  ```json
  {
    "email": "falak@gmail.com",
    "password": "123"
  }
  ```
- Response: On successful login, you will receive both an access token and a refresh token.

#### Refresh Token

- Endpoint: `/api/token/refresh/`
- Method: POST
- Body:
  ```json
  {
    "refresh": "<your_refresh_token>"
  }
  ```
- Response: You will receive a new access token.

#### Register User

- Endpoint: `/api/register/`
- Method: POST
- Body:
  ```json
  {
    "user": {
      "username": "falak",
      "email": "falak@gmail.com",
      "password": "123"
    },
    "company_name": "colabrain",
    "phone": "12345"
  }
  ```
- Response: New user will be registered with the provided details.

### User Profile

#### Profile View

- Endpoint: `/api/company-profile/`
- Method: GET
- Description: Make a GET request to view user data.

#### Profile Edit

- Endpoint: `/api/company-profile/`
- Method: PATCH
- Description: Make a PATCH request to edit user data.
- Body:
  ```json
  {
    "user": {
      "email": "falak@gmail.com",
      "username": "falak"
    },
    "company_name": "colabrain",
    "country": "pakistan",
    "phone": "12345",
    "role": "organization",
    "profile_pic": null
  }
  ```

### Change Password

- Endpoint: `/api/change-password/`
- Method: POST
- Body:
  ```json
  {
    "old_password": "12345",
    "new_password": "1234",
    "confirm_password": "1234"
  }
  ```
- Response: Password will be changed if the old password matches and the new password is confirmed.

### Token Usage

To access protected endpoints, pass the access token in the Authorization header as follows:

```
Authorization: Bearer <your_access_token>
```

Make sure to replace `<your_access_token>` with the actual access token obtained after successful login or token refresh.

Feel free to use these endpoints to interact with the Colabrain API. If you encounter any issues or have questions, please don't hesitate to reach out to us. Happy coding!