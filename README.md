# Professor Rating System

This is a Django-based web application designed to allow users to register, log in, and rate professors for specific modules. Users can also view average professor ratings and review ratings provided by other students.

## Features

- User authentication (Registration/Login)
- Rate professors associated with specific modules
- View ratings of all professors
- View average ratings for professors per module

## Project Structure

- `client/`: Contains client-side scripts for interacting with the API.
- `professor_rating/`: Django project settings and configurations.
- `rating_app/`: Contains the main application logic, including models, views, serializers, and API endpoints.

## Technology Stack

- **Backend:** Django, Django REST Framework
- **Frontend (Client scripts):** Python (using `requests` library)

## Installation

1. Clone this repository:

```bash
git clone <repository-url>
cd professor_rating
```

2. Create a virtual environment and activate it:

```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up the database and apply migrations:

```bash
python manage.py makemigrations
python manage.py migrate
```

5. Run the server:

```bash
python manage.py runserver
```

## API Endpoints

- User registration: `/register/`
- User login (obtain token): `/api-token-auth/`
- List module instances: `/module-instances/`
- List professor ratings: `/professors/ratings/`
- View professor average rating: `/professors/<professor_id>/modules/<module_code>/average/`
- Create rating: `/ratings/`

## Usage (Client Scripts)

Navigate to the `client` directory and execute:

```bash
python client.py
```

Follow the command-line prompts to perform desired actions. You can use the following commands:

```
1. register - Register a new user
2. login - Log in with your credentials
3. logout - Log out the current user
4. list - View all modules and professors
5. view - View ratings of all professors
6. average - View average rating of a professor in a module
7. rate - Rate a professor in a module instance
8. exit - Exit the application
```

## Deployment

The project can be deployed easily on platforms like PythonAnywhere, Heroku, or other Django-compatible hosting services.
