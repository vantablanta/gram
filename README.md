# gram
>Developed by [Michelle-Njeri](https://github.com/vantablanta)  
  
## Description  
>An application where a user can sign into it, upload pictures, see their profile with all pictures they uploaded. Follow other users and see their pictures. Like a picture and leave a comment on it.

##  Live Link  
>[View Site]()  to visit the site
  

## User Story  
  
* Sign in to the application to start using.
* Upload my pictures to the application.
* See my profile with all my pictures.
* Follow other users and see their pictures on my timeline.
* Like a picture and leave a comment on it.
    
## Setup and Installation  
To get the project .......  
  
##### Cloning the repository:  
```bash 
 https://github.com/vantablanta/gram.git
```
##### Navigate into the folder
 ```bash 
cd project-gram
```
##### Install and activate Virtual  
 ```bash 
pipenv shell 
```  
##### Install Dependencies  
 ```bash 
 pipenv sync
```  
 ##### Setup Database  
  SetUp your database User,Password, Host then make migrate  
 ```bash 
python manage.py makemigrations gram_app
 ``` 
 Now Migrate  
 ```bash 
 python manage.py migrate 
```
##### Run the application  
 ```bash 
 python manage.py runserver 
``` 
##### Testing the application  
 ```bash 
 python manage.py test 
```
Open the application on your browser `127.0.0.1:8000`.  
  
## Technology used  
  
* [Python3.8](https://www.python.org/)  
* [Django 4.0](https://docs.djangoproject.com/en/2.2/)  
* [Heroku](https://heroku.com)  
  
  
## Known Bugs  
* There are no known bugs currently but pull requests are allowed incase you spot a bug  
  
## Contact Information   
If you have any question or contributions, please email me at [vantablanta@gmail.com]  
  
## License 

[![License](https://img.shields.io/packagist/l/loopline-systems/closeio-api-wrapper.svg)](https://github.com/vantablanta/gram/blob/master/LICENSE)  
>Copyright (c) 2022 **Michelle Njeri**