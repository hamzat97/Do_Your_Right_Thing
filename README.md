# Do_Your_Right_Thing
Every manager is looking for a better project management because he needs more than task management solved. DYRT project is a web application for managing and supervising the day-to day activities of multiple projects at the same time. This application helps both manager and employee to organize the work be more efficient and productive. It allows the managers to delegate work to his team members, track every task progress, set deadlines and adjust work schedules. On the other hand, employees can through this app access their task list, view detailed task information, report work progress and notify managers of any issues that can arise. 
## Summary
We all know you and your team work on multiple tasks every day! Can you imagine handling all of that with a pen and paper or even an Excel sheet? How crazy and how exhausting that would be?

<p align="center"><img src="https://github.com/hamzat97/Do_Your_Right_Thing/blob/main/Jimmy.gif"></p>

Exactly Jimmy 😄, but no worries cause there is a set of good project management tools and DYRT is one of them. It's a JIRA project management tool that allows users to pull their JIRA issues lists in real time using JIRA REST APIs. The main goal behind it is to always keep the work organized, avoid distractions, prioritize tasks, communicate well, update everyone immediately and strengthen collaboration between team members.   
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
- Log in to your user account ([click here](http://localhost:8000/signin))
- Connect to JIRA Cloud using JIRA REST APIs
- Pull list of JIRA issues reported by you and assigned to you
- Access to your JIRA account where your JIRA issues list should be displayed 
- Log out from your JIRA account
- Log in to user account again and access to your JIRA issues list directly     
## Acknowledgments
Many thanks to Mr. [Vadim Axelrod](https://github.com/vadim1) for giving me the chance to handle your project from scratch, I really feel joyful that your trust in me has come up with a good result. This project was a fruitful collaboration and an opportunity to deal with new issues and gain more experience, I enjoyed working with you [Vadim](https://github.com/vadim1) and I also look forward to collaborating with you in the future.
