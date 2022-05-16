# Do_Your_Right_Thing
Every manager is looking for a better project management because he needs more than task management solved. DYRT project is a web application for managing and supervising the day-to day activities of multiple projects at the same time. This application helps both manager and employee to organize the work be more efficient and productive. It allows the managers to delegate work to his team members, track every task progress, set deadlines and adjust work schedules. On the other hand, employees can through this app access their task list, view detailed task information, report work progress and notify managers of any issues that can arise. 
## Summary
DYRT web application 
## Tech Tools
- Python
- Django
- JIRA REST APIs
- Web Development Languages
## Environment Setup and Installation Requirements
- Install Python and Django
```php
$pip install django
``` 
- Install mysqlclient (fork of MySQL-python) for MySQL lovers
```php
$pip install mysqlclient
``` 
- Install JIRA Python library
```php
$pip install jira
``` 
- Django project configuration (Database & Mail Settings) 
## User Guide
- Open the Django project path in terminal and enter the below two commands:
```php
$python manage.py makemigrations
$python manage.py migrate
``` 
- Run the Django web development server
```php
$python manage.py runserver
```
- Create your user account ([click here](http://localhost:8000/signup))
- Check your Gmail inbox and click on the activation link
- Log in to your account ([click here](http://localhost:8000/signin))
## Acknowledgments
