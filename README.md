# NewGym
> Log your gym workouts and track your progress using data visualization.
> https://new-gym.onrender.com/.

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)


## General Information
New Gym is my final project for Coderslab Python Developer Bootcamp. It has all functionalities of a commercial workout tracker application. The database, backend and frontend is my original design. The project reflects my passion for strength training and showcase my data analysis skillset.

Feel free to register as a new user and track your own workouts or login as a preview user with just one click. Please bear in mind that the application and database is hosted on render, a free hosting platform and it can take a few seconds to perform an action.


## Technologies Used
- Django 4.1.4 - web framework
- PostreSQL - database
- Bootstrap 5 / MD Bootstrap - frontend library
- Javascript ES6 - frontend engeneering
- Charts JS - data visualization


## Features
- Exercises
The exercises menu lets you easily filter through the exercise database based on the equipment you have, muscle you want to train or just by typing the name of the exercise. You can also add you own exercises!
- Templates
You can use one of the built-in workout templates or create your own. Before your workout pick a template and if you have previously used it, the app will automatically upload the last workout data into the form, so you can easily progress
- Analytics
The analytics dashboard lets you easily track your progress. The dynamic filtering lets you change the training period you want to analyze, look at workouts with a specific template or progress of a specific exercise.


## Screenshots
![New workout](/Screenshots/new_workout.png)
![Workout details](/Screenshots/workout_details.png)
![Analytics](/Screenshots/analytics.png)
![Analytics filters](/Screenshots/analytics_filters.png)
![Exercises](/Screenshots/exercises.png)
![Workout History](/Screenshots/workout-history.png)



## Setup
To run the project on your machine please install all requirements in a virtual environment from requirements.txt file in the main project folder. Then run a local server on your machine using the manage.py runserver commnad from the terminal.


## Usage
To register as a new user please enter your username and password, the username must be unique and the password requeirements are stated at the registration form. There is no password recovery system implemented at this moment. Plsease be awere that the current databse hosting platform offers only 3 months of database existance so your data will be erased on 06.06.2023. 

To create a new workout please enter the "New workout" menu item and pick a template on which the workout should be based on. The template must be created beforehand. The data for the new workout form will be automatically filled out to make it easier to add progression to your training. The data will be resetet (load = 0 for each set) if one of three thing happened earlier:
- user edited the template
- last workout user has not completed all sets prepared for the workout

In your workout form you should edit every set as ypu progress through your workout. It is important to check the "done" checkbox as this is the condition needed for the set to save. After all sets of the workout are done click the save button at the botton of the form, you will be redirected to the workout details page to see the workout summary and make changes if something is wrong.

The templates manu lets you look wthrough all your workouts templates, edit, delete them and create new ones.

Before creating a template check if all desired exercises are already in the database using the Exercise manu item. If not you can easily create new ones.


## Project Status
Project is: _in progress_ / _complete_ / _no longer being worked on_. If you are no longer working on it, provide reasons why.


## Room for Improvement
Include areas you believe need improvement / could be improved. Also add TODOs for future development.

Room for improvement:
- Improvement to be done 1
- Improvement to be done 2

To do:
- Feature to be added 1
- Feature to be added 2


## Acknowledgements
Give credit here.
- This project was inspired by...
- This project was based on [this tutorial](https://www.example.com).
- Many thanks to...


## Contact
Created by [@flynerdpl](https://www.flynerd.pl/) - feel free to contact me!


<!-- Optional -->
<!-- ## License -->
<!-- This project is open source and available under the [... License](). -->

<!-- You don't have to include all sections - just the one's relevant to your project -->
