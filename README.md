### DISCLAIMER: This is a student in cybersecurity creating an app with crypto reliance. Please do not trust anything put out there yet. Thanks.

# PainlessPass
PainlessPass is a simple way to store your account credentials. Developed with security in mind, PainlessPass ensures that you, and only **_you_** can access your stored credentials. PainlessPass allows you to store and search through your credentials with ease. PainlessPass is open-source and dockerized, making it easy to run your own instance on your own hardware. 

## Installation
1. Copy the code to your local machine or server
2. Install Docker
3. Edit the app.env, db.env, and settings.py files in order to add necessary secrets and tune the app to your liking
4. Browse to your directory and launch the commands in getting started to install


## Getting Started
These are the commands for now. More to come later!
```bash
docker-compose build
docker-compose up
docker-compose run app python manage.py makemigrations
docker-compose run app python manage.py migrate
```
