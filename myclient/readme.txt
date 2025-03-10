# Professor Rating System

This is a Django-based web application deployed on [PythonAnywhere](https://www.pythonanywhere.com/) at `sc22zy.pythonanywhere.com`. 
The application allows users to register, log in, and rate professors for specific modules. Users can also view average professor ratings and review ratings provided by other students.


## 🌟 **Features**
- User authentication (Registration/Login)
- Rate professors associated with specific modules
- View ratings of all professors
- View average ratings for professors per module


## Admin Login Credentials:
- Domain: http://sc22zy.pythonanywhere.com/admin/
- Username: yangziqing
- Password: yzq20040301

## API Endpoints
- User registration: /rating/register/
- User login (obtain token): /rating/api-token-auth/
- List module instances: /rating/module-instances/
- List professor ratings: /rating/professors/ratings/
- View professor average rating: /rating/professors/<professor_id>/modules/<module_code>/average/
- Create rating: /rating/ratings/

## Usage
Local Testing
1. Run the development server:
python manage.py runserver
2. Navigate to the client directory and execute:
python client.py
3. Use the following URL during local testing:
http://127.0.0.1:8000/

Deployed Testing (PythonAnywhere)
1. Navigate to the client directory and execute:
python client.py
2. Use the deployed domain:
sc22zy.pythonanywhere.com

## Available Commands:

register - Register a new user.
login - Log in with your credentials.
logout - Log out the current user.
list - View all modules and professors.
view - View ratings of all professors.
average - View average rating of a professor in a module.
rate - Rate a professor in a module instance.
exit - Exit the application.
Note: When executing the view and rate commands, ensure that the professor IDs and module codes are entered in uppercase to avoid errors.


## Instructions for Registration/Login
1. Register a User
Send a POST request to /rating/register/ with the following data:
{
    "username": "your_username",
    "email": "your_email@example.com",
    "password": "your_password"
}
2. Login to Obtain Token
Send a POST request to /rating/api-token-auth/ with:
{
    "username": "your_username",
    "password": "your_password"
}

##  Common Issues
1. Database Not Updating
Run the following commands:
python manage.py makemigrations
python manage.py migrate

## Technologies Used
Python 3.10
Django 5.x
Django REST Framework
SQLite (for local development)
PythonAnywhere (for deployment)