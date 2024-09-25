# SPA_health_tracker

This project is the backend part of a web application for tracking users' healthy habits, 
based on James Clear's book Atomic Habits.

## Intro

The book describes a good example of a habit as a specific action that can be put into one sentence:

I will [ACTION] at [TIME] at [LOCATION].

For every useful habit, you should reward yourself or make a pleasant habit immediately afterward. 
But at the same time the habit should not take more than two minutes to perform. 
Based on this we get the first model - “Habit”.


What is the difference between a useful habit and a pleasant and related habit?
A useful habit is the very action that the user will perform and receive a certain reward for performing it 
(a pleasant habit or any other reward).

A pleasant habit is a way to reward yourself for performing a useful habit. A pleasant habit is specified 
as a linked habit for a useful habit (in the Linked Habit field).

For example: as a useful habit, you will go out for a walk around the block right after dinner. 
Your reward for doing so will be the pleasant habit of taking a bubble bath. That is, such a useful 
habit will have a bound habit.

Let's look at another example: the useful habit is “I will not be late for my weekly meeting with friends 
at a restaurant.” As a reward, you order yourself a dessert. In this case, a useful habit has a reward, 
but not a pleasant habit.

The sign of a pleasant habit is a boolean field, which indicates that the habit is pleasant, not useful.


## Setup
Follow the steps below to setup and run the project locally:

1. Clone the Repository.
2. Setup a Virtual Environment.
Navigate to your project directory and create a virtual environment using the command:
python3 -m venv venv
3. Activate the Virtual Environment.
Activate the virtual environment using the following command:
source venv/bin/activate
4. Install Dependencies.
Install all the required dependencies from the 'requirements.txt' file using the command:
pip install -r requirements.txt
5. Setup Environment Variables.
Create an .env file in the root directory of your project and define the variables 
that are in the .env.sample file
6. Initialize the Database.
python manage.py migrate
7. Start the Server
Run the command below to start Django's development server:
python manage.py runserver
The server should now be accessible on http://localhost:8000/


## Usage 

This project provides several API endpoints for interacting with the application:

- `POST /users/register`: Register a new user.
- `POST /users/login`: Log in an existing user.
- `GET /users/<int:pk>/`: Displays detailed information about the user
- `PUT /users/<int:pk>/update/`: Modifies an existing user.

- `GET /habits/habits/`: Get the list of Habits and public Habits.
- `POST /habits/habits/`: Create a new habit.
- `GET /habits/<int:pk>/`: Retrieves the details of a particular Habit.
- `PUT /habits/<int:pk>/`: Updates the details of a particular Habit.
- `PUTCH /habits/<int:pk>/`: Partially updates the details of a particular Habit.
- `DELETE /habits/<int:pk>/`: This operation deletes a particular Habit.


## Docker-compose

1. Install Docker if you don't already have it. You can download it [here](https://docs.docker.com/).
2. Type the command in the terminal: docker-compose up -d --build

